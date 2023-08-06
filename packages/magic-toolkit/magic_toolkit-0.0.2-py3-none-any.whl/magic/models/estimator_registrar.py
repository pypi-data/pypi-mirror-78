import os
import sys
import shutil
import importlib
from magic import LOG_INFO
from magic import ConfigParser
from magic import Estimator


def search_config_path(model_name):
    """
    config file ends with _config.py
    """
    root = os.path.join(os.path.dirname(__file__), model_name)
    assert os.path.exists(root), "model name error"
    files = os.listdir(root)

    config_path = None
    for f in files:
        if f.endswith("_config.py"):
            config_path = os.path.join(root, f)
            break
    assert config_path, "not found config, config endswith '_config.py'"
    return config_path


def search_estimator_path(root):
    """
    estimator file ends with _estimator.py
    """
    assert os.path.exists(root), "root of _estimator.py error"
    files = os.listdir(root)

    estimator_path = None
    for f in files:
        if f.endswith("_estimator.py"):
            estimator_path = os.path.join(root, f)
            break
    assert estimator_path, "not found estimator file, endswith '_estimator.py'"
    return estimator_path


def search_estimator(estimator_path):
    """
    ClassName of ModelEstimator ends with Estimator
    """
    project, estimator_file = os.path.split(estimator_path)
    pkg_path, package = os.path.split(project)
    sys.path.insert(0, project)  # support absolute import secondly
    sys.path.insert(0, pkg_path)  # support relative import firstly
    relative = estimator_file.split(".")[0]
    estimator_module = importlib.import_module("." + relative, package=package)

    attrs = dir(estimator_module)
    framework_estimator = ["TorchEstimator",
                           "TensorflowEstimator"]
    estimator_class = None
    for item in attrs:
        if item.endswith("Estimator") and item not in framework_estimator:
            estimator_class = getattr(estimator_module, item)
            break
    assert estimator_class, "not found estimator class, endswith 'Estimator'"
    return estimator_class


def get_config(model_name):
    config_path = search_config_path(model_name)
    shutil.copy(config_path, "./")
    cwd = os.getcwd()
    LOG_INFO("{} config is located in {}".format(model_name, cwd))


def create(*args) -> Estimator:
    """
    search _config.py and _estimator.py to call Estimator
    :return: estimator
    """
    assert len(args) >= 1
    assert args[0].endswith("_config.py")

    config_path = args[0]
    config = ConfigParser(config_path)

    # place _config.py under root of project
    root = os.path.dirname(config_path)
    if not os.path.isabs(root):
        root = os.path.abspath(root)
    try:
        estimator_path = search_estimator_path(root)
    except:
        model_name = config.model_name
        root = os.path.join(os.path.dirname(__file__), model_name)
        estimator_path = search_estimator_path(root)

    estimator_class = search_estimator(estimator_path)
    return estimator_class(config)

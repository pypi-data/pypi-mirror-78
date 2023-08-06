import argparse
import magic


def main():
    parser = argparse.ArgumentParser()
    # list something
    parser.add_argument('--list', default='', metavar='', help='model_list, .trt')
    # get config template
    parser.add_argument('--config', default='', metavar='', help='get config template: pytorch, tensorflow')
    # onnx to trt
    parser.add_argument("--onnx", default='', metavar='', help="onnx path")
    parser.add_argument('--batch', default=1, type=int, metavar='', help="tensorrt max batch，default=1")
    parser.add_argument("--fp16", default=0, type=int, metavar='', help="default=0")
    # fit and export
    parser.add_argument("--fit", default='', metavar='', help='need config file')
    parser.add_argument("--pretrained", default=0, type=int, metavar='', help="default=0")
    parser.add_argument('--summary', default='', metavar='', help='need config file')
    parser.add_argument('--export_model', default='', metavar='', help='need config file')

    args = parser.parse_args()

    # list trt engine info
    if args.list.endswith(".trt"):
        from magic.tensorrt import trt_infer
        sess = trt_infer.TrtSession()
        sess.load_engine(args.list)
    elif args.list == "model_list":
        magic.get_model_list()

    # get config template
    if len(args.config):
        magic.get_config(args.config)

    # onnx to trt
    if len(args.onnx):
        from magic.tensorrt import onnx_convert
        assert args.onnx.endswith(".onnx"), "need .onnx"
        onnx_convert(args.onnx, args.onnx.split('.')[0] + ".trt", args.batch, args.fp16, verbose=1)

    if len(args.fit):
        estimator = magic.create(args.fit)
        if args.pretrained:
            estimator.load()
        estimator.fit()

    if len(args.summary):
        estimator = magic.create(args.summary)
        estimator.summary()

    if len(args.export_model):
        estimator = magic.create(args.export_model)
        estimator.load()
        estimator.export_model()

if __name__ == '__main__':
    main()
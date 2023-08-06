def get_model_list():
    model_list = {
        "RFBNet": "人体检测",
    }

    for key, value in model_list.items():
        print(key.ljust(30), value)
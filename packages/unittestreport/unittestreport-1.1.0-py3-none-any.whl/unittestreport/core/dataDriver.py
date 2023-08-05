from functools import wraps


def data(datas):
    """
    :param datas: 测试数据
    :return:
    """
    def ddt(func):
        setattr(func, "PARAMS", datas)
        return func

    return ddt


def create_test_name(index, name):
    """创建用例名"""
    if index + 1 < 10:
        test_name = name + "_0" + str(index + 1)
    else:
        test_name = name + "_" + str(index + 1)
    return test_name


def update_func(new_func_name, params, test_desc, func, *args, **kwargs):
    """
    生成测试用例
    :param cls: 测试类
    :param new_func_name: 用例方法名
    :param test_desc: 用例描述
    :param params: 用例参数
    :param func: 用例方法
    :return:测试用例方法
    """
    @wraps(func)
    def wrapper(self, ):
        return func(self, params, *args, **kwargs)

    wrapper.__wrapped__ = func
    wrapper.__name__ = new_func_name
    wrapper.__doc__ = test_desc
    return wrapper


def ddt(cls):
    """
    :param cls: 测试类
    :return:
    """
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, "PARAMS"):
            for index, case_data in enumerate(getattr(func, "PARAMS")):
                # 生成用例名称，
                new_test_name = create_test_name(index, name)
                # 生成用例描述
                if isinstance(case_data, dict) and case_data.get("title"):
                    test_desc = case_data.get("title")
                elif isinstance(case_data, dict) and case_data.get("desc"):
                    test_desc = case_data.get("desc")
                else:
                    test_desc = func.__doc__
                func2 = update_func(new_test_name, case_data, test_desc, func)
                setattr(cls, new_test_name, func2)
            else:
                delattr(cls, name)
    return cls

import typing


def fb_dict_factory(var_list: typing.List[typing.Tuple]):
    return {var[0]: var[1] for var in var_list if var[1] is not None}

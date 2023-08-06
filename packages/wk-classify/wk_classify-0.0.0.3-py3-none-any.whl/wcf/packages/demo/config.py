
class ConfigBase:
    @classmethod
    def get_config_info_dict(cls):
        if issubclass(cls.__base__, ConfigBase):
            dic=cls.__base__.get_config_info_dict()
        else:
            dic = {}
        for k, v in cls.__dict__.items():
            if not k.startswith('_') and k[0].upper() == k[0] and v is not None:
                dic[k] = v
        return dic

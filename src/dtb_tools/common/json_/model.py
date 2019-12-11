import json

__all__ = ["JsonBean", "JsonBeanEncoder"]


class JsonBean:
    """
        只是需要 继承 当前类，就可以 实现将 当前类转换为 dict;
        json_filter 是返回json 的时候的 过滤器，如果有值，则返回 其中的属性
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.json_filter = None
        return instance

    def to_json(self):
        b = self.filter_list()

        if not b:
            slot = getattr(self, "__slots__", None)
            if slot is not None:
                return self.__get_by_list(slot)
            else:
                return self.__dict__
        else:
            return self.__get_by_list(b)

    def __get_by_list(self, ls):
        data = {}

        for i in ls:
            d = getattr(self, i, None)
            if d is not None:
                data[i] = d
        return data

    def filter_list(self) -> list:
        """
            返回需要 截取的内容
        :rtype: object
        """
        return self.json_filter


class JsonBeanEncoder(json.JSONEncoder):
    """
        进行 json 转换的时候的  encoder
    """

    def default(self, obj):
        if isinstance(obj, JsonBean):
            return obj.to_json()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super().default(obj)

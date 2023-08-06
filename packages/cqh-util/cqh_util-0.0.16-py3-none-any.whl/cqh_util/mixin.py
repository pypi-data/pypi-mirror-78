import typing
import time


class AssertMixin(object):
    """
    用于单元测试
    """

    def assert_record_and_map_equal(self, record: typing.Union[object, dict], pairs: dict):
        """
        从 `pairs` 里面的每个key, value, `record` 必然存在且相等
        """
        for key, value in pairs.items():
            if not isinstance(record, dict):
                record_value = getattr(record, key)
            else:
                record_value = record[key]

            self.assertEqual(record_value, value, "key:{}, value:{}, record_value:{}".format(
                key, value, record_value
            ))

    def assert_wait_until(self, assert_func, timeout=20):
        """
        一直到now+timeout, 尝试判断assert_func()的返回值为True, 否则报错
        """
        now = int(time.time())
        end = now + timeout
        while 1:

            now = int(time.time())
            if now >= end:
                raise ValueError("Timeout")
            ret = assert_func()
            if ret:
                break
            time.sleep(0.05)


class RecordMixin(object):
    """
    一般用于单元测试
    """
    @classmethod
    def record_mixin_attrs_get(cls, record, dict_or_keys):
        def get_field(name):
            if isinstance(record, dict):
                return record[name]
            return getattr(record, name)
        if isinstance(dict_or_keys, dict):
            dict_or_keys = list(dict_or_keys.keys())
        dict_or_keys = list(dict_or_keys)
        d = {key: get_field(key) for key in dict_or_keys}
        return d

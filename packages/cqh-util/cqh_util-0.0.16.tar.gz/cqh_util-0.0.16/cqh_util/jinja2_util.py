# cqh_goto: __file__||dump_bytecode_start
from jinja2.bccache import BytecodeCache
from jinja2.utils import LRUCache
import logging
_logger = logging.getLogger(__name__)


class MemoryCache(BytecodeCache):
    '''
    添加jinaj2的redis cache
    使用的时候尽量让他成为全局变量，或者classmethod::

        class TemplateRendring(object):
            """
            A simple class to hold methods for rendering templates.
            """

            @property
            def template_env(self):
                if not hasattr(self, '_template_env'):
                    template_dirs = []
                    if self.settings.get('template_path', ''):
                        template_dirs.append(self.settings['template_path'])
                    byte_cache = self.jinja2_cache()
                    # 这个env不是全局的，那么cache有用吗？
                    env = Environment(loader=FileSystemLoader(template_dirs),
                                    auto_reload=False,
                                    bytecode_cache=byte_cache)
                    self._template_env = env
                return self._template_env

            @classmethod
            def jinja2_cache(cls):
                if not hasattr(cls, '_jinja2_cache'):
                    cls._jinja2_cache = MemoryCache(400)
                return cls._jinja2_cache


            def render_template(self, template_name, **kwargs):
                # template_dirs = []
                # if self.settings.get('template_path', ''):
                #     template_dirs.append(self.settings['template_path'])
                # env = Environment(loader=FileSystemLoader(template_dirs))
                env = self.template_env

                try:
                    """
                    # 没有bytecode_cache的时候
                    [I /tornado.general/ 200821 15:02:52 util_common:123] template_raw_render: cost 0.20970797538757324s
                    [I /tornado.general/ 200821 15:02:52 util_common:123] render_template: cost 0.27033448219299316s
                    get_template要这么久？
                    """
                    template = env.get_template(template_name)
                except TemplateNotFound:
                    raise TemplateNotFound(template_name)
                with utils.util_common_loger_context(self.logger, 'template_raw_render'):
                    # [I /tornado.general/ 200821 15:02:52 util_common:123] template_raw_render: cost 0.20970797538757324s
                    # 居然要这么久？
                    content = template.render(kwargs)
                return content

    '''

    def __init__(self, cache_size=400,
                 logger=_logger):
        self.raw_cache = LRUCache(cache_size)
        self.logger = logger

    # def get_bucket(self, environment, name, filename, source):
    #     """Return a cache bucket for the given template.  All arguments are
    #     mandatory but filename may be `None`.
    #     """
    #     self.logger.info("get_cache_key:{}, {}".format(name, filename))
    #     key = self.get_cache_key(name, filename)
    #     checksum = self.get_source_checksum(source)
    #     bucket = Bucket(environment, key, checksum)
    #     self.load_bytecode(bucket)
    #     return bucket

    def load_bytecode(self, bucket):
        try:

            code = self.raw_cache.get(bucket.key)
            self.logger.debug("load_bytecode key:{}, coder: {} ".format(bucket.key, code is None))
            self.logger.debug(self.raw_cache._mapping.keys())
        except Exception:
            raise
            code = None
        if code is not None:
            bucket.bytecode_from_string(code)
    # dump_bytecode_start

    def dump_bytecode(self, bucket):
        # args = (bucket.key, bucket.bytecode_to_string())
        try:
            # self.raw_cache.set(*args)
            self.logger.debug("dump_bytecode key:{}".format(bucket.key))
            self.raw_cache[bucket.key] = bucket.bytecode_to_string()
        except Exception:
            raise

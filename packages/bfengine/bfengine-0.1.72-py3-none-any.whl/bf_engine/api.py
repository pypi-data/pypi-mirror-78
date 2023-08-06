import os
from . import util
from .config import Config
from .core.bot import Bot
from .utils.local_cache import LocalCache
import urllib3

urllib3.disable_warnings()

def init(app_id: str = None, local=False, url=None)->Bot:
    """
    创建bot，并返回实例
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    if not app_id:
        # app_id = util.random_uui
        cache = LocalCache(tmp_dir+"/var.bot")
        if cache:
            app_id = cache["app_id"]
        if not app_id:
            app_id = util.random_uuid()
            cache["app_id"]=app_id
    if local:
        Config.base_url = 'http://172.17.0.1'
    elif url:
        Config.base_url = url
    else:
        Config.base_url = Config.remote_url

    bot = Bot(app_id)
    bot.dm.load()
    return bot

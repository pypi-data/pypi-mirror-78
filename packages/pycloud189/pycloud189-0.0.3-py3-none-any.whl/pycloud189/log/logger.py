import os
import logging
from datetime import datetime
from pycloud189.conf import const

FILE_NAME = const.Constant.log_path
if os.path.isdir(const.Constant.conf_dir) is False:
    os.mkdir(const.Constant.conf_dir)
    if os.path.exists(const.Constant.log_path):
        stat = os.stat(const.Constant.log_path)
        if stat.st_size > (5 * 1024 * 1024):  # >5MB
            os.remove(const.Constant.log_path)

with open(FILE_NAME, 'a+') as f:
    f.write('#' * 10)
    d = datetime.now()
    f.write('{0}'.format(d.strftime('%Y-%m-%d %H:%M:%S')))
    f.write('#' * 10)
    f.write('\n')


def getLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # File output handler
    fh = logging.FileHandler(FILE_NAME)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        '%(levelname)s:%(name)-10s %(message)s'))  # NOQA
    log.addHandler(fh)

    # console output handler
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    if const.Constant.ENABLE_DEBUG:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        log.addHandler(console)
    return log

import os


class Constant(object):
    ENABLE_DEBUG = True
    conf_dir = os.path.join(os.path.expanduser('~'), '.tickstep')
    config_path = os.path.join(conf_dir, 'pycloud189.conf')
    log_path = os.path.join(conf_dir, 'pycloud189.log')
    temp_dir_path = os.path.join(conf_dir, 'temp')

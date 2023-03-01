from configparser import ConfigParser
from os import getcwd, makedirs, path


def conf_parser():

    """Configuration paresr

    Returns:
        [parser]
    """
    parser = ConfigParser()
    CONFIG_DIR = "config"
    CONFIG_FILE_NAME = "config.ini"
    CONFIG_PATH = path.join(CONFIG_DIR, CONFIG_FILE_NAME)
    parser.read(CONFIG_PATH, encoding="utf-8")
    return parser


def create_dir():
    """
    创建资源目录
    """
    src_dir = ["template_dir"]
    for dir in src_dir:
        dir_path = path.join(getcwd(), conf_parser()["BASIC"][dir])
        if not path.exists(dir_path):
            makedirs(dir_path)


if __name__ == "__main__":
    create_dir()
    print(conf_parser().sections())
    for _, v in conf_parser()["BASIC"].items():
        print(v)

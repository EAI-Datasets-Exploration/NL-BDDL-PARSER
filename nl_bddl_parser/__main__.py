import configparser
from nl_bddl_parser.annotations_gui.gui import run_gui

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("../nl-bddl-parser/main_config.ini")

    if config.getboolean("programs", "run_annotation"):
        anno_config_path = config["paths"]["annotation_config"]
        run_gui(anno_config_path)

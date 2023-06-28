import os
import codecs
import json
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from translate_tools import *


WINDOW_SIZE = 900, 600

CONFIG_PATH = "./data/tool_configs.json"
CONFIG_PATH_DEFAULT = "./tool_configs_default.json"


class ExecuterBlock():
    mapping_dict = {}
    trans_sp_cases = {}
    trans_exceptions = {}
    
    block_name = None
    path_widgets_dict = None

    layout_items = None
    
    def __init__(self, proc_args):
        self.path_widgets_dict = {}
        self.layout_items = []
        one_line = len(proc_args["IN"]) < 4 and len(proc_args["OUT"]) < 4 and len(proc_args["IN"]) + len(proc_args["OUT"]) <= 4
        if one_line:
            self.layout_items.append(item_layout := QHBoxLayout())
        for group in proc_args.keys():
            group_value = proc_args[group]
            if group == "NAME":
                self.block_name = group_value
                continue
            combo_box_dict_sub = self.path_widgets_dict[group] = {}
            for path_args in group_value:
                default_val = self.mapping_dict[path_args]
                combo_box_dict_sub[path_args] = (QLineEdit(default_val), default_val)
        
            if one_line:
                self.build_path_block(item_layout, group, group_value)
            else:
                self.layout_items.append(item_layout := QHBoxLayout())
                self.build_path_block(item_layout, group, group_value)

        self.layout_items.append(button_layout := QHBoxLayout())

        button_layout.addWidget(button_1 := QPushButton(self.block_name))
        button_1.clicked.connect(lambda: self.call_excute())

        button_layout.addWidget(button_2 := QPushButton("Reset to Default"))
        button_2.clicked.connect(lambda: self.reset())
        
    
    def build_path_block(self, layout, label_name, grid_args):
        label = QLabel(label_name)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label.setFixedWidth(50)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(label, 0)
        layout.addLayout(grid_layout := QGridLayout(), 1)
        column_count = 0
        for line_item in grid_args:
            if column_count > 0:
                grid_layout.setColumnMinimumWidth(column_count-1, 10)
            label = QLabel(line_item)
            grid_layout.addWidget(label, 0, column_count)
            grid_layout.addWidget(self.path_widgets_dict[label_name][line_item][0], 1, column_count)
            column_count += 2
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


    def reset(self):
        for value in self.path_widgets_dict.values():
            for item, default in value.values():
                item.setText(default)


    def call_excute(self):
        print("[process excute]", self.block_name)

        if self.block_name == "Copy Snapshot":
            trans_src_file = self.path_widgets_dict["IN"]["Target Translation"][0].text()
            trans_target_file = self.path_widgets_dict["OUT"]["Snapshot Translation"][0].text()
            excute_copy(trans_src_file, trans_target_file)
            lang_src_file = self.path_widgets_dict["IN"]["Latest Language Base"][0].text()
            lang_target_file = self.path_widgets_dict["OUT"]["Prev Language Base"][0].text()
            excute_copy(lang_src_file, lang_target_file)

        elif self.block_name == "Sync Base Changes":
            prev_lang_base_f = self.path_widgets_dict["IN"]["Prev Language Base"][0].text()
            latest_lang_base_f = self.path_widgets_dict["IN"]["Latest Language Base"][0].text()
            snapshot_translation_f = self.path_widgets_dict["IN"]["Snapshot Translation"][0].text()
            target_translation_f = self.path_widgets_dict["OUT"]["Target Translation"][0].text()
            diff_report_f = self.path_widgets_dict["OUT"]["Sync Diff Report"][0].text()
            refer_report_f = self.path_widgets_dict["OUT"]["Sync Refer Report"][0].text()

            excute_sync(prev_lang_base_f, latest_lang_base_f, snapshot_translation_f, target_translation_f, diff_report_f, refer_report_f, self.trans_sp_cases, self.trans_exceptions)
        elif self.block_name == "Check Translation Misses":
            latest_lang_base_f = self.path_widgets_dict["IN"]["Latest Language Base"][0].text()
            target_translation_f = self.path_widgets_dict["IN"]["Target Translation"][0].text()
            miss_report_f = self.path_widgets_dict["OUT"]["Check Miss Report"][0].text()
            excute_check(latest_lang_base_f, target_translation_f, miss_report_f, self.trans_sp_cases, self.trans_exceptions)
        elif self.block_name == "Merge Additions to Translation":
            snapshot_translation_f = self.path_widgets_dict["IN"]["Snapshot Translation"][0].text()
            translate_additions_f = self.path_widgets_dict["IN"]["Translate Additions"][0].text()
            target_translation_f = self.path_widgets_dict["OUT"]["Target Translation"][0].text()

            excute_merge(snapshot_translation_f, translate_additions_f, target_translation_f, self.trans_sp_cases, self.trans_exceptions)
        elif self.block_name == "Convert Zh-cn to Zh-tw":
            inputs_dir = self.path_widgets_dict["IN"]["Current Translate Dir"][0].text()
            outputs_dir = self.path_widgets_dict["OUT"]["Transform Translate Dir"][0].text()
            excute_convert(inputs_dir, outputs_dir)
        print("[process excute] Finished")


class Executer():
    widget = None

    def __init__(self, config_args):
        self.widget = QWidget()
        self.widget.setLayout(layout := QVBoxLayout())
        layout.addWidget(Executer.generate_line())
        ExecuterBlock.mapping_dict.update(config_args["default_fileds_paths"])
        ExecuterBlock.trans_sp_cases.update(config_args["translate_special_cases"])
        ExecuterBlock.trans_exceptions.update(config_args["translate_exceptions"])

        for item in config_args["process_mapings_gui"]:
            block = ExecuterBlock(item)
            for layout_item in block.layout_items:
                layout.addLayout(layout_item)
            layout.addWidget(Executer.generate_line())
    
    def generate_line():
        line = QWidget()
        line.setFixedHeight(5)
        line.setAutoFillBackground(True)
        palette = line.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("gray"))
        line.setPalette(palette)
        return line
    

if __name__ == '__main__':
    if os.path.exists(CONFIG_PATH):
        print("config found, path: ", CONFIG_PATH)
    elif os.path.exists(CONFIG_PATH_DEFAULT):
        CONFIG_PATH = CONFIG_PATH_DEFAULT
        print("config not found, use default copy instead: ", CONFIG_PATH_DEFAULT)
    else:
        print("default config file miss, please revert git to recover it")
        sys.exit(0)
    CONFIGS = json.load(codecs.open(CONFIG_PATH, "r", encoding="utf-8"))


    app = QApplication([])
    # 获取屏幕类并调用 geometry() 方法获取屏幕大小
    screen = QApplication.primaryScreen().geometry()  
    desktop_w = screen.width()
    desktop_h = screen.height()

    window = QWidget()
    window.setWindowTitle("Translator")
    window.setGeometry(int((desktop_w - WINDOW_SIZE[0])/2), int((desktop_h - WINDOW_SIZE[1])/2), WINDOW_SIZE[0], WINDOW_SIZE[1])
    window.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])
    
    executer = Executer(CONFIGS)
        
    # executer.widget.move(0, 320)
    executer.widget.setParent(window)
    executer.widget.setFixedWidth(WINDOW_SIZE[0])

    window.show()

    # 5. Run your application's event loop
    sys.exit(app.exec())
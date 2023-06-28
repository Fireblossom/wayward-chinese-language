import os
import codecs
import json

from translate_tools import *


if __name__ == '__main__':
    config_path = "./data/tool_configs.json"
    config_path_default = "./tool_configs_default.json"
    
    # default configs bans all process, copy to modify yourself ones
    if os.path.exists(config_path):
        print("config found, path: ", config_path)
    if os.path.exists(config_path_default):
        config_path = config_path_default
        print("config not found, use default copy instead: ", config_path_default)
    else:
        print("default config file miss, please revert git to recover it")
        exit(0)
    config_args = json.load(codecs.open(config_path, "r", encoding="utf-8"))

    mapping_dict = config_args["default_fileds_paths"]
    trans_sp_cases = config_args["translate_special_cases"]
    trans_exceptions = config_args["translate_exceptions"]
    process_active = config_args["process_active_cli"]

    if "Copy Snapshot" in process_active:
        trans_src_file = mapping_dict["Target Translation"]
        trans_target_file = mapping_dict["Snapshot Translation"]
        excute_copy(trans_src_file, trans_target_file)
        lang_src_file = mapping_dict["Latest Language Base"]
        lang_target_file = mapping_dict["Prev Language Base"]
        excute_copy(lang_src_file, lang_target_file)
    if "Sync Base Changes" in process_active:
        prev_lang_base_f = mapping_dict["Prev Language Base"]
        latest_lang_base_f = mapping_dict["Latest Language Base"]
        snapshot_translation_f = mapping_dict["Snapshot Translation"]
        target_translation_f = mapping_dict["Target Translation"]
        diff_report_f = mapping_dict["Sync Diff Report"]
        refer_report_f = mapping_dict["Sync Refer Report"]
        excute_sync(prev_lang_base_f, latest_lang_base_f, snapshot_translation_f, target_translation_f, diff_report_f, refer_report_f, trans_sp_cases, trans_exceptions)
    if "Check Translation Misses" in process_active:
        latest_lang_base_f = mapping_dict["Latest Language Base"]
        target_translation_f = mapping_dict["Target Translation"]
        miss_report_f = mapping_dict["Check Miss Report"]
        excute_check(latest_lang_base_f, target_translation_f, miss_report_f, trans_sp_cases, trans_exceptions)
    if "Merge Additions to Translation" in process_active:
        snapshot_translation_f = mapping_dict["Snapshot Translation"]
        target_translation_f = mapping_dict["Target Translation"]
        translate_additions_f = mapping_dict["Target Translation"]
        excute_merge(snapshot_translation_f, translate_additions_f, target_translation_f, trans_sp_cases, trans_exceptions)
    if "Convert Zh-cn to Zh-tw" in process_active:
        inputs_dir = mapping_dict["Current Translate Dir"]
        outputs_dir = mapping_dict["Transform Translate Dir"]
        excute_convert(inputs_dir, outputs_dir)
    print("[process excute] All finished")

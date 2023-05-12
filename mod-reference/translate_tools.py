import os
import codecs
import json



# check translation diff between two version of official, then sync the changes to related version of translantion file
# notice that sync will remove all outdate ones, all addition will be ignored
def check_official_diff (base_lan_dict, base_lan_before_dict, tran_lan_dict):
    tran_lan_sync_dict = {}
    diff_report_dict = {}
    
    # removed case is ignored
    for key in base_lan_dict:
        if type(base_lan_dict[key]) == dict:
            if key in base_lan_before_dict and key in tran_lan_dict:
                tran_lan_sync_dict_sub, diff_report_dict_sub = check_official_diff(base_lan_dict[key], base_lan_before_dict[key], tran_lan_dict[key])
                if not diff_report_dict_sub == {}:
                    diff_report_dict[key] = diff_report_dict_sub
                    tran_lan_sync_dict[key] = tran_lan_sync_dict_sub
                else:
                    tran_lan_sync_dict[key] = tran_lan_dict[key]
            else:
                diff_report_dict[key] = base_lan_dict[key]
        elif key in base_lan_before_dict and key in tran_lan_dict and base_lan_before_dict[key] == base_lan_dict[key]:
            tran_lan_sync_dict[key] = tran_lan_dict[key]
        else:
            diff_report_dict[key] = base_lan_dict[key]
            
    return tran_lan_sync_dict, diff_report_dict

# find all items of base that not translated 
def check_translation_diff (base_lan_dict, tran_lan_dict):
    diff_report_dict = {}
    for key in base_lan_dict:
        if type(base_lan_dict[key]) == dict and key in tran_lan_dict:
            diff_report_dict_sub = check_translation_diff(base_lan_dict[key], tran_lan_dict[key])
            if not diff_report_dict_sub == {}:
                diff_report_dict[key] = diff_report_dict_sub
        elif key not in tran_lan_dict:
            diff_report_dict[key] = base_lan_dict[key]
        else:
            pass

    return diff_report_dict


# extract old version of translation for ref, diff of original file can be check by git
def report_translation_diff (tran_lan_dict, diff_report_dict):
    tran_report_dict = {}
    for key in diff_report_dict:
        if type(diff_report_dict[key]) == dict and key in tran_lan_dict:
            tran_report_dict_sub = report_translation_diff(tran_lan_dict[key], diff_report_dict[key])
            if not tran_report_dict_sub == {}:
                tran_report_dict[key] = tran_report_dict_sub
        elif key in tran_lan_dict:
            tran_report_dict[key] = tran_lan_dict[key]
        else:
            pass

    return tran_report_dict


# merge addition_tran into tran_lan_dict, replace by key idx
def merge_translation (tran_lan_dict, addition_tran):
    for key in addition_tran:
        if type(addition_tran[key]) == dict:
            if key in tran_lan_dict:
                merge_translation(tran_lan_dict[key], addition_tran[key])
            else:
                tran_lan_dict[key] = addition_tran[key]
        else:
            tran_lan_dict[key] = addition_tran[key]

def filter_exceptions(filter_dict, tran_exceptions):
    for key, value in list(filter_dict.items()):
        if type(filter_dict[key]) == dict:
            if key in tran_exceptions:
                if tran_exceptions[key] is None or type(tran_exceptions[key]) != dict:
                    del filter_dict[key]
                else:
                    filter_exceptions(filter_dict[key], tran_exceptions[key])
            else:
                pass
        elif key in tran_exceptions and type(tran_exceptions[key]) != dict:
            del filter_dict[key]
        else:
            pass

if __name__ == '__main__':
    # default configs bans all process, copy to modify yourself ones
    config_path = "./script_data/tool_configs.json"
    config_default_path = "./tool_configs_default.json"
    if os.path.exists(config_path):
        print("config found, path: ", config_path)
    elif os.path.exists(config_default_path):
        print("config not found, pls copy default config to script_data dir and modify for yourself ones, found default here: ", config_default_path)
        exit(0)
    else:
        print("default config file miss, please revert git to recover it")
        exit(0)
    configs = json.load(codecs.open(config_path, "r", encoding="utf-8"))
    
    # check diffs between official language file, report and remove it from translation for each remove & changes
    if configs["update_process_paths"]["active"]:
        print("update process active, will check for official diffs")
        configs["translate_exceptions"]
        configs["translate_special_cases"]
        update_conf = configs["update_process_paths"]
        # official language file, old version's copy
        official_prev_ver = json.load(codecs.open(update_conf["in"]["official_prev_ver"], "r", encoding="utf-8"))
        # official language file, latest/target version
        official_latest_ver = json.load(codecs.open(update_conf["in"]["official_latest_ver"], "r", encoding="utf-8"))
        # translated language file, old version's copy, here use the mod's main translate file
        translation_prev_ver = json.load(codecs.open(update_conf["in"]["translation_prev_ver"], "r", encoding="utf-8"))

        # check diff between diff versions of base lang file
        tran_lan_sync, diff_report = check_official_diff(official_latest_ver, official_prev_ver, translation_prev_ver)
        merge_translation(tran_lan_sync, configs["translate_special_cases"])
        filter_exceptions(tran_lan_sync, configs["translate_exceptions"])

        filter_exceptions(diff_report, configs["translate_special_cases"])
        filter_exceptions(diff_report, configs["translate_exceptions"])
        tran_report = report_translation_diff(translation_prev_ver, diff_report)

        
        # this file will keep all translation items without changes/removes, can be seen as fast compatibility version
        json.dump(tran_lan_sync, codecs.open(update_conf["out"]["translation_sync"], "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        # this file will found all changes/adds, as the base of additional translation file, waiting for re-translation
        json.dump(diff_report, codecs.open(update_conf["out"]["report_diff"], "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        # this file will remains all changes of old version's translation, as reference for re-translation work, no other usages
        json.dump(tran_report, codecs.open(update_conf["out"]["report_refer"], "w", encoding="utf-8"), indent=4, ensure_ascii=False)

    if configs["check_process_paths"]["active"]:
        print("check process active, will find diffs of translation and official lang")

        check_conf = configs["check_process_paths"]

        # translated language file, old version's copy, here use the mod's main translate file
        translation_prev_ver = json.load(codecs.open(check_conf["translation_prev_ver"], "r", encoding="utf-8"))
        # official language file, latest/target version
        official_latest_ver = json.load(codecs.open(check_conf["official_latest_ver"], "r", encoding="utf-8"))        
        
        # check diff between diff versions of base lang file
        miss_report = check_translation_diff(official_latest_ver, translation_prev_ver)
        filter_exceptions(miss_report, configs["translate_special_cases"])
        filter_exceptions(miss_report, configs["translate_exceptions"])

        # this file will found all miss of translation, as the base of additional translation file, waiting for work
        json.dump(miss_report, codecs.open(check_conf["report_miss"], "w", encoding="utf-8"), indent=4, ensure_ascii=False)


    # for each item, report and replace it with addition translation when exists
    if configs["merge_process_paths"]["active"]:        
        print("merge process active, will merge diffs into prev translation")

        merge_conf = configs["merge_process_paths"]
        # translated language file to be merged, should be same format with latest lang file
        base_tran = json.load(codecs.open(merge_conf["translation_prev_ver"], "r", encoding="utf-8"))
        # can be missing/replacing translations to be merged in, usually translated from report of diff
        addition_tran = json.load(codecs.open(merge_conf["addition_translations"], "r", encoding="utf-8"))

        merge_translation(base_tran, addition_tran)
        merge_translation(base_tran, configs["translate_special_cases"])
        filter_exceptions(base_tran, configs["translate_exceptions"])
        # this file will keep all translation items without changes/removes, can be seen as fast compatibility version
        json.dump(base_tran, codecs.open(merge_conf["merged_out_path"], "w", encoding="utf-8"), indent=4, ensure_ascii=False)

    # convert all files from zh to zh-tw by lines, the 2nd line should be lang type
    if configs["convert_process_paths"]["active"]:
        print("convert process active, will convert zh to zh-tw")
        from zhconv import convert
        
        convert_conf = configs["convert_process_paths"]
        
        if not (os.path.isdir(convert_conf["inputs"]) and os.path.isdir(convert_conf["outputs"]) ):
            print("given path is not dir")
        else:
            for filename in os.listdir(convert_conf["inputs"]):
                input_filepath = os.path.join(convert_conf["inputs"], filename)
                if os.path.isfile(input_filepath):
                    # target output of zh-tw, convert from the merged one
                    line_count = 0
                    output_filepath = os.path.join(convert_conf["outputs"], filename)
                    with codecs.open(input_filepath, "r", encoding="utf-8") as input:
                        with codecs.open(output_filepath, "w", encoding="utf-8") as output:
                            line = input.readline()
                            output.write(line)
                            line = input.readline()
                            output.write(convert(line.replace("简体", "繁体"), 'zh-tw'))
                            for line in input.readlines():
                                output.write(convert(line, 'zh-tw'))

    print("all process finished")

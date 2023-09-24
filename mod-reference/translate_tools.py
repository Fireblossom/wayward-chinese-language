import os
import codecs
import shutil
import json

from zhconv import convert


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


# filter ones defined as not translated before
def filter_exceptions(filter_dict, tran_exceptions):
    for key in list(filter_dict.keys()):
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


# convert zh-cn to zh-tw
def convert_process(inputs_dir, outputs_dir):
    for filename in os.listdir(inputs_dir):
        input_filepath = os.path.join(inputs_dir, filename)
        if os.path.isfile(input_filepath):
            # target output of zh-tw, convert from the merged one
            output_filepath = os.path.join(outputs_dir, filename)
            with codecs.open(input_filepath, "r", encoding="utf-8") as input:
                with codecs.open(output_filepath, "w", encoding="utf-8") as output:
                    line = input.readline()
                    output.write(line)
                    line = input.readline()
                    output.write(convert(line.replace("简体", "繁体"), 'zh-tw'))
                    for line in input.readlines():
                        output.write(convert(line, 'zh-tw'))


def excute_copy(src_file, target_file):
    print("[excute copy] will copy for snapshot")
    if not os.path.isdir(target_file):
        dirname = os.path.dirname(target_file)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    shutil.copy(src_file, target_file)


def excute_sync(prev_lang_base_f, latest_lang_base_f, snapshot_translation_f, target_translation_f, diff_report_f, refer_report_f, trans_sp_cases, trans_exceptions):
    print("[excute sync] will check for official diffs")
    # official language file, old version's copy
    prev_lang_base = json.load(codecs.open(prev_lang_base_f, "r", encoding="utf-8"))

    # official language file, latest/target version
    latest_lang_base = json.load(codecs.open(latest_lang_base_f, "r", encoding="utf-8"))

    # translated language file, old version's copy, here use the mod's main translate file
    snapshot_translation = json.load(codecs.open(snapshot_translation_f, "r", encoding="utf-8"))

    # check diff between diff versions of base lang file
    tran_lan_sync, diff_report = check_official_diff(latest_lang_base, prev_lang_base, snapshot_translation)
    merge_translation(tran_lan_sync, trans_sp_cases)
    filter_exceptions(tran_lan_sync, trans_exceptions)

    filter_exceptions(diff_report, trans_sp_cases)
    filter_exceptions(diff_report, trans_exceptions)
    refer_report = report_translation_diff(snapshot_translation, diff_report)

    
    # this file will keep all translation items without changes/removes, can be seen as fast compatibility version
    json.dump(tran_lan_sync, codecs.open(target_translation_f, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    # this file will found all changes/adds, as the base of additional translation file, waiting for re-translation
    json.dump(diff_report, codecs.open(diff_report_f, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    # this file will remains all changes of old version's translation, as reference for re-translation work, no other usages
    json.dump(refer_report, codecs.open(refer_report_f, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def excute_check(latest_lang_base_f, target_translation_f, miss_report_f, trans_sp_cases, trans_exceptions):
    print("[excute check] will find diffs of translation and official lang")
    # translated language file, old version's copy, here use the mod's main translate file
    tran_lan_to_check = json.load(codecs.open(target_translation_f, "r", encoding="utf-8"))
    # official language file, latest/target version
    latest_lang_base = json.load(codecs.open(latest_lang_base_f, "r", encoding="utf-8"))        
    
    # check diff between diff versions of base lang file
    miss_report = check_translation_diff(latest_lang_base, tran_lan_to_check)
    filter_exceptions(miss_report, trans_sp_cases)
    filter_exceptions(miss_report, trans_exceptions)

    # this file will found all miss of translation, as the base of additional translation file, waiting for work
    json.dump(miss_report, codecs.open(miss_report_f, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def excute_merge(snapshot_translation_f, translate_additions_f, target_translation_f, trans_sp_cases, trans_exceptions):
    print("[excute merge] will merge diffs into prev translation")

    # translated language file to be merged, should be same format with latest lang file
    base_tran = json.load(codecs.open(snapshot_translation_f, "r", encoding="utf-8"))
    # can be missing/replacing translations to be merged in, usually translated manual from report of diff
    if not os.path.exists(translate_additions_f):
        print("[excute merge][ERROR] translate additions should be written manually")
        return
    trans_addition = json.load(codecs.open(translate_additions_f, "r", encoding="utf-8"))

    merge_translation(base_tran, trans_addition)
    filter_exceptions(base_tran, trans_exceptions)
    merge_translation(base_tran, trans_sp_cases)
    # this file will keep all translation items without changes/removes, can be seen as fast compatibility version
    json.dump(base_tran, codecs.open(target_translation_f, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def excute_convert(inputs_dir, outputs_dir):
    print("[excute convert] will convert zh to zh-tw")
    if not (os.path.isdir(inputs_dir) and os.path.isdir(outputs_dir) ):
        print("given path is not dir")
    else:
        convert_process(inputs_dir, outputs_dir)

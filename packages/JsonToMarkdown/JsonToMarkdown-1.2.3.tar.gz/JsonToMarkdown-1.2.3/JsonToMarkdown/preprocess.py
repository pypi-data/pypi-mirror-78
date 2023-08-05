# -*- coding: utf-8 -*-

import json


class PreProcess(object):
    def __init__(self):
        pass

    def start(self, json_file):
        with open(json_file, 'r') as jf:
            js_dict = json.load(jf)
        return js_dict

if __name__ == "__main__":
    pp = PreProcess()
    #js_dict = pp.start("aaa.json")
    js_dict = pp.start("npu_register.json")
    print(js_dict)


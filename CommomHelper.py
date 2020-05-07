'''
    工具类
'''
import json

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open( style , 'r',  encoding='UTF-8') as f:
            return f.read()

    @staticmethod
    def load_json(path):
        return json.load(open(path, 'r', encoding='utf-8'))

    @staticmethod
    def load_setting(path):
        return json.load(open(path, 'r', encoding='utf-8'))

    @staticmethod
    def load_english_source(path):
        return json.load(open(path, 'r', encoding='utf-8'))

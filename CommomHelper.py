'''
    工具类
'''
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open( style , 'r',  encoding='UTF-8') as f:
            return f.read()

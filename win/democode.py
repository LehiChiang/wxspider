import re

flg=True
def jobCode(txtstr,regex):
    result=re.search(regex,txtstr)
    if result.group()==txtstr:
        return flg==True
    else:
        return flg==False

#程序主入口
if __name__=='__main__':
    txtstr=str(input("请输入待匹配的字符串："))
    regex=input("请输入正则表达式:")
    print(jobCode(txtstr,regex)) #调用定义函数jobCode()
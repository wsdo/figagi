'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-27 10:11:12
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-29 01:44:47
Description: 
'''
import re

# 将段落分成小的句子
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

# 在分局的基础上，设置最小句子长度，方便获取长段落
def cut_sent_long(para, min_long = 0):
    sentences = cut_sent(para=para)

    sentence = None
    result = []

    for sen in sentences:
        if (sentence is None):
            sentence = sen
        else:
            sentence = sentence + sen

        if (len(sentence) > min_long):
            result.append(sentence)
            sentence = None
    
    if (sentence is not None):
        result.append(sentence)

    return result
            
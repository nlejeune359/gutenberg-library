import re

def cleanStr(inputStr):
    inputStr.replace('\n', '').replace('\r', '')
    res = re.sub(r'[^\w\s]', '', inputStr)
    return res


def splitInToken(inputStr):
    res = inputStr.split(' ')
    return list(filter(lambda x: x != ' ' and x != '', res))


def createTokenList(inputStr):
    return splitInToken(cleanStr(inputStr))

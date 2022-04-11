import re


def cleanStr(inputStr):
    inputStr_ = inputStr.lower().replace('\n', ' ').replace('\r', ' ')
    res = re.sub(r'[^\w\s]', '', inputStr_)
    return res


def splitInToken(inputStr):
    splitedData = inputStr.split(' ')
    res = list(filter(lambda x: x != ' ' and x != '', splitedData))
    return set(res), res


def createTokenList(inputStr):
    return splitInToken(cleanStr(inputStr))

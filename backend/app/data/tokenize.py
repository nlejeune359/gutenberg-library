import re

def cleanStr(inputStr):
    inputStr_ = inputStr.lower().replace('\n', '').replace('\r', '')
    res = re.sub(r'[^\w\s]', '', inputStr_)
    return res


def splitInToken(inputStr):
    res = inputStr.split(' ')
    return set(filter(lambda x: x != ' ' and x != '', res))


def createTokenList(inputStr):
    return splitInToken(cleanStr(inputStr))

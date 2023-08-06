
from .pos import pos_japanese

import re
import warnings
import jieba

from nltk.tokenize import RegexpTokenizer


def brace(article):
    result = []
    
    # doing the regression
    conversation = re.findall('(「.*?」)', article)
    rename = re.findall('(（.*?\）)', article)
    entity = re.findall('(【.*?\】)', article)
    name = re.findall('(＜.*?\＞)', article)
    
    # merged together
    result += conversation
    result += rename
    result += entity
    result += name

    return result



def NER(text, language):
    """Word token
    
    Arguments:
        text {[str]} -- [description]
        langurage {[str]} -- [description]
    
    Returns:
        [list] -- [description]
    """
    if language == "japanese":
        ls_word = []
        ls_pos = []
        data = pos_japanese(text)
        for item in data:
            # print(item)
            if "固有名詞" in item[1]:
                ls_word.append(item[0])
        # ls_word.extend(brace(text))
        return ls_word
    else:
        return []


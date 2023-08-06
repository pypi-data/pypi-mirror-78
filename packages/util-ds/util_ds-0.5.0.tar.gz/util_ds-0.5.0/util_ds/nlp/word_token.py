
import re
import warnings

import jieba
# from nltk.tokenize import RegexpTokenizer

from sudachipy import tokenizer
from sudachipy import dictionary
import MeCab

from .pos import pos_japanese

tokenizer_obj_japanese = dictionary.Dictionary().create()

def japanese_num_replace(text,reversed=False):
    """Change the jp to math

    # Arguments
        - text {str}: e.g. "abcde。"
    """

    jp_num = ["１","２","３","４","５","６","７","８","９","０"]
    math_num = ["1","2","3","4","5","6","7","8","9","0"]
    if reversed:
        for item in range(10):
            text = re.sub(math_num[item], jp_num[item], text)
    else:
        for item in range(10):
            text = re.sub(jp_num[item], math_num[item], text)
    return text 


def word_token(text, language, pos=False):
    """Word token
    
    Arguments:
        text {[str]} -- [description]
        langurage {[str]} -- [description]
    
    Returns:
        [list] -- [description]
    """
    if language == "chinese":
        # r = r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+"
        # r = r"[\s+\.\/_,$%^*()?;；:-【】+\"\']+|[+——;:、~@#￥%……&*（）]+"
        # r = r"[\s+\.\/_,$%^*?;；:-+\"\']+|[+——;:、~@#￥%……&*（）]+"
        # text = re.sub(r, '', text)
        list_words = list(jieba.cut(text))
        return list_words
    elif language == "english":
        tokenizer = RegexpTokenizer(r'\w+')
        list_words = tokenizer.tokenize(text)
        return list_words
    elif language == "japanese":
        print("The Word Token is based on Mecab 1.0.1.")
        wakati = MeCab.Tagger("-Owakati")
        return wakati.parse(text).split()
    
    elif language == "japanese_sudachipy":
        from sudachipy import tokenizer
        mode = tokenizer.Tokenizer.SplitMode.B
        if not pos:
            ls_word = [m.surface() for m in tokenizer_obj_japanese.tokenize(text, mode)]
            return ls_word
        else:
            ls_word = [m.surface() for m in tokenizer_obj_japanese.tokenize(text, mode)]
            ls_pos = [m.part_of_speech() for m in tokenizer_obj_japanese.tokenize(text, mode)]
            return (ls_word, ls_pos)
        
    elif language == "japanese_mecab":
        ls_word = []
        ls_pos = []
        data = pos_japanese(text)
        for item in data:
            # print(item)
            if "記号" not in item[1]:
                ls_word.append(item[0])
                ls_pos.append(item[1])
            else: 
                if "記号-句点" in item[1] or "記号-読点" in item[1] or "記号-括弧" in item[1]:
                    ls_word.append(item[0])
                    ls_pos.append(item[1])
        return ls_word
    
    elif language == "jp_pos":
        ls_word = []
        ls_pos = []
        data = pos_japanese(text)
        for item in data:
            ls_word.append(item[0])
            ls_pos.append(item[1])
        return ls_pos
    
    elif language == "jp_pos_word":
        words = []
        data = pos_japanese(text)
        for item_pair in data:
            if "名詞" in item_pair[1] or "動詞" in item_pair[1]:
                words.append(item_pair[1])
            elif "記号" in item_pair[1]:
                pass
            else: 
                words.append(item_pair[0])
        return words
    
    elif language == "japanese_conversation":
        ls_word = []
        ls_pos = []
        dic, text = brace(text)
        data = pos_japanese(text)
        for item in data:
            if "記号" not in item[1]:
                ls_word.append(item[0])
                ls_pos.append(item[1])
            else: 
                if "記号-句点" in item[1] or "記号-読点" in item[1]:
                    ls_word.append(item[0])
                    ls_pos.append(item[1])
        ls_word = brace_reversed(ls_word, dic)
        return ls_word


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

    # unique
    result = list(set(result))

    for idx, item in enumerate(result):
        article = re.sub(item, " REPLACE{} ".format(idx), article)

    return result, article


def brace_reversed(list_word, dic):
    result = []

    start = 0
    for idx, item in enumerate(list_word):
        if item == "REPLACE":
            start = 1
        elif start == 1:
            word_index = int(item)
            result.append(dic[word_index])
            start = 0
        else:
            result.append(item)
    return result

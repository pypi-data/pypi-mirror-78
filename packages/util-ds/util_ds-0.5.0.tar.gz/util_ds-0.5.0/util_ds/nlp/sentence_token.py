
from .Sumy.summarizers.text_rank import TextRankSummarizer
from .Sumy.nlp.stemmers import Stemmer
from .Sumy.utils import get_stop_words
from .Sumy.parsers.html import HtmlParser
from .Sumy.parsers.plaintext import PlaintextParser
from .Sumy.nlp.tokenizers import Tokenizer
import re


def sentenceTaken(language, text):
    sentences = []
    summarizer = TextRankSummarizer(Stemmer(language))
    summarizer.stop_words = get_stop_words(language)
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    for item in parser.document.sentences:
        sentences.append("{}".format(item))
    # print(sentences)
    return sentences

'''This is the sub functions'''

def _sentence_taken(language, text):
    text = re.sub("◆|■|", 
                    "", text, count=0, flags=0)
    text = text.replace("[STOP]","")
    text = _conversation_detection(text)
    pattern = '([。！？\?])([^」』）])'
    summary_split = re.sub(pattern, r"\1\n\2", text).split("\n")
    summary_split = list(map(lambda x: x.strip(), summary_split))
    summary_split = list(filter(lambda x: x!="", summary_split))
    summary_split = _reversed_conversation(summary_split)
    summary_split = list(map(lambda x: _number_normalization(x), summary_split)) 
    return summary_split

def _reversed_conversation(text_list):
    result = []
    for item in text_list:
        result.append(item.replace("unk","。"))
    return result

def _conversation_detection(text, language="japanese"):
    textcp = text
    for item in re.findall("「.*?」",textcp):
        idx = text.index(item)
        text = text[:idx] + text[idx:idx+len(item)].replace("。","unk") + text[idx+len(item):]
    return text

def _number_normalization(text,reversed=False):
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


if __name__ == "__main__":
    print(sentenceTaken("chinese",text))
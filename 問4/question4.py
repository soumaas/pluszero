#形態素解析とはなにかを簡単に説明してください。
#文章を単語ごとに分類して、その単語の品詞を解析する手法

import re
import MeCab
from bs4 import BeautifulSoup
import pandas as pd

def answer(text_path,num):    
    with open(text_path, 'r', encoding="utf-8") as f:
         sentenses = f.readlines()     

    mecabTagger = MeCab.Tagger()
    df_natural = pd.DataFrame()
    cols =re.split('\t|,', '表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音')

    #形態素解析をして、DataFrameに変換する
    for i in range(len(sentenses)):
        mecab_sen = mecabTagger.parse(sentenses[i])
        sep_sen = re.split('\n', mecab_sen)    
        sep_words_list = []

        for num1 in range(len(sep_sen)-1):
            sep_words_list.append(re.split('\t|,', sep_sen[num1]))  

        df = pd.DataFrame(sep_words_list, columns = cols)
        df_natural = pd.concat([df_natural,df])  

    #動詞の個数がnum以上のDataFrameを抽出する
    df_verb        = df_natural.query('品詞 == "動詞"')
    verb_counts    = df_verb["原形"].value_counts()
    df_unique_verb = verb_counts.rename_axis('unique_values').reset_index(name='counts')
    df_answer      = df_unique_verb.query("counts > @num")
    return df_answer["unique_values"]

text_path = "C:\\Users\\souma\\OneDrive\\デスクトップ\\チェックテスト\\project4\\text.txt"
print(answer(text_path,10))
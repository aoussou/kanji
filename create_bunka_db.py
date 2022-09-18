#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 22:35:51 2022

@author: ceo
"""

import pandas as pd
import json
from mecabutils import *
hira_tupple = ('あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん','っ','ゃ','ゅ','ょ','ー','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び','ぶ','べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ')
kata_tupple = ('ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ヲ','ン','ッ','ャ','ュ','ョ','ー','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ')

df = pd.read_csv("./bunka.csv")


def populateDict(dict_,base_pronunciation,examples_line_break_down,pronunciation_type):
    
    populated_dict = dict_
    example_list = examples_line_break_down[j].split("，")
    if '' in example_list: example_list.remove('')
    
    example_dict = dict()
    

    for i,example in enumerate(example_list):
  
        ind_parenthesis = example.find("（")
        
        if ind_parenthesis != -1:
            example = example[:ind_parenthesis]

        target_furigana = getTargetWordFurigana(example,base_pronunciation)
        
        

        # If it's a kunyomi, you might need to remove the okurgianas 
        if pronunciation_type == "kun":
            
            # Given the structure of the data,　in most cases only the first 
            # example matches exactly the pronunciation
            if i == 0:
                
                stem_furigana = removeOkurigana(example,target_furigana)
            
            # print("base:", base_pronunciation,"example:",example,"target_furigana",target_furigana,"stem_furigana",stem_furigana)
        else:
            stem_furigana = target_furigana

        example_dict[example] = stem_furigana
        
    populated_dict[pronunciation_type + str(len(dict_) + 1)] = {
        "base_pronunciation": base_pronunciation,
        "examples": example_dict,
        }
    
    return populated_dict


kanji_dict = dict()

for i,row in df.iterrows():
    
    kanji = row["漢字"]
    ind_parenthesis = kanji.find("（")
    
    if ind_parenthesis != -1:
        kanji = kanji[:ind_parenthesis]

    pronunciation = row["音訓"]
    pronun_line_break_down = pronunciation.split("\n")
    

    
    if not pd.isnull(row["例"]):
        examples = row["例"]
        examples_line_break_down = examples.split("\n")
    else:
        examples = row["備考"]
        examples_line_break_down = examples.split("\n")        

    on_yomi = dict()
    kun_yomi = dict()  
    
    
    
    for j, base_pronunciation in enumerate(pronun_line_break_down):
        
        base_pronunciation = base_pronunciation.replace('　','')
        
        for char in kata_tupple:
            if char in base_pronunciation:
                on_yomi = populateDict(on_yomi,base_pronunciation,examples_line_break_down,"on")
                break           
            
            
        for char in hira_tupple:
            if char in base_pronunciation:
                kun_yomi = populateDict(kun_yomi,base_pronunciation,examples_line_break_down,"kun")
                break

    kanji_dict[kanji] = {"on": on_yomi, "kun": kun_yomi}
    

kanken_kanjis = pd.read_csv("./kanken_kanji.csv")
columns = kanken_kanjis.columns

for kyu in columns:
    
    c = kanken_kanjis[kyu].dropna().tolist()
    
    for kanji in c:
        
        info = kanji_dict[kanji]
        kanji_dict[kanji] = {"on": info["on"], "kun": info["kun"], "kyu": kyu[:-1]}
    
for kanji, info in kanji_dict.items():
    
    if len(info)<3:
        kanji_dict[kanji] = {"on": info["on"], "kun": info["kun"], "kyu": 2}
        

with open("kanji_bunka.json", 'w') as fp:
    json.dump(kanji_dict, fp)
fp.close()
    
    
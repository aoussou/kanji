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


def populateDict(dict_,most_common_word_pronunciation,example_list,pronunciation_type,kanji):
    
    populated_dict = dict_
    
    
    example_dict = dict()
    

    for i,example in enumerate(example_list):
  

        ind_parenthesis = example.find("（")
        
        if ind_parenthesis != -1:
            example = example[:ind_parenthesis]


                  

        # if example == '獲る':      
        #     print(example,most_common_word_pronunciation,whole_word_furigana)
        
            

        # If it's a kunyomi, you might need to remove the okurgianas 
        if pronunciation_type == "kun":
            
            # Given the structure of the data,　in most cases only the first 
            # example matches exactly the pronunciation


            if i == 0:
                
                base_pronunciation = getBasePronunciationKunYomi(kanji,example,most_common_word_pronunciation)
                # print(base_pronunciation)

                # if example == '獲る':
                #     print(example,'*', most_common_word_pronunciation,'*',whole_word_furigana,'*',stem_furigana)
                #     STOP
            # else:
            # print("k:",kanji,"e:",example,"w:",most_common_word_pronunciation,"b:",base_pronunciation)
            
            if len(base_pronunciation) != 0 : 
                target_furigana = getTargetWordFurigana(example,base_pronunciation)
                if target_furigana == "" : target_furigana = base_pronunciation
            else:
                print("couldn't find base pronunciation for",kanji,"in",example,"going with",most_common_word_pronunciation)
                target_furigana = most_common_word_pronunciation
            
            # if len(whole_word_furigana) == 0:
            #     target_furigana = stem_furigana
            #     base_pronunciation = stem_furigana
            # elif len(stem_furigana) == 0:
            #     target_furigana = whole_word_furigana
            #     base_pronunciation = whole_word_furigana
            # else:
            #     target_furigana = whole_word_furigana[:len(stem_furigana)]
            #     base_pronunciation = stem_furigana
            # print("base:", base_pronunciation,"example:",example,"whole_word_furigana",whole_word_furigana,"stem_furigana",stem_furigana)
        else:
            base_pronunciation = most_common_word_pronunciation
            target_furigana =  getTargetWordFurigana(example,most_common_word_pronunciation)

        # print(kanji,example)
        example_dict[example] = target_furigana
        

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
        
    ind_bracket = kanji.find("［")
    if ind_bracket != -1:
        kanji = kanji[:ind_bracket]

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
    
    if '\xa0 ' in pronun_line_break_down: pronun_line_break_down.remove('\xa0 ')
    

    for j, most_common_word_pronunciation in enumerate(pronun_line_break_down):
        
        most_common_word_pronunciation = most_common_word_pronunciation.replace('　','')

        # if '' in examples_line_break_down: examples_line_break_down.remove('')        
        example_list = examples_line_break_down[j].split("，")

        if example_list == [''] : break
        
        if '' in example_list: example_list.remove('')   
        
        # print(kanji,examples_line_break_down)
        
        for char in kata_tupple:
            if char in most_common_word_pronunciation:
                on_yomi = populateDict(on_yomi,most_common_word_pronunciation,example_list,"on",kanji)
                break           
            
            
        for char in hira_tupple:
            if char in most_common_word_pronunciation:
                kun_yomi = populateDict(kun_yomi,most_common_word_pronunciation,example_list,"kun",kanji)
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
    
    
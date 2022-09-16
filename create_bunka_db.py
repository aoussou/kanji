#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 22:35:51 2022

@author: ceo
"""

import pandas as pd
import json

hira_tupple = ('あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん','っ','ゃ','ゅ','ょ','ー','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び','ぶ','べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ')
kata_tupple = ('ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ヲ','ン','ッ','ャ','ュ','ョ','ー','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ')

df = pd.read_csv("./bunka.csv")

kanji_dict = {}
for i,row in df.iterrows():
    
    kanji = row["漢字"]
    ind_parenthesis = kanji.find("（")
    
    if ind_parenthesis != -1:
        kanji = kanji[:ind_parenthesis]

    pronounciation = row["音訓"]
    pronoun_line_break_down = pronounciation.split("\n")
    

    
    if not pd.isnull(row["例"]):
        examples = row["例"]
        examples_line_break_down = examples.split("\n")
    else:
        examples = row["備考"]
        examples_line_break_down = examples.split("\n")        

    on_yomi = {}
    kun_yomi = {}    
    for j,l in enumerate(pronoun_line_break_down):
        
        for char in kata_tupple:
            if char in l:
                
                on_yomi["onyomi" + str(len(on_yomi) + 1)] = {
                    "pronunciation": l,
                    "examples": examples_line_break_down[j]
                    }
                break
            
        for char in hira_tupple:
            if char in l:
                
                kun_yomi["kyunyomi" + str(len(kun_yomi) + 1)] = {
                    "pronunciation": l,
                    "examples": examples_line_break_down[j]
                    }
                break


    kanji_dict[kanji] = {"on": on_yomi, "kun": kun_yomi}
    print(i,kanji)    
    # print(i,kanji,len(pronoun_line_break_down)-len(examples_line_break_down))
    
    
with open("kanji_bunka.json", 'w') as fp:
    json.dump(kanji_dict, fp)
fp.close()
    
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 00:28:34 2022

@author: ceo
"""

"""
https://www.kokugobunpou.com/%E6%96%87%E6%B3%95%E3%81%AE%E5%9F%BA%E7%A4%8E/%E5%8D%98%E8%AA%9E%E3%81%AE%E5%88%86%E9%A1%9E-3-%E5%93%81%E8%A9%9E%E3%81%AE%E5%88%86%E9%A1%9E/#gsc.tab=0


https://manapedia.jp/text/1363
"""
import MeCab
from suffix_trees import STree

hira_list = ['あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん','っ','ゃ','ゅ','ょ','ー','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び','ぶ','べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ']
kata_list = ['ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ヲ','ン','ッ','ャ','ュ','ョ','ー','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ']
k2h_dict = dict()

for i in range(len(hira_list)):
    k2h_dict[kata_list[i]] = hira_list[i]
    
    

def getMecabDict(str_):
    
    """
    Return a dictionary version of Mecab's output.
    """
    
    t = MeCab.Tagger()

    node = t.parseToNode(str_)
    
    dict_ = {}
    count = 0
    while node:
        
        local_dict = {}
        f = node.feature.split(',')

        if f[0] == "BOS/EOS" or len(f)<8:
            pass
        else:

            local_dict['word_type'] = f[0]
            local_dict['subcategory'] = f[1]     
            local_dict['grammatical_properties'] = f[2]
            local_dict['verb_type'] = f[4]
            local_dict['original_kanji_word'] = f[8]
            local_dict['katakana_pronunciation'] = f[9]
            local_dict['infinitive_katakana'] = f[11]
            local_dict['hiragana_equivalent'] = f[17]
            dict_[count] = local_dict
    
        count += 1         
     
        node = node.next

    return dict_


def getKatakanaString(str_):
    
    """
    Given a string including kanji, return the katakana only equivalent string.
    """
    
    t = MeCab.Tagger()
    node = t.parseToNode(str_)    
    katakana_str = ''
    
    while node:
        
        wclass = node.feature.split(',')

        if len(wclass) > 6:
            katakana_str += wclass[17]
        
        node = node.next

    return katakana_str.replace('*','')


def kata2hira(katakana):

    """
    Given a katakana string, return the hiragana equivalent.
    """
    
    hira = ""

    for c in list(katakana):
        if c in k2h_dict:
            hira += k2h_dict[c]
        else: 
            hira += c
            
    return hira


def getHiraganaString(sentence):

    kata = getKatakanaString(sentence)
    hira = kata2hira(kata)
    
    return hira
    
    

def getHiraganaTarget(sentence,kanji):

    hira = getHiraganaString(kanji)
    
    
    if hira in sentence:
        
        return hira
    else:
        return None
   
kata1 = ['カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト']
kata_rendaku1 = ['ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド']

kata2 = ['ハ','ヒ','フ','ヘ','ホ']
kata_rendaku2a = ['バ','ビ','ブ','ベ','ボ']
kata_rendaku2b = ['パ','ピ','プ','ペ','ポ']

kata_rendaku_dict = dict()

for i,k in enumerate(kata1):
    
    kata_rendaku_dict[k] = [kata_rendaku1[i]]
    
for i,k in enumerate(kata2):
    
    kata_rendaku_dict[k] = [kata_rendaku2a[i],kata_rendaku2b[i]]

##############################
hira1 = ['か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と']
hira_rendaku1 = ['が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど']

hira2 = ['は','ひ','ふ','へ','ほ']
hira_rendaku2a = ['ば','び','ぶ','べ','ぼ']
hira_rendaku2b = ['ぱ','ぴ','ぷ','ぺ','ぽ']

hira_rendaku_dict = dict()

for i,k in enumerate(hira1):
    
    hira_rendaku_dict[k] = [hira_rendaku1[i]]
    
for i,k in enumerate(hira2):
    
    hira_rendaku_dict[k] = [hira_rendaku2a[i],hira_rendaku2b[i]]

def getRendakuFuriganaList(isolated_furigana):
    
    """
    Given the furigana of a word in an isolated situation, get the possible
    rendaku furigana list, including the non rendaku version.
    
    Example: ("ふん") ->　["ふん","ぶん","ぷん"]
    """
    
    first_char = isolated_furigana[0]
    
    if first_char in kata_list:
        rendaku_dict = kata_rendaku_dict
    else:
        rendaku_dict = hira_rendaku_dict   

    if first_char in rendaku_dict:
        
        rendaku_chars = rendaku_dict[first_char]
        
        
        from_second_char_string = isolated_furigana[1:]
        
        if len(rendaku_chars) == 1:
            
            rendaku_furigana = rendaku_chars[0] + from_second_char_string
            
            return [isolated_furigana,rendaku_furigana]
        else:
            rendaku_furigana1 = rendaku_chars[0] + from_second_char_string  
            rendaku_furigana2 = rendaku_chars[1] + from_second_char_string  
            
            return [isolated_furigana,rendaku_furigana1,rendaku_furigana2]

    else:
        return [isolated_furigana]
        
        




def getTargetWordFurigana(word,isolated_furigana):
    
    
    
    """
    Get Furigana of one specific word in a sentence given the pronounciation
    of the stem of the word in isolation (including okurigana)
    
    Example: ("水分","ふん") ->　"分"
    
    """
    
    if isolated_furigana[0] in kata_list:
        isolated_furigana_hira = kata2hira(isolated_furigana)
    else:
        isolated_furigana_hira = isolated_furigana
    
    rendaku_furigana_list = getRendakuFuriganaList(isolated_furigana_hira)

    
    all_possible_furigana = rendaku_furigana_list


    
    tagger = MeCab.Tagger()
    foo = tagger.parse(word).split("	")

    hiragana_str = kata2hira(foo[2])

    common_substrings = []
    for r_word in all_possible_furigana:
        

        st = STree.STree([hiragana_str,r_word])
        common_substrings.append(st.lcs())

        

    furigana = max(common_substrings, key=len)
    
    return furigana



def removeOkurigana(kanji_with_okurigana,pronunciation_with_okurigana):
    
    st = STree.STree([kanji_with_okurigana,pronunciation_with_okurigana])
    
    okurigana = st.lcs()
    
    furigana = pronunciation_with_okurigana.replace(okurigana,'')
    
    return furigana

# removed = removeOkurigana("悪い", "わるい")
# print(removed)

# removed = removeOkurigana("悪さ", "わるい")
# print(removed)
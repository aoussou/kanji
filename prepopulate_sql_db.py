#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 02:10:20 2022

@author: ceo
"""


import sqlite3

import os
import numpy as np
import shutil
import json

sqlite3.register_adapter(np.int64, lambda val: int(val))
sqlite3.register_adapter(np.int32, lambda val: int(val))


connection = sqlite3.connect(os.path.join('.','qas.db'))
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
cursor = connection.execute('select * from kankenVoc')
names = list(map(lambda x: x[0], cursor.description))
 
data = json.load(open(os.path.join('.',"kanji_bunka.json")))

# str_ = "INSERT INTO vocabularyQA(%s,%s,%s,%s,%s,%s,%s,%s) VALUES(?,?,?,?,?,?,?,?)" % (
#     names[1],
#     names[2],
#     names[3],
#     names[4],
#     names[5],
#     names[6],
#     names[7],
#     names[8],
#     )

str_ = "INSERT INTO kankenVoc(%s,%s,%s,%s) VALUES(?,?,?,?)" % (
    names[1],
    names[2],
    names[3],
    names[4],
    )



for kanji, entry in data.items():
    
    kyu = entry["kyu"]
    print(kanji,kyu)
    

    # dict_ = entry["kun"]
    dict_ = entry["on"]    
    if dict_ != {}:
        for pronunciation_nbr, examples_list in dict_.items():
    
            for word, pronunciation in examples_list["examples"].items():
            
                    cursor.execute(str_,(
                        word,
                        kanji,
                        pronunciation,
                        kyu,
                        )
                            )
         



# group_id = "SOMATOME_N2_KANJI"
# for key, entry in data.items() :
    
#     print(key)


    
    

    


    
connection.commit()        
connection.close()

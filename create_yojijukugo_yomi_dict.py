import os
import shutil
import pandas as pd
from pathlib import Path

# Access directory from home
home_dir = Path.home()
home_path = os.fspath(home_dir)

subdir_path = os.path.join("dev", "data", "kanken")
data_directory = os.path.join(home_path, subdir_path)
file_name = "yoji_4_kyu"
csv_path = os.path.join(data_directory, file_name + ".csv")
df = pd.read_csv(csv_path)

question_type = "四字熟語・読み"
global_dict = {}

for i, row in df.iterrows():
    local_dict = {}

    local_dict["question"] = row[0]
    local_dict["target"] = row[0]
    local_dict["answer"] = row[1].replace('/', '')
    local_dict["question_type"] = question_type

    global_dict[i] = local_dict

import json

save_path = os.path.join(data_directory, file_name + "_yomi.json")
with open(save_path, 'w') as fp:
    json.dump(global_dict, fp)
fp.close()

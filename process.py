import json
import pypinyin
from pypinyin import pinyin, lazy_pinyin, Style


chengyu2_path = "data/chengyu2.json"
idioms_path = "data/merged_idioms_listed_pinyin.json"

idiom_dict = {}
"格式：{成语: {pinyin: [拼音], frequency: [频率]}}"

with open(chengyu2_path, "r", encoding="utf-8") as f:
    chengyu2 = json.load(f)
with open(idioms_path, "r", encoding="utf-8") as f:
    idioms = json.load(f)
for idiom, pinyin in idioms.items():
    frequency = 0
    for chengyu in chengyu2:
        if idiom == chengyu["word"]:
            frequency = chengyu["frequency"]
            break
    idiom_dict[idiom] = {
        "pinyin": pinyin,
        "frequency": frequency,
    }
with open("data/idioms.json", "w", encoding="utf-8") as f:
    json.dump(idiom_dict, f, ensure_ascii=False, indent=4)

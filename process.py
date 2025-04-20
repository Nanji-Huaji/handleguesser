import json
import pypinyin
from pypinyin import pinyin, lazy_pinyin, Style


def process_idioms(input_file):
    idioms_dict = {}
    # 读取成语文件
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            idiom = line.strip()
            if idiom:
                pronunciation = generate_pronunciation(idiom)
                idioms_dict[idiom] = pronunciation
    return idioms_dict


def generate_pronunciation(idiom):
    pinyin_list = pinyin(idiom, style=Style.TONE3)
    return " ".join([item[0] for item in pinyin_list])


if __name__ == "__main__":
    input_path = "data/idioms.txt"
    output_path = "data/idioms.json"
    dict = process_idioms(input_path)
    print(f"Processed {len(dict)} idioms.")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)

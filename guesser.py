import json
import re
import time


with open("data/idioms.json", "r", encoding="utf-8") as f:
    idioms = json.load(f)

shengmu = [
    "b",
    "p",
    "m",
    "f",  # 双唇音和唇齿音
    "d",
    "t",
    "n",
    "l",  # 舌尖音
    "g",
    "k",
    "h",  # 舌根音
    "j",
    "q",
    "x",  # 舌面音
    "zh",
    "ch",
    "sh",
    "r",  # 卷舌音
    "z",
    "c",
    "s",  # 平舌音
    "y",
    "w",  # 半元音
]

yunmu = [
    "a",
    "o",
    "e",
    "i",
    "u",
    "ü",
    "v",  # 单韵母
    "ai",
    "ei",
    "ao",
    "ou",
    "ia",
    "ie",
    "ua",
    "uo",
    "üe",  # 复韵母
    "ve",
    "an",
    "en",
    "ang",
    "eng",
    "ong",
    "ian",
    "in",
    "iang",
    "ing",
    "uan",
    "un",
    "uang",
    "ueng",
    "üan",
    "ün",  # 鼻韵母
]


def get_yunmu(pinyin: str) -> str:
    global yunmu
    # 优先匹配复韵母，将复韵母放在单韵母之前
    yunmu_sorted = sorted(yunmu, key=len, reverse=True)  # 按长度降序排列
    yunmu_pattern = rf"({'|'.join(yunmu_sorted)})"
    match = re.search(yunmu_pattern, pinyin)
    if match:
        return match.group(0)  # 提取匹配到的韵母
    return None


def get_shengmu(pinyin: str) -> str:
    global shengmu
    shengmu_pattern = rf"^({'|'.join(shengmu)})"
    match = re.match(shengmu_pattern, pinyin)
    if match:
        return match.group(0)  # 提取匹配到的声母
    return None


def get_shengdiao(pinyin: str) -> str:
    shengdiao_pattern = r"\d$"
    match = re.search(shengdiao_pattern, pinyin)
    if match:
        return match.group(0)  # 提取匹配到的声调
    return None


def get_condition(is_exclusive: bool, first_input: str, other_input: str) -> dict:
    first_conditions = first_input.split(",")
    other_conditions = other_input.split(",")

    # 确保 first_conditions 长度为 4，不足时用 None 补足
    while len(first_conditions) < 4:
        first_conditions.append(None)

    return {
        "is_exclusion": is_exclusive,
        "first_conditions": first_conditions,
        "other_conditions": other_conditions,
    }


def input_guess():
    """
    根据用户输入的格式解析条件并返回条件列表。
    格式: [第1字条件, 第2字条件, 第3字条件, 第4字条件], 任意字条件, 任意字条件, 任意字条件
    或者：/[反选第1字条件, 反选第2字条件, 反选第3字条件, 反选第4字条件], 反选任意字条件, 反选任意字条件, 反选任意字条件
    """
    print(
        """    格式:
     [第1字条件, 第2字条件, 第3字条件, 第4字条件], 任意字条件, 任意字条件, 任意字条件
    /[反选第1字条件, 反选第2字条件, 反选第3字条件, 反选第4字条件], 反选任意字条件, 反选任意字条件, 反选任意字条件"""
    )
    user_input = input("请输入条件: ").strip()

    # 判断是否是反选条件
    is_exclusion = user_input.startswith("/")
    if is_exclusion:
        user_input = user_input[1:]  # 去掉开头的 "/"

    # 解析条件
    try:
        parts = user_input.split("],")
        first_part = parts[0].strip("[]")  # 提取第1部分条件
        other_parts = parts[1:]  # 提取其余部分条件

        # 将条件分割为列表
        first_conditions = [cond.strip() for cond in first_part.split(",")]
        other_conditions = [cond.strip() for cond in ",".join(other_parts).split(",")]

        # 返回解析结果
        return {
            "is_exclusion": is_exclusion,
            "first_conditions": first_conditions,
            "other_conditions": other_conditions,
        }
    except Exception as e:
        print(f"输入格式错误: {e}")
        return None


def idiom_filter(condition: dict) -> list:
    """
    根据条件过滤成语列表。
    :param condition: 解析后的条件字典
    :return: 符合条件的成语列表
    """
    global idioms
    # 提取条件
    is_exclusion = condition["is_exclusion"]
    first_conditions = condition["first_conditions"]
    other_conditions = condition["other_conditions"]

    filtered_idioms = []

    # 正选条件处理
    if not is_exclusion:
        for idiom, idiom_value in idioms.items():
            # 判断是否满足第1字到第4字的条件
            match_first = True
            for i in range(4):
                if first_conditions == ["", "", "", ""] or first_conditions == [None, None, None, None]:
                    break
                condition = first_conditions[i]
                if condition:
                    # 如果条件是一个汉字
                    if re.match(r"[\u4e00-\u9fff]", condition):
                        if idiom[i] != condition:
                            match_first = False
                            break
                    # 如果条件是拼音
                    if not re.match(r"[\u4e00-\u9fff]", condition):
                        # 匹配声调
                        if condition[-1].isdigit():
                            if get_shengdiao(idiom_value["pinyin"][i]) != condition[-1]:
                                match_first = False
                                break
                        # 匹配声母
                        if get_shengmu(condition):
                            if get_shengmu(condition) != get_shengmu(idiom_value["pinyin"][i]):
                                match_first = False
                                break
                        # 匹配韵母
                        if get_yunmu(condition):
                            if get_yunmu(condition) != get_yunmu(idiom_value["pinyin"][i]):
                                match_first = False
                                break
            # 判断是否满足其它条件
            if match_first:
                match_other = True
                for condition in other_conditions:
                    # 如果是汉字
                    if re.match(r"[\u4e00-\u9fff]", condition):
                        if condition not in idiom:
                            match_other = False
                            break
                    else:
                        # 如果是拼音
                        if not any(condition in pinyin for pinyin in idiom_value["pinyin"]):
                            match_other = False
                            break
                if match_other:
                    # 如果满足条件，就添加到结果列表
                    filtered_idioms.append({idiom: idiom_value["frequency"]})
    else:
        # 排除条件处理
        for idiom, idiom_value in idioms.items():
            # 判断是否满足第1字到第4字的排除条件
            match_first = False
            for i in range(4):
                if first_conditions == ["", "", "", ""] or first_conditions == [None, None, None, None]:
                    break
                condition = first_conditions[i]
                if condition:
                    # 如果条件是一个汉字
                    if re.match(r"[\u4e00-\u9fff]", condition):
                        if idiom[i] == condition:
                            match_first = True
                            break
                    # 如果条件是拼音
                    if not re.match(r"[\u4e00-\u9fff]", condition):
                        # 匹配声调
                        if condition[-1].isdigit():
                            if get_shengdiao(idiom_value["pinyin"][i]) == condition[-1]:
                                match_first = True
                                break
                        # 匹配声母
                        if get_shengmu(condition):
                            if get_shengmu(condition) == get_shengmu(idiom_value["pinyin"][i]):
                                match_first = True
                                break
                        # 匹配韵母
                        if get_yunmu(condition):
                            if get_yunmu(condition) == get_yunmu(idiom_value["pinyin"][i]):
                                match_first = True
                                break

            # 判断是否满足其它排除条件
            if match_first:
                match_other = False
                for condition in other_conditions:
                    # 如果是汉字
                    if re.match(r"[\u4e00-\u9fff]", condition):
                        if condition in idiom:
                            match_other = True
                            break
                    else:
                        # 如果是拼音
                        if any(condition in pinyin for pinyin in idiom_value["pinyin"]):
                            match_other = True
                            break
                if match_other:
                    continue  # 如果满足排除条件，则跳过当前成语，不将其加入结果
            # 如果该成语没有满足排除条件，就添加到结果列表
            filtered_idioms.append({idiom: idiom_value["frequency"]})
    # 对结果进行排序
    filtered_idioms.sort(key=lambda x: list(x.values())[0], reverse=True)
    # 只保留成语名称
    filtered_idioms = [list(item.keys())[0] for item in filtered_idioms]

    return filtered_idioms


def joint_idiom_filter(inclusive_condition, exclusive_condition):
    if inclusive_condition["first_conditions"] and inclusive_condition["other_conditions"] is None:
        return idiom_filter(exclusive_condition)
    if exclusive_condition["first_conditions"] and exclusive_condition["other_conditions"] is None:
        return idiom_filter(inclusive_condition)
    inclusive_condition = idiom_filter(inclusive_condition)
    exclusive_condition = idiom_filter(exclusive_condition)
    # 取交集
    result = list(set(inclusive_condition) & set(exclusive_condition))
    # 对结果进行排序
    result.sort(key=lambda x: idioms[x]["frequency"], reverse=True)
    return result


if __name__ == "__main__":
    condition = {
        "is_exclusion": False,
        "first_conditions": ["long2", "", "", ""],
        "other_conditions": [],
    }
    result = idiom_filter(condition)
    print(result)

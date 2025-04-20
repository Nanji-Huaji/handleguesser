import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="什么是Handle")

st.sidebar.title("Handle Guesser")
st.sidebar.markdown(
    """
南极滑稽制作

[GitHub](https://github.com/Nanji-Huaji)

[博客](https://blog.nanjihuaji.top/)
"""
)

st.markdown("# 汉兜 - 汉字 Wordle 游戏")
st.write("原始GitHub仓库：https://github.com/antfu/handle")
st.markdown(
    """
![Handle](https://github.com/antfu/handle/raw/main/public/og.png)
    
汉兜是一款基于汉字的Wordle游戏，玩家需要在十次机会内猜出一个四字词语。每次猜测后，游戏会通过颜色提示玩家猜测的正确性。

## 游戏规则

- 你有十次的机会猜一个四字词语。
- 每次猜测后，汉字与拼音的颜色将会标识其与正确答案的区别。

### 颜色提示说明

- **绿色**：表示该字出现在答案中且位置正确。
- **橙色**：表示该字出现在答案中，但位置不正确。

### 字母颜色提示说明

- 每个格子中的汉字、声母、韵母、声调都会独立进行颜色的指示。
- 例如，第一个字“巧”为灰色，而其声母“Q”与韵母“iao”均为青色，代表该位置的正确答案为其同音字但非“巧”字本身。
- 同理，第二个字中韵母“uo”为橙色，代表其韵母出现在四个字之中，但非位居第二。以此类推。
![例子](https://blog.nanjihuaji.top/wp-content/uploads/2025/04/instance.png)

当四个格子都为青色时，你便赢得了游戏！

![好运](https://blog.nanjihuaji.top/wp-content/uploads/2025/04/goodluck.png)
"""
)

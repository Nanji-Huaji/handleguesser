import jieba
import json
import guesser
import streamlit as st

# Set the page configuration

st.set_page_config(
    page_title="Handle Guesser",
    # layout="wide",
)

# Set the title and description

st.title("Handle Guesser")

# 功能区

warn_placeholder = st.empty()

st.markdown("## 正选条件")

inclusive_condition = st.text_input(
    "位置条件：第一字条件,第二字条件,第三字条件,第四字条件（以英文逗号','分隔）", key="inclusive_condition", value=""
)
inclusive_other_condition = st.text_input(
    "其他正选条件：其他条件一,其他条件二,其他条件三（以英文逗号','分隔）", key="inclusive_other_condition", value=""
)

st.markdown("## 排除条件")
exclusive_condition = st.text_input(
    "位置条件：第一字条件,第二字条件,第三字条件,第四字条件（以英文逗号','分隔）", key="exclusive_condition", value=""
)
exclusive_other_condition = st.text_input(
    "其他排除条件：其他条件一,其他条件二，其他条件三（以英文逗号','分隔）", key="exclusive_other_condition", value=""
)

search = st.button("筛选")

if search:
    try:
        if (
            inclusive_condition == ""
            and exclusive_condition == ""
            and inclusive_other_condition == ""
            and exclusive_other_condition == ""
        ):
            warn_placeholder.warning("请输入条件")
        else:
            inclusive_condition = guesser.get_condition(False, inclusive_condition, inclusive_other_condition)
            exclusive_condition = guesser.get_condition(True, exclusive_condition, exclusive_other_condition)
            result = guesser.joint_idiom_filter(inclusive_condition, exclusive_condition)
            if result:
                st.markdown("## 筛选结果")
                for idiom in result:
                    st.write(idiom)
            else:
                warn_placeholder.warning("没有符合条件的成语")
    except Exception as e:
        warn_placeholder.warning("发生错误，请检查输入条件")
        print(e)
        st.markdown("## 错误信息")
        st.write(e)

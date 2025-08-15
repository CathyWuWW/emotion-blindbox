""""
import streamlit as st
import random

# ------------------ 情绪留言数据 ------------------
mood_dict = {
    "开心": [
        "真希望和你在一起，能看到你的笑~",
        "如果感到幸福你就拍拍手！或者微信拍拍我！",
        "能让你感到开心的人和事，也会令我开心"
    ],
    "难过": [
        "哦亲爱的，不管是什么事情，请相信它是一时的，而时间是流动的，我们自身也是，我们不会被难过的情绪固定住。",
        "感到难过的时候，我也想为你分担，你可以说暗号：”……“，我速速来"
    ],
    "幸福": [
        "希望我爱的人一直幸福，笑口常开~"
    ]
}

# ------------------ 页面配置 ------------------
st.set_page_config(page_title="情绪盲盒", layout="centered")

st.title("🎁 情绪盲盒：专属于你的心情留言")
st.write("点击下面的心情按钮，看看七七为你准备了什么小惊喜吧～")

# ------------------ 状态初始化 ------------------
if "shown_messages" not in st.session_state:
    st.session_state.shown_messages = {k: [] for k in mood_dict}

# ------------------ 情绪按钮 ------------------
cols = st.columns(len(mood_dict))
selected_mood = None
for i, mood in enumerate(mood_dict.keys()):
    if cols[i].button(mood):
        selected_mood = mood

# ------------------ 展示留言 ------------------
if selected_mood:
    all_msgs = mood_dict[selected_mood]
    shown = st.session_state.shown_messages[selected_mood]
    remaining = list(set(all_msgs) - set(shown))

    if not remaining:
        st.info(f"所有「{selected_mood}」留言都展示过啦！")
    else:
        msg = random.choice(remaining)
        shown.append(msg)
        st.success(f"💌 来自「{selected_mood}」盲盒：")
        st.write(f"> {msg}")

# ------------------ 展示已出现留言 ------------------
st.markdown("---")
st.header("📝 已展示留言")
for mood, msgs in st.session_state.shown_messages.items():
    if msgs:
        st.subheader(f"💖 {mood}")
        for m in msgs:
            st.write(f"- {m}")
"""
import streamlit as st
import random

# 情绪留言内容
mood_dict = {
    "开心": [
        "真希望和你在一起，能看到你的笑~",
        "如果感到幸福你就拍拍手！或者微信拍拍我！",
        "能让你感到开心的人和事，也会令我开心"
    ],
    "难过": [
        "哦亲爱的，不管是什么事情，请相信它是一时的。",
        "感到难过的时候，我也想为你分担，你可以说暗号：”……“，我速速来"
    ],
    "幸福": [
        "希望我爱的人一直幸福，笑口常开~"
    ]
}

# 初始化展示记录 & 当前页面
if "shown_messages" not in st.session_state:
    st.session_state.shown_messages = {k: [] for k in mood_dict}
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_mood" not in st.session_state:
    st.session_state.current_mood = None

# 页面：情绪选择
def show_home():
    st.title("🎁 情绪盲盒")
    st.write("点击一个情绪按钮，打开专属盲盒吧～")
    cols = st.columns(len(mood_dict))
    for i, mood in enumerate(mood_dict.keys()):
        if cols[i].button(mood):
            st.session_state.current_mood = mood
            st.session_state.page = "mood"

# 页面：某种情绪下
def show_mood_page():
    mood = st.session_state.current_mood
    st.markdown(f"### 💌 {mood}盲盒")
    
    # 返回按钮
    if st.button("← 返回情绪选择"):
        st.session_state.page = "home"
        return

    # 抽一句未展示过的
    all_msgs = mood_dict[mood]
    shown = st.session_state.shown_messages[mood]
    remaining = list(set(all_msgs) - set(shown))

    if remaining:
        if st.button("打开一条新留言"):
            msg = random.choice(remaining)
            shown.append(msg)
            st.success("💬 新留言：")
            st.write(f"> {msg}")
    else:
        st.info("所有留言都展示过啦 🎉")

    # 展示已读留言
    if shown:
        st.markdown("#### 📝 已展示留言")
        for m in shown:
            st.write(f"- {m}")

# 页面路由控制
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "mood":
    show_mood_page()

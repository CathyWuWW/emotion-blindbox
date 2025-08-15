# emotion_blindbox.py
import streamlit as st
import random
import json
import os
import pandas as pd
from collections import defaultdict

# ---------- 动态读取 Excel 数据 ----------
def load_mood_dict(excel_file="mood.xlsx"):
    df = pd.read_excel(excel_file)
    df.columns = ["emotion", "message"]
    mood_dict = defaultdict(list)
    for _, row in df.iterrows():
        mood_dict[row["emotion"]].append(str(row["message"]))
    return dict(mood_dict)

mood_dict = load_mood_dict()

# ---------- 保存与读取展示记录 ----------
SAVE_FILE = "shown.json"

def load_shown():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {k: [] for k in mood_dict}

def save_shown(shown_dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(shown_dict, f, ensure_ascii=False, indent=2)

# ---------- 情绪 emoji 映射 ----------
EMOJI_MAP = {
        "开心": "😄",
        "难过": "😢",
        "幸福": "💖",
        "生气": "😠",
        "感动": "🥹",
        "想念": "🌙"
}

# ---------- 初始化状态 ----------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_mood" not in st.session_state:
    st.session_state.current_mood = None
if "shown_messages" not in st.session_state:
    st.session_state.shown_messages = load_shown()
# ---------- 页面背景渐变样式 ----------
def set_background_gradient():
    st.markdown(
        """
        <style>
        html, body, .stApp {
            background: linear-gradient(to bottom right, #fef6f9, #f0faff);
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_background_gradient()

# ---------- 自定义展示新留言 ----------
def display_new_message(message, mood):
    emoji = EMOJI_MAP.get(mood, "💬")
    st.markdown(
        f"""
        <div style="background-color:#fff9e6;padding:20px 25px;border-radius:12px;margin-top:15px;">
            <span style="font-size:18px;font-weight:bold;color:#000;">{emoji}：</strong></span><br><br>
            <blockquote style="font-size:17px;color:#000;font-weight:bold;border-left:4px solid #ffe082;padding-left:12px;">
                {message}
            </blockquote>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- 页面：情绪选择 ----------
def show_home():
    st.title("🎁 情绪盲盒")
    st.write("Dear you: 请选择你现在的心情，让我不在你身边时，也能够像一直陪伴着你一样~")

    moods = list(mood_dict.keys())
    rows = len(moods) // 3 + int(len(moods) % 3 != 0)
    for i in range(rows):
        cols = st.columns(3)
        for j in range(3):
            idx = i * 3 + j
            if idx < len(moods):
                mood = moods[idx]
                if cols[j].button(mood):
                    st.session_state.current_mood = mood
                    st.session_state.page = "mood"

# ---------- 页面：展示留言 ----------
def show_mood_page():
    mood = st.session_state.current_mood
    st.markdown(f"### 💌 {mood}盲盒")

    if st.button("← 返回情绪选择"):
        st.session_state.page = "home"
        return

    all_msgs = mood_dict[mood]
    shown = st.session_state.shown_messages.get(mood, [])
    remaining = list(set(all_msgs) - set(shown))

    new_msg = None
    if remaining and st.button("打开一条新留言"):
        new_msg = random.choice(remaining)
        shown.append(new_msg)
        st.session_state.shown_messages[mood] = shown
        save_shown(st.session_state.shown_messages)

    if new_msg:
        display_new_message(new_msg, mood)
    elif not remaining:
        st.info("所有留言都展示过啦 🎉，戳戳wyn更新嘻嘻")

    if shown:
        st.markdown("#### 📝 已展示留言")
        for m in shown:
            st.write(f"- {m}")

# ---------- 页面控制 ----------
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "mood":
    show_mood_page()

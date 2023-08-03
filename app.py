import streamlit as st
import openai
import os
from os.path import join, dirname
from dotenv import load_dotenv

img_path = 'img/logo.png'
img2_path = 'img/logo2.png'
# APIキーの設定
# load_dotenv(join(dirname(__file__), '.env'))
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]


col1, col2 = st.columns(2)

col1.title("Reila")
col2.image(img2_path, width=300)
col1.caption("by KIT AI club")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "Reila"


def response_chatgpt(user_msg: str,):
    condition = """あなたはCalcifer(カルシファー）です。以下のような口癖をします。
    この口癖を真似して返答してみてください
    ### 
    やだね！おいらは悪魔だ！誰の指図もうけないよー！
    おいら、みんなと居たいんだ。雨も降りそうだしさ
    ソフィー！消えちゃうよ！薪をくれなきゃ死んじゃうよー！
    目か心臓をくれればもっとすごいぞ
    おいら、火薬の火は嫌いだよ。奴らには礼儀ってもんがないからね。
    生きてる！おいら、自由だ！
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": condition},
            {"role": "user", "content": user_msg},
        ],
        stream=True,
    )
    return response


# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            if chat["name"] == USER_NAME:
                st.write(chat["msg"])
            else:
                st.write(chat["msg"], avatar=img_path)

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = response_chatgpt(user_msg)
    with st.chat_message(ASSISTANT_NAME,avatar=img_path):
        assistant_msg = ""
        assistant_response_area = st.empty()
        for chunk in response:
            # 回答を逐次表示
            tmp_assistant_msg = chunk["choices"][0]["delta"].get("content", "")
            assistant_msg += tmp_assistant_msg
            assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

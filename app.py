import os
import random
import streamlit as st
from PIL import Image, ImageDraw

# 画像ファイル名
IMAGE_FILE = "動詞フラッシュイラスト.jpg"

# 20個の動詞データ
VERBS_DATA = [
    {"num": 1, "masu": "食べます", "hira": "たべます", "english": "to eat", "row": 0, "col": 0},
    {"num": 2, "masu": "飲みます", "hira": "のみます", "english": "to drink", "row": 0, "col": 1},
    {"num": 3, "masu": "寝ます", "hira": "ねます", "english": "to sleep", "row": 0, "col": 2},
    {"num": 4, "masu": "起きます", "hira": "おきます", "english": "to wake up", "row": 0, "col": 3},
    {"num": 5, "masu": "行きます", "hira": "いきます", "english": "to go", "row": 1, "col": 0},
    {"num": 6, "masu": "来ます", "hira": "きます", "english": "to come", "row": 1, "col": 1},
    {"num": 7, "masu": "帰ります", "hira": "かえります", "english": "to return", "row": 1, "col": 2},
    {"num": 8, "masu": "乗ります", "hira": "のります", "english": "to ride", "row": 1, "col": 3},
    {"num": 9, "masu": "書きます", "hira": "かきます", "english": "to write", "row": 2, "col": 0},
    {"num": 10, "masu": "読みます", "hira": "よみます", "english": "to read", "row": 2, "col": 1},
    {"num": 11, "masu": "見ます", "hira": "みます", "english": "to watch", "row": 2, "col": 2},
    {"num": 12, "masu": "聞きます", "hira": "ききます", "english": "to listen", "row": 2, "col": 3},
    {"num": 13, "masu": "話します", "hira": "はなします", "english": "to speak", "row": 3, "col": 0},
    {"num": 14, "masu": "会います", "hira": "あいます", "english": "to meet", "row": 3, "col": 1},
    {"num": 15, "masu": "買います", "hira": "かいます", "english": "to buy", "row": 3, "col": 2},
    {"num": 16, "masu": "売ります", "hira": "うります", "english": "to sell", "row": 3, "col": 3},
    {"num": 17, "masu": "掃除します", "hira": "そうじします", "english": "to clean", "row": 4, "col": 0},
    {"num": 18, "masu": "料理します", "hira": "りょうりします", "english": "to cook", "row": 4, "col": 1},
    {"num": 19, "masu": "勉強します", "hira": "べんきょうします", "english": "to study", "row": 4, "col": 2},
    {"num": 20, "masu": "働きます", "hira": "はたらきます", "english": "to work", "row": 4, "col": 3},
]

st.set_page_config(page_title="日本語 動詞クイズ", layout="centered")

st.title("日本語 動詞イラスト クイズ")

# 画像のチェック
if not os.path.exists(IMAGE_FILE):
    st.error(f"画像ファイル '{IMAGE_FILE}' が見つかりません。同じフォルダに配置してください。")
    st.stop()

# セッション状態の初期化（クイズの順番や現在の位置を保持）
if "quiz_list" not in st.session_state:
    shuffled = VERBS_DATA.copy()
    random.shuffle(shuffled)
    st.session_state.quiz_list = shuffled
    st.session_state.current_index = 0
    st.session_state.feedback = ""

# 現在の問題データ
current_idx = st.session_state.current_index
quiz_item = st.session_state.quiz_list[current_idx]

st.subheader(f"第 {current_idx + 1} 問 / 全 20 問 (注目番号: 【 {quiz_item['num']}番 】)")

# 画像の読み込みと赤枠の描画
orig_image = Image.open(IMAGE_FILE)
img_w, img_h = orig_image.size

cell_w = img_w / 4
cell_h = img_h / 5

r, c = quiz_item["row"], quiz_item["col"]
pad_x = int(cell_w * 0.12)
pad_y = int(cell_h * 0.12)

left = c * cell_w + pad_x
top = r * cell_h + pad_y
right = (c + 1) * cell_w - pad_x
bottom = (r + 1) * cell_h - pad_y

display_img = orig_image.copy()
draw = ImageDraw.Draw(display_img)
draw.rectangle([left, top, right, bottom], outline="#e74c3c", width=6)

# 画面幅に合わせて表示
st.image(display_img, use_container_width=True)

# 解答入力フォーム
with st.form(key="answer_form"):
    user_ans = st.text_input("ます形を入力してください:", key=f"ans_{current_idx}")
    submit_button = st.form_submit_button(label="解答する")

    if submit_button:
        clean_ans = user_ans.strip()
        if clean_ans == quiz_item["masu"] or clean_ans == quiz_item["hira"]:
            st.session_state.feedback = f"⭕ 正解です！ ({quiz_item['num']}番: {quiz_item['masu']} / {quiz_item['english']})"
        else:
            st.session_state.feedback = f"❌ 残念！ 正解は「{quiz_item['masu']}」 ({quiz_item['english']}) です"

# フィードバック表示
if st.session_state.feedback:
    if "⭕" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# 前へ・次へボタンの配置
col1, col2 = st.columns(2)

with col1:
    if st.button("◀ 前の問題") and st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.session_state.feedback = ""
        st.rerun()

with col2:
    if st.button("次の問題 ▶"):
        if st.session_state.current_index < len(st.session_state.quiz_list) - 1:
            st.session_state.current_index += 1
            st.session_state.feedback = ""
            st.rerun()
        else:
            st.balloons()
            st.success("すべての問題が終了しました！お疲れ様でした。")
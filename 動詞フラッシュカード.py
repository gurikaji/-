import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import random

# 画像ファイル名（ご自身の環境のファイル名に合わせて変更してください）
IMAGE_FILE = "動詞フラッシュイラスト.jpg"

# 20個の動詞データ（ます形、ひらがな表記、画像内のグリッド位置）
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

class VerbGridQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("日本語 動詞クイズ（スクロール対応）")
        self.root.geometry("540x720")
        self.root.configure(bg="#f8f9fa")

        # 問題の順番をランダムにシャッフル
        self.quiz_list = VERBS_DATA.copy()
        random.shuffle(self.quiz_list)
        
        self.current_index = 0
        self.display_width = 400  # 初期表示の画像幅

        # 画像読み込みチェック
        if not os.path.exists(IMAGE_FILE):
            messagebox.showerror("エラー", f"画像ファイル '{IMAGE_FILE}' が見つかりません。\n同じフォルダに配置してください。")
            self.root.destroy()
            return

        self.orig_image = Image.open(IMAGE_FILE)
        
        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        # タイトル・問題番号
        self.title_label = tk.Label(self.root, text="動詞イラスト クイズ", font=("Meiryo", 14, "bold"), bg="#f8f9fa", fg="#2c3e50")
        self.title_label.pack(pady=2)

        self.progress_label = tk.Label(self.root, text="", font=("Meiryo", 11, "bold"), bg="#f8f9fa", fg="#2980b9")
        self.progress_label.pack(pady=2)

        # 拡大・縮小ボタンエリア
        zoom_frame = tk.Frame(self.root, bg="#f8f9fa")
        zoom_frame.pack(pady=2)

        self.zoom_out_btn = tk.Button(zoom_frame, text=" ➖ 縮小 ", font=("Meiryo", 9), bg="#bdc3c7", fg="#2c3e50", command=self.zoom_out)
        self.zoom_out_btn.grid(row=0, column=0, padx=5)

        self.zoom_in_btn = tk.Button(zoom_frame, text=" ➕ 拡大 ", font=("Meiryo", 9), bg="#bdc3c7", fg="#2c3e50", command=self.zoom_in)
        self.zoom_in_btn.grid(row=0, column=1, padx=5)

        # スクロール 가능한 画像表示エリア（Canvas ＋ スクロールバー）
        frame_canvas = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        frame_canvas.pack(pady=5)

        self.canvas = tk.Canvas(frame_canvas, width=420, height=340, bg="#ffffff", highlightthickness=0)
        
        v_bar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        h_bar = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)

        v_bar.pack(side=tk.RIGHT, fill=tk.Y)
        h_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # マウスドラッグで画像を動かせる機能
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)

        # 入力エリア
        input_frame = tk.Frame(self.root, bg="#f8f9fa")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="ます形を入力:", font=("Meiryo", 11), bg="#f8f9fa").pack(side=tk.LEFT, padx=3)
        
        self.entry = tk.Entry(input_frame, font=("Meiryo", 12), width=12)
        self.entry.pack(side=tk.LEFT, padx=3)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        self.submit_btn = tk.Button(input_frame, text="解答", font=("Meiryo", 10, "bold"), bg="#3498db", fg="white", command=self.check_answer)
        self.submit_btn.pack(side=tk.LEFT, padx=3)

        # 正解・不正解のフィードバック表示
        self.feedback_label = tk.Label(self.root, text="", font=("Meiryo", 12, "bold"), bg="#f8f9fa")
        self.feedback_label.pack(pady=2)

        # 前へ・次へボタン
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=5)

        self.prev_btn = tk.Button(btn_frame, text="◀ 前の問題", font=("Meiryo", 10), width=10, bg="#95a5a6", fg="white", command=self.prev_question)
        self.prev_btn.grid(row=0, column=0, padx=8)

        self.next_btn = tk.Button(btn_frame, text="次の問題 ▶", font=("Meiryo", 10), width=10, bg="#2ecc71", fg="white", command=self.next_question)
        self.next_btn.grid(row=0, column=1, padx=8)

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def show_question(self):
        item = self.quiz_list[self.current_index]
        
        # 進捗と問題番号の更新
        self.progress_label.config(text=f"第 {self.current_index + 1} 問 / 全 20 問 (注目番号: 【 {item['num']}番 】)")

        display_img = self.orig_image.copy()
        img_w, img_h = display_img.size

        cell_w = img_w / 4
        cell_h = img_h / 5

        r, c = item["row"], item["col"]
        
        # ★赤枠を小さくするため、パディング（内側の余白）を大きめに設定しました（左右15px、上下15pxなど）
        pad_x = int(cell_w * 0.12)
        pad_y = int(cell_h * 0.12)
        
        left = c * cell_w + pad_x
        top = r * cell_h + pad_y
        right = (c + 1) * cell_w - pad_x
        bottom = (r + 1) * cell_h - pad_y

        # 赤い枠線を描画（太さも少しすっきりさせるため 4px に調整）
        draw = ImageDraw.Draw(display_img)
        draw.rectangle([left, top, right, bottom], outline="#e74c3c", width=4)

        # リサイズして表示
        scale = self.display_width / img_w
        display_h = int(img_h * scale)
        resized_img = display_img.resize((self.display_width, display_h), Image.Resampling.LANCZOS)
        
        self.tk_image = ImageTk.PhotoImage(resized_img)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=(0, 0, self.display_width, display_h))

        # 注目している赤枠の位置へ自動スクロール
        target_x = (left / img_w) * self.display_width
        target_y = (top / img_h) * display_h
        self.canvas.xview_moveto(max(0, (target_x - 150) / self.display_width))
        self.canvas.yview_moveto(max(0, (target_y - 120) / display_h))

        # 入力欄クリアとフィードバックリセット
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.entry.focus()

    def check_answer(self):
        item = self.quiz_list[self.current_index]
        user_ans = self.entry.get().strip()

        if not user_ans:
            return

        if user_ans == item["masu"] or user_ans == item["hira"]:
            self.feedback_label.config(text=f"⭕ 正解です！ ({item['num']}番: {item['masu']})", fg="#27ae60")
        else:
            self.feedback_label.config(text=f"❌ 残念！ 正解は「{item['masu']}」です", fg="#e74c3c")

    def zoom_in(self):
        if self.display_width < 700:
            self.display_width += 80
            self.show_question()

    def zoom_out(self):
        if self.display_width > 250:
            self.display_width -= 80
            self.show_question()

    def next_question(self):
        if self.current_index < len(self.quiz_list) - 1:
            self.current_index += 1
            self.show_question()
        else:
            messagebox.showinfo("終了", "すべての問題が終了しました！お疲れ様でした。")

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = VerbGridQuizGUI(root)
    root.mainloop()

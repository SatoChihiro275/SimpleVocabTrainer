import csv
import tkinter as tk
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 日本語フォントの設定（matplotlibの日本語バグ抑制のため）
mpl.rcParams['font.family'] = 'Meiryo'

# グローバル変数として選択されたカテゴリの単語リストを保持
selected_category_words = []

############ CSVファイルから単語を読み込み、リストとして返す関数 ############
def load_words(filename):
    words = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                words[row[0]] = row[1]  # 単語とその意味を辞書に格納
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filename}")
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
    return words

############ モード選択画面の表示 ############
def start_mode_selection(root, words, mastery_levels):
    selection_frame = tk.Frame(root)
    selection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Button(selection_frame, text="単語暗記モード", height=3, width=20, command=lambda: start_learning_mode(root, words, mastery_levels)).pack(pady=10)
    tk.Button(selection_frame, text="単語テストモード", height=3, width=20, command=lambda: start_test_mode(root, words, mastery_levels)).pack(pady=10)

    selection_frame.pack()

############ 単語暗記モードを開始する関数 ############
def start_learning_mode(root, words, mastery_levels):
    # モード選択画面をクリア
    for widget in root.winfo_children():
        widget.destroy()

    # 単語リスト選択ボタン（画面上部）
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    for level in ["全て", "未学習", "学習中", "習得済み"]:
        btn = tk.Button(btn_frame, text=f"{level} ({count_words(mastery_levels, level)})", command=lambda l=level: display_words(words, mastery_levels, word_label, meaning_label, l))
        btn.pack(side=tk.LEFT)

    # 単語を表示するフレーム
    learning_frame = tk.Frame(root)
    learning_frame.pack(pady=20)

    # 単語と意味を表示するラベル
    word_label = tk.Label(learning_frame, text="", font=("Helvetica", 16))
    word_label.pack(pady=10)

    meaning_label = tk.Label(learning_frame, text="", font=("Helvetica", 16))
    meaning_label.pack(pady=10)

    # 次の単語を表示するボタン
    next_word_button = tk.Button(root, text="次の単語", command=lambda: display_next_word(words, mastery_levels, word_label, meaning_label))
    next_word_button.pack(pady=10)

    # 最初に全ての単語を表示
    display_words(words, mastery_levels, word_label, meaning_label, "全て")


############ 単語テストモードを開始する関数 ############
def start_test_mode(root, words, mastery_levels):
    pass

############ 特定のカテゴリの単語を表示する関数 ############
def display_words(words, mastery_levels, word_label, meaning_label, level):
    global selected_category_words
    selected_category_words = [word for word, lvl in mastery_levels.items() if lvl == level_to_num(level) or level == "全て"]
    if not selected_category_words:
        word_label.config(text="単語がありません")
        meaning_label.config(text="")
    else:
        word_label.config(text=selected_category_words[0])
        meaning_label.config(text=words[selected_category_words[0]])

def level_to_num(level):
    return {"全て": None, "未学習": 0, "学習中": 1, "習得済み": 2}[level]

############ 特定の習熟度レベルの単語数を数える関数 ############
def count_words(mastery_levels, level):
    if level == "全て":
        return len(mastery_levels)
    else:
        level_num = level_to_num(level)
        return sum(1 for lvl in mastery_levels.values() if lvl == level_num)
    
############ 次の単語を表示する関数 ############
def display_next_word(words, mastery_levels, word_label, meaning_label):
    global selected_category_words
    current_word = word_label.cget("text")

    # 現在の単語のインデックスを見つけ、次の単語を探す
    if current_word in selected_category_words:
        current_index = selected_category_words.index(current_word)
        next_index = (current_index + 1) % len(selected_category_words)
        next_word = selected_category_words[next_index]
        word_label.config(text=next_word)
        meaning_label.config(text=words[next_word])
    else:
        word_label.config(text="単語がありません")
        meaning_label.config(text="")


############ メイン関数 ############
def main():
    root = tk.Tk()
    root.title("単語帳アプリ")
    root.geometry("500x400")

    words = load_words("words.csv")
    mastery_levels = {word: 0 for word in words}  # 各単語の習熟度を初期化

    start_mode_selection(root, words, mastery_levels)

    root.mainloop()

if __name__ == "__main__":
    main()

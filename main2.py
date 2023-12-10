import csv
import tkinter as tk
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 日本語フォントの設定（matplotlibの日本語バグ抑制のため）
mpl.rcParams['font.family'] = 'Meiryo'

# カテゴリとそのカテゴリ内の現在のインデックスを追跡するグローバル変数
current_category = "全て"
current_index = 0

########## ユーティリティ関数 ##########
# CSVファイルから単語リストと習熟度を読み込む関数
def load_words(filename):
    words = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                word, meaning, mastery_level = row
                words[word] = {'meaning': meaning, 'mastery_level': int(mastery_level)}
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filename}")
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
    return words

# 単語リストと習熟度をCSVファイルに保存する関数
def save_words(filename, words):
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for word, info in words.items():
                writer.writerow([word, info['meaning'], info['mastery_level']])
    except Exception as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")

# カテゴリを習熟度レベルの数値に変換するヘルパー関数
def category_to_num(category):
    return {"全て": None, "未学習": 0, "学習中": 1, "習得済み": 2}.get(category, None)

########## コア機能の関数 ##########
# モード選択画面を表示する関数
def start_mode_selection(root, words):
    # 既存のウィジェットをクリア
    for widget in root.winfo_children():
        widget.destroy()

    # モード選択ボタンを配置するフレーム
    selection_frame = tk.Frame(root)
    selection_frame.pack(expand=True)

    # 「単語暗記モード」選択ボタン
    tk.Button(selection_frame, text="単語暗記モード", height=3, width=20, 
              command=lambda: start_learning_mode(root, words)).pack(pady=10)

    # 「単語テストモード」選択ボタン
    tk.Button(selection_frame, text="単語テストモード", height=3, width=20, 
              command=lambda: start_test_mode(root, words)).pack(pady=10)

    selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

########## UI操作の関数 ##########
# 単語暗記モードを開始する関数
def start_learning_mode(root, words):
    # 既存のウィジェットをクリア
    for widget in root.winfo_children():
        widget.destroy()

    # 単語リスト選択ボタン（画面上部）
    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.TOP, fill=tk.X)

    # 単語と意味を表示するフレーム
    learning_frame = tk.Frame(root)
    learning_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 単語と意味を表示するラベル
    word_label = tk.Label(learning_frame, text="", font=("Helvetica", 16))
    word_label.pack(pady=10)

    meaning_label = tk.Label(learning_frame, text="", font=("Helvetica", 14))
    meaning_label.pack(pady=5)

    # 習熟度ボタンとその機能
    buttons = ["全て", "未学習", "学習中", "習得済み"]
    for level in buttons:
        btn = tk.Button(btn_frame, text=f"{level} ({count_words(words, level)})", height=2, width=15,
                        command=lambda l=level: display_words(words, word_label, meaning_label, l))
        btn.pack(side=tk.LEFT, padx=10)

    # 次の単語を表示するボタン
    next_word_frame = tk.Frame(root)
    next_word_frame.pack(side=tk.BOTTOM, pady=10)

    next_word_button = tk.Button(next_word_frame, text="次の単語", height=2, width=20,
                                 command=lambda: display_next_word(words, word_label, meaning_label))
    next_word_button.pack()

    # モード選択に戻るボタン
    back_button = tk.Button(next_word_frame, text="モード選択に戻る", height=2, width=20,
                            command=lambda: start_mode_selection(root, words))
    back_button.pack(side=tk.BOTTOM, pady=10)

    # 最初の単語を表示
    display_words(words, word_label, meaning_label, "全て")

# 単語テストモードを開始する関数
def start_test_mode(root, words):
    pass

########## イベントハンドラー関数 ##########
# 特定のカテゴリの単語を表示する関数
def display_words(words, word_label, meaning_label, category):
    global current_category, current_index
    current_category = category  # 現在のカテゴリを設定
    current_index = 0  # カテゴリが変更されたときにインデックスをリセット

    # 選択したカテゴリに基づいて単語をフィルターする
    filtered_words = [word for word, info in words.items() if category_to_num(category) == info['mastery_level'] or category == "全て"]

    if filtered_words:
        word_label.config(text=filtered_words[current_index])
        meaning_label.config(text=words[filtered_words[current_index]]['meaning'])
    else:
        word_label.config(text="単語がありません")
        meaning_label.config(text="")

# 次の単語を表示する関数
def display_next_word(words, word_label, meaning_label):
    global current_category, current_index
    filtered_words = [word for word, info in words.items() if category_to_num(current_category) == info['mastery_level'] or current_category == "全て"]

    if filtered_words:
        # インデックスを増やし、必要に応じてループさせる
        current_index = (current_index + 1) % len(filtered_words)
        word_label.config(text=filtered_words[current_index])
        meaning_label.config(text=words[filtered_words[current_index]]['meaning'])
    else:
        word_label.config(text="単語がありません")
        meaning_label.config(text="")

# 特定の習熟度レベルの単語数を数える関数
def count_words(words, level):
    if level == "全て":
        return len(words)
    level_num = category_to_num(level)
    return sum(1 for info in words.values() if info['mastery_level'] == level_num)

########## アプリケーション終了時の処理 ##########
def on_close(root, filename, words):
    save_words(filename, words)
    root.destroy()


########## メイン関数 ##########
def main():
    root = tk.Tk()
    root.title("単語帳アプリ")
    root.geometry("500x400")

    words = load_words("words.csv")

    start_mode_selection(root, words)

    # アプリケーションの終了イベントに保存機能をバインド
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, "words.csv", words))

    root.mainloop()

if __name__ == "__main__":
    main()

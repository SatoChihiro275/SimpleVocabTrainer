import csv
import tkinter as tk
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 日本語フォントの設定（matplotlibの日本語バグ抑制のため）
mpl.rcParams['font.family'] = 'Meiryo'

########################################################

### CSVファイルから単語を読み込み、リストとして返す関数 ###
def load_words(filename):
    words = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                words.append(row)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filename}")
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
    return words

### 指定されたラベルに次の単語を表示し、グラフを非表示にする関数 ###
def next_word(label, words, index, mastery_levels, frame):
    # 習熟度が最大でない単語を探す
    original_index = index[0]
    while True:
        index[0] += 1
        if index[0] >= len(words):
            index[0] = 0

        # 全ての単語をチェックしたか確認
        if index[0] == original_index:
            label.config(text="全ての単語が習得済みです")
            break

        current_word = words[index[0]][0]
        if mastery_levels[current_word] < 2:  # 習得済みでない単語を選択
            label.config(text=current_word)
            break
    
    # グラフを非表示にする
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()

### 現在表示されている単語の習熟度を更新し、次の単語を表示し、グラフを更新する関数 ###
def update_and_next(word_label, words, index, mastery_levels, frame, progress_button, level):
    word = word_label.cget("text")
    mastery_levels[word] = level
    next_word(word_label, words, index, mastery_levels, frame)
    
    # グラフを非表示にし、ボタンのテキストを更新
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()
    progress_button.config(text="進捗を表示")

### グラフの表示と非表示を切り替える関数 ###
# 「進捗を表示」ボタンのテキストに基づいて、グラフを表示または非表示にする
def toggle_progress(button, frame, mastery_levels):
    if button.cget("text") == "進捗を表示":
        show_progress(mastery_levels, frame)
        button.config(text="進捗を非表示")
    else:
        # グラフの非表示処理
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()
        button.config(text="進捗を表示")

### 習熟度レベルごとの単語数をグラフとして表示する関数 ###
# グラフはTkinterウィンドウ内に描画される
def show_progress(mastery_levels, frame):
    # 以前のグラフをクローズ
    plt.close()

    # 既存のグラフをクリア
    for widget in frame.winfo_children():
        widget.destroy()

    # 習熟度レベルごとの単語数を集計
    counts = [0, 0, 0]  # 0: 未学習, 1: 学習中, 2: 習得済み
    for level in mastery_levels.values():
        counts[level] += 1

    # グラフの作成
    fig, ax = plt.subplots()
    ax.bar(["未学習", "学習中", "習得済み"], counts, color=['red', 'yellow', 'green'])

    # Tkinterウィンドウにグラフを埋め込む
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    frame.pack()  # グラフを表示するフレームを表示

########################################################

### メイン関数 ###
# GUIのウィンドウとウィジェットを作成し、アプリケーションを起動する
def main():
    root = tk.Tk()
    root.title("単語帳アプリ")
    root.geometry("600x450")  # ウィンドウのサイズを設定

    words = load_words("words.csv") # 単語リストの読み込み
    current_word_index = [0]  # 現在の単語のインデックスを追跡
    mastery_levels = {word[0]: 0 for word in words}  # 各単語の習熟度を初期化
    # 例: 0 = 未学習, 1 = 学習中, 2 = 習得済み
    
    # 最初に単語を表示するラベル
    if all(level == 2 for level in mastery_levels.values()):
        initial_text = "全ての単語の習熟度が最大です"
    elif not words:
        initial_text = "単語リストを読み込めませんでした"
    else:
        initial_text = words[current_word_index[0]][0]
    
    word_label = tk.Label(root, text=initial_text, font=("Helvetica", 16))
    word_label.pack(pady=20)

    # 習熟度更新ボタン
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="未学習", command=lambda: update_and_next(word_label, words, current_word_index, mastery_levels, progress_frame, progress_button, 0)).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="学習中", command=lambda: update_and_next(word_label, words, current_word_index, mastery_levels, progress_frame, progress_button, 1)).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="習得済み", command=lambda: update_and_next(word_label, words, current_word_index, mastery_levels, progress_frame, progress_button, 2)).pack(side=tk.LEFT)

    # 進捗表示ボタン
    progress_frame = tk.Frame(root)
    progress_button = tk.Button(root, text="進捗を表示", command=lambda: toggle_progress(progress_button, progress_frame, mastery_levels))
    progress_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
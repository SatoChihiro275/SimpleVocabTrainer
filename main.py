import csv
import tkinter as tk

########################################################

# CSVファイルから単語を読み込む関数
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

# 次の単語を表示する関数
def next_word(label, words, index, mastery_levels):
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

# 習熟度を更新する関数
def update_mastery(word, mastery_levels, level):
    mastery_levels[word] = level

########################################################

# メイン関数
def main():
    root = tk.Tk()
    root.title("単語帳アプリ")
    root.geometry("400x300")  # ウィンドウのサイズを設定

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

    # 次の単語に進むボタン
    next_button = tk.Button(root, text="次の単語", command=lambda: next_word(word_label, words, current_word_index, mastery_levels))
    next_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
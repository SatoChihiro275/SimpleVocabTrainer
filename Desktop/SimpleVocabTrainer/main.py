import csv
import tkinter as tk

# 単語リスト(csvファイル)の読み込み
def load_words(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

def main():
    root = tk.Tk()
    root.title("単語帳アプリ")
    root.geometry("400x300")  # ウィンドウのサイズを設定

    # ここにウィジェットを追加するコードを書く

    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
import tkinter.messagebox as tkm
import math
from decimal import Decimal, Context

# ボタンがクリックされた時の挙動
def button_click(event):
    btn = event.widget
    num = btn["text"]
    if num == "=": #「=」が押された時
        txt = entry.get() #入力欄の値を取得
        txt = txt.replace("÷", "/")
        txt = txt.replace("×", "*")
        ans = decimal_normalize(eval(txt)) #入力欄の値を評価、計算
        entry.delete(0, tk.END) #入力欄の削除
        entry.insert(tk.END, ans) #計算結果を入力欄に戻す
    elif num == "AC":
        entry.delete(0, tk.END)
    elif num == "C":
        txt = entry.get() #入力欄の値を取得
        ans = txt[0:-1]
        entry.delete(0, tk.END) #入力欄の削除
        entry.insert(tk.END, ans) #計算結果を入力欄に戻す
    elif num == "±":
        txt = entry.get() #入力欄の値を取得
        try:
            ans = decimal_normalize(float(txt) * -1) #入力欄の値にマイナス１をかける
            entry.delete(0, tk.END) #入力欄の削除
            entry.insert(tk.END, ans) #計算結果を入力欄に戻す
        except:
            pass
    elif num == "x²":
        txt = entry.get() #入力欄の値を取得
        try:
            ans = decimal_normalize(pow(float(txt), 2)) #入力欄の値を２乗する
            entry.delete(0, tk.END) #入力欄の削除
            entry.insert(tk.END, ans) #計算結果を入力欄に戻す
        except:
            pass
    elif num == "x!":
        txt = entry.get() #入力欄の値を取得
        try:
            ans = decimal_normalize(math.factorial(float(txt))) #入力欄の値を階乗する
            entry.delete(0, tk.END) #入力欄の削除
            entry.insert(tk.END, ans) #計算結果を入力欄に戻す
        except:
            pass
    elif num == "√":
        txt = entry.get() #入力欄の値を取得
        try:
            ans = decimal_normalize(math.sqrt(float(txt))) #入力欄の値の平方根を計算する
            entry.delete(0, tk.END) #入力欄の削除
            entry.insert(tk.END, ans) #計算結果を入力欄に戻す
        except:
            pass
    elif num == "R3":
        txt = entry.get() #入力欄の値を取得
        try:
            ans = decimal_normalize(round((float(txt)), 3)) #入力欄の値の小数点第３位で丸める
            entry.delete(0, tk.END) #入力欄の削除
            entry.insert(tk.END, ans) #計算結果を入力欄に戻す
        except:
            pass
    else: #上記以外のボタンが押された時
        #クリックしたボタンの値を入力欄の末尾に入れる
        entry.insert(tk.END, num)

def decimal_normalize(f): #小数点以下を正規化し、文字列で返す（0などの余計な小数点を出力させないため）
    def _remove_exponent(d):
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    a = Decimal.normalize(Decimal(str(f)))
    b = _remove_exponent(a)
    return str(b)

def enter_bg_number(event): #マウスホバー時の処理（数字）
    event.widget['bg'] = "#808080"
def leave_bg_number(event): #マウスが離れた時の処理（数字）
    event.widget['bg'] = "#696969"
def enter_bg(event): #マウスホバー時の処理（数字以外）
    event.widget['bg'] = "#ffffff"
def leave_bg(event): #マウスが離れた時の処理（数字以外）
    event.widget['bg'] = "#f2f2f2"


root = tk.Tk()
root.title("電卓") #タイトル
root.geometry("390x550") #ウィンドウサイズの設定
root.resizable(False, False)
root.configure(bg="black") #背景色の変更

#入力欄
entry = tk.Entry(root, justify="right", width=14, font=("Times New Roman", 40))
entry.grid(row=0, column=0, columnspan=4)

r, c = 1, 0
count = 0
operators = [["x²", "x!", "C", "AC"], ["R3", "√", "±", "÷"], ["×", "-", "+"], [".", "="]]

#上２行
for i in range(2):
    for j in range(4):
        ope = operators[i][j]
        Button = tk.Button(root, text=f"{ope}", width=4, height=1, font=("Times New Roman", 30), bg="#f2f2f2")
        Button.grid(row=r, column=c)
        Button.bind("<1>", button_click)
        Button.bind("<Enter>", enter_bg)
        Button.bind("<Leave>", leave_bg)
        c += 1
        if c%4 == 0:
            c = 0
    r += 1

#数字部分
for num in range(9, -1, -1):
    if c==2:
        moji = operators[2][count]
        Button = tk.Button(root, text=f"{moji}", width=4, height=1, font=("Times New Roman", 30), bg="#f2f2f2")
        Button.grid(row=r, column=(c+1))
        Button.bind("<1>", button_click)
        Button.bind("<Enter>", enter_bg)
        Button.bind("<Leave>", leave_bg)
        count += 1
    if num == 0:
        Button = tk.Button(root, text=f"{num}", width=8, height=1, font=("Times New Roman", 31), fg="white", bg="#696969")
        Button.grid(row=r, column=c, columnspan=2)
    else:
        Button = tk.Button(root, text=f"{num}", width=4, height=1, font=("Times New Roman", 30), fg="white", bg="#696969")
        Button.grid(row=r, column=c)
    Button.bind("<Enter>", enter_bg_number)
    Button.bind("<Leave>", leave_bg_number)
    Button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

#最後の行の数字以外
for ope in operators[3]:
    Button = tk.Button(root, text=f"{ope}", width=4, height=1, font=("Times New Roman", 30), bg="#f2f2f2")
    Button.grid(row=r, column=c+1)
    Button.bind("<1>", button_click)
    Button.bind("<Enter>", enter_bg)
    Button.bind("<Leave>", leave_bg)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

root.mainloop()
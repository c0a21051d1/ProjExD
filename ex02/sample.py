import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk() #ウィンドウ作成(Pythonでは大文字から始まるとクラス名)
root.title("おためしか")
root.geometry("500x200") #ウィンドウのサイズ"幅×高さ"

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo("txt",f"[{txt}]ボタンが押されました")

label = tk.Label(root,text  = "らべるを書いてみた件",
                font=("", 20) #font:(フォントタイプ、フォントサイズ)
                )
label.pack()

button = tk.Button(root,text = "押すな", command = button_click)

button.bind("<1>",button_click)
button.pack() #pack(方向)：指定した方向（デフォルト：上）から順に配置する

entry = tk.Entry(root, width=30) #半角30文字ぐらいの幅
entry.insert(tk.END,"fugapiyo")
entry.pack()

root.mainloop()#ウィンドウを表示する

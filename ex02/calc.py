import tkinter as tk
import tkinter.messagebox as tkm


# 練習３
def button_click(event):
    btn = event.widget
    num = btn["text"]
    if num == "=":
        siki = entry.get() #数式の文字列
        res = eval(siki)
        entry.delete(0,tk.END) #表示文字列の削除
        entry.insert(tk.END,res) #結果の挿入

    else: # 「=」以外のボタン字
        #tkm.showinfo("", f"{num}ボタンがクリックされました")
        # 練習６
        entry.insert(tk.END, num)

    if num =="AC":                 #文字列削除
        entry.delete(0,tk.END)
    
        
    
# 練習１
root = tk.Tk()
root.geometry("380x600")

# 練習４
entry = tk.Entry(root, justify="right", width=10, font=("",40))
entry.grid(row=0, column=0, columnspan=3)

# 練習２
r, c = 1, 0
operands = ["7","8","9","4","5","6","1","2","3","0"]
for num in operands:
    button = tk.Button(root, text=f"{num}", width=4, height=2, font=("", 30))
    button.grid(row=r, column=c)
    button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0
    button['bg'] = '#FFFFFF' #色をWhiteに変更

# 練習５
operators = ["/","*","-","+","="] #四則演算,イコール
r,c=0,3
for ope in operators:
    button = tk.Button(root, text=f"{ope}", width=4, height=2, font=("", 30))
    button.grid(row=r, column=c)
    button.bind("<1>", button_click)
    r+=1
    if c%4 == 0:
        c += 1
    button['bg'] = '#D3D3D3' #色をLightGreyに変更
    button['fg'] = "#0000ff" #文字色をBlueに変更    

func = ["C","AC"] #一文字削除と全消去
r,c=4,1
for fun in func:
    button = tk.Button(root, text=f"{fun}", width=4, height=2, font=("", 30))
    button.grid(row=r,column=c)
    button.bind("<1>",button_click)
    c+=1
    button['bg'] = "#FFFF00" #背景色をLightGreyに変更
    button['fg'] = "#0000ff" #文字色をBlueに変更

root.mainloop()
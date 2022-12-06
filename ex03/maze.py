import tkinter as tk


def key_down(event):
    global key
    key = event.keysym

def key_up():
    global key
    key = ""

def main_proc():
    global cx,cy
    if key == "Up":
        cy-=20
    if key == "Down":
        cy+=20
    if key == "Left":
        cx-=20
    if key == "Right":
        cx+=20
    canvas.coords("kokaton",cx,cy)
    root.after(100,main_proc)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root,width = 1500,height = 900,bg = "black")

    kokaton = tk.PhotoImage(file="fig/8.png")
    cx,cy = 300,400
    canvas.create_image(cx,cy,image = kokaton,tag = "kokaton")
    key = ""
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    main_proc()
    canvas.pack()
    root.mainloop()
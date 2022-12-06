import tkinter as tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""


def main_proc():
    global cx, cy,mx,my
    if key == "Up"   or key == "w" :  #上矢印キーか"w"が押されたら
        my -= 1        
    if key == "Down" or key == "s" :  #下矢印キーか"s"が押されたら
        my += 1
    if key == "Left" or key == "a" :  #左矢印キーか"a"が押されたら
        mx -= 1
    if key == "Right"or key == "d" :  #右矢印キーか"d"が押されたら
        mx += 1

    if maze_lst[mx][my] ==1:     #移動先が壁だったら
        if key == "Up"   or key == "w" : my += 1
        if key == "Down" or key == "s" : my -= 1
        if key == "Left" or key == "a" : mx += 1
        if key == "Right"or key == "d" : mx -= 1


    cx, cy = mx*100+50, my*100+50
    canvas.coords("kokaton", cx, cy)
    root.after(100, main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()

    maze_lst = mm.make_maze(15, 9)
    # print(maze_lst)
    mm.show_maze(canvas, maze_lst)

    mx,my = 1,1
    cx, cy = mx*50, my*50
    tori = tk.PhotoImage(file="fig/8.png")
    canvas.create_image(cx, cy, image=tori, tag="kokaton")
    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    root.mainloop()
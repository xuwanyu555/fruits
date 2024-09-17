import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
#自动生成
PASSWORD = "12893"
def start_game1():
    # 启动第一个游戏
    subprocess.Popen(["python", "fruithard.py"])

def start_game2():
    # 弹出密码对话框
    password = simpledialog.askstring("果了个果破解版", "请用一个八卦交换密钥，输入密钥启动果了个果破解版:")
    
    if password == PASSWORD:
        # 启动第二个游戏
        subprocess.Popen(["python", "fruiteasy.py"])
    else:
        messagebox.showerror("错误", "密钥错误!")


def show_help():
    # 弹出游戏规则对话框
    messagebox.showinfo("游戏规则", "1、点击水果图片移入卡槽\r\n2、三个相同的水果可进行消除\r\n3、卡槽只允许同时存放11张图片\r\n5、只有等上一层的图片点完才能点开下一层\r\n4、你一共有144s的时间消除水果")

# 创建主窗口
root = tk.Tk()
root.title("果了个果")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" % (int(width / 2), int(height / 2), int(width / 4), int(height / 4)))
#
bg_image = tk.PhotoImage(file="C:\\Users\\86158\\Desktop\\果了个果\\images\\back0.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
#设置字体
font_settings = ('宋体', 40) 
# 创建按钮
btn_start_game1 = tk.Button(root, text="开始游戏", command=start_game1, bg='green' , fg='blue', font=font_settings)
btn_start_game1.pack(pady=10)

btn_help = tk.Button(root, text="帮助", command=show_help, bg='green', fg='blue', font=font_settings)
btn_help.pack(pady=10)

btn_start_game2 = tk.Button(root, text="破解版", command=start_game2, bg='green', fg='blue', font=font_settings)
btn_start_game2.pack(pady=10)



# 运行主事件循环
root.mainloop()

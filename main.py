import tkinter as tk
from tkinter import messagebox, filedialog
import os
import threading

from markitdown import MarkItDown


def convert_file(file_path):
    try:
        output = os.path.splitext(file_path)[0] + ".md"

        converter = MarkItDown()

        result = converter.convert(file_path)

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(result.text_content)

        messagebox.showinfo(
            "转换完成",
            f"已生成：\n{output}"
        )

    except Exception as e:
        messagebox.showerror(
            "转换失败",
            str(e)
        )


def run_convert(file_path):
    thread = threading.Thread(
        target=convert_file,
        args=(file_path,)
    )

    thread.daemon = True
    thread.start()


def choose_file():
    file = filedialog.askopenfilename()

    if file:
        run_convert(file)


# 拖拽处理
def drop(event):
    files = root.tk.splitlist(event.data)

    for file in files:
        if os.path.isfile(file):
            run_convert(file)



# 创建窗口
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES

    root = TkinterDnD.Tk()

    drag_support = True

except ImportError:

    root = tk.Tk()

    drag_support = False



root.title("MarkItDown lite")
root.geometry("600x400")


label = tk.Label(
    root,
    text=
    "MarkItDown lite\n\n"
    "拖入 PDF / DOCX / PPTX / XLSX\n\n"
    "自动转换为 Markdown",
    font=("Microsoft YaHei", 16)
)

label.pack(expand=True)



button = tk.Button(
    root,
    text="选择文件",
    width=20,
    height=2,
    command=choose_file
)

button.pack(pady=20)



if drag_support:

    label.drop_target_register(
        DND_FILES
    )

    label.dnd_bind(
        "<<Drop>>",
        drop
    )


root.mainloop()

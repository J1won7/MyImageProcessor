import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
from bitmap import Bitmap

# 전역 변수 선언
tk_img = None


def open_file_dialog():
    global tk_img  # 전역 변수 사용

    # 파일 탐색기 열기
    file_path = filedialog.askopenfilename()

    if file_path:
        bm_img = Bitmap(file_path).get_image()
        tk_img = ImageTk.PhotoImage(bm_img)
        label.config(image=tk_img)


# Tkinter 윈도우 생성
root = tk.Tk()
root.title("이미지 처리기")
root.geometry("400x200")

# 버튼 생성 및 배치
button = tk.Button(root, text="이미지 열기", command=open_file_dialog)
button.pack(pady=20)

# 이미지 라벨 생성 및 배치
label = tk.Label(root)
label.pack(pady=10)

# Tkinter 이벤트 루프 시작
root.mainloop()

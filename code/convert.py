import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import pyttsx3
from googletrans import Translator
import numpy as np

# Khoi tao GUI
root = tk.Tk()
root.geometry('800x600')
root.title('Detection text in image')
root.configure(background='#F3F3F3')

# Tao frame
button_frame1 = tk.Frame(root)
button_frame1.pack(side=tk.BOTTOM, pady=10)
button_frame2 = tk.Frame(root)
button_frame2.pack(side=tk.BOTTOM, pady=10)

image_label = None

# Khoi tao reader
reader = easyocr.Reader(['en','vi'])

detected_texts = []

# Phat hien chu trong anh
def image_to_text(img):
    result = reader.readtext(img)
    detected_texts.clear()
    print("\nText is detected:")
    for detection in result:
        bbox, text, score = detection
        bbox = np.array(bbox)
        bbox = bbox.reshape(-1, 2)
        x1, y1 = map(int, bbox[0])
        x2, y2 = map(int, bbox[2])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(img, text, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
        print(text)
        detected_texts.append(text)

    return img


# Chon file anh de mo
def open_image():
    global image_label
    filetypes = (
        ("JPEG files", "*.jpg"),
        ("PNG files", "*.png")
    )
    image_path = filedialog.askopenfilename(title="Select Image",filetypes=filetypes)

    if image_path:
        img = cv2.imread(image_path)

        detection_img = image_to_text(img)

        img_pil = Image.fromarray(cv2.cvtColor(detection_img, cv2.COLOR_BGR2RGB))

        max_width = 800
        max_height = 600
        img_pil.thumbnail((max_width, max_height))

        img_tk = ImageTk.PhotoImage(img_pil)

        if image_label:
            image_label.configure(image=img_tk)
            image_label.image = img_tk
        else:
            image_label = tk.Label(root, image=img_tk)
            image_label.pack()

    save_button.config(state=tk.NORMAL)
    speech_button.config(state=tk.NORMAL)
    translate_button1.config(state=tk.NORMAL)
    translate_button2.config(state=tk.NORMAL)

    root.mainloop()


def clear_label():
    notif_label.config(text="")


# Luu ket qua nhan dang
def save_result():
    filetypes = (
        ("PDF files", "*.pdf"),
        ("Text files", "*.txt"),
        ("Docx files", "*.docx")
    )
    save_path = filedialog.asksaveasfilename(title="Save Result", filetypes=filetypes, defaultextension=".txt")
    if save_path:
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write("\n".join(detected_texts))
            print("\nSave success!")
            notif_label.config(text="Lưu thành công!")
            root.after(5000,clear_label)


# Chuyen tu chu sang loi noi
def text_to_speech():
    speech = pyttsx3.init()
    speech.say(detected_texts)
    speech.runAndWait()


# Dich sang tieng viet
def translate_to_vi():
    text = " ".join(detected_texts)
    translator = Translator()
    translation = translator.translate(text,src='en',dest="vi")
    print("\nDịch: ")
    print(translation.text)

    # Luu ban dich
    filetypes = (
        ("PDF files", "*.pdf"),
        ("Text files", "*.txt"),
        ("Docx files", "*.docx")
    )
    save_path = filedialog.asksaveasfilename(title="Save Result", filetypes=filetypes, defaultextension=".txt")
    if save_path:
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write("\n"+translation.text)
            print("\nSave success!")
            notif_label.config(text="Lưu thành công!")
            root.after(5000,clear_label)


# Dich sang tieng anh
def translate_to_en():
    text = " ".join(detected_texts)
    translator = Translator()
    translation = translator.translate(text,src='vi',dest="en")
    print("\nDịch: ")
    print(translation.text)

    # Luu ban dich
    filetypes = (
        ("PDF files", "*.pdf"),
        ("Text files", "*.txt"),
        ("Docx files", "*.docx")
    )
    save_path = filedialog.asksaveasfilename(title="Save Result", filetypes=filetypes, defaultextension=".txt")
    if save_path:
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write("\n"+translation.text)
            print("\nSave success!")
            notif_label.config(text="Lưu thành công!")
            root.after(5000,clear_label)


# Khoi tao cac thanh phan GUI
notif_label = tk.Button(root,text="",background='white', foreground='black')
notif_label.pack(side=tk.BOTTOM,pady=10)    

save_button = tk.Button(button_frame1, text="Lưu kết quả", command=save_result)
save_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
save_button.pack(side=tk.LEFT,padx=10,pady=10)
save_button.config(state=tk.DISABLED)

open_button = tk.Button(button_frame1, text="Chọn ảnh", command=open_image)
open_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
open_button.pack(side=tk.LEFT,padx=10,pady=10)

speech_button = tk.Button(button_frame2, text="Chuyển sang lời nói", command=text_to_speech)
speech_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
speech_button.pack(side=tk.LEFT,padx=10)
speech_button.config(state=tk.DISABLED)

translate_button1 = tk.Button(button_frame2, text="Dịch sang tiếng việt", command=translate_to_vi)
translate_button1.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
translate_button1.pack(side=tk.LEFT,padx=10)
translate_button1.config(state=tk.DISABLED)

translate_button2 = tk.Button(button_frame2, text="Dịch sang tiếng anh", command=translate_to_en)
translate_button2.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
translate_button2.pack(side=tk.LEFT,padx=10)
translate_button2.config(state=tk.DISABLED)

heading = tk.Label(root, text="Trích xuất chữ từ ảnh",pady=20, font=('arial',20,'bold'))
heading.configure(background='#F3F3F3',foreground='black')
heading.pack(side=tk.TOP)

root.mainloop()

import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import pyttsx3
import keyboard

# Khoi tao GUI
root = tk.Tk()
root.geometry('800x600')
root.title('Detection text in image')
root.configure(background='#F3F3F3')

# Tao frame
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

image_label = None

# Phat hien chu trong anh
reader = easyocr.Reader(['en','vi'])

detected_texts = []

# Tach chu tu anh
def image_to_text(img):
    result = reader.readtext(img)
    detected_texts.clear()
    print("\nText is detected:")
    for detection in result:
        bbox, text, score = detection
        x1, y1 = bbox[0]
        x2, y2 = bbox[2]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(img, text, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
        print(detection[1])
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
        max_height = 800
        img_pil.thumbnail((max_width, max_height))

        img_tk = ImageTk.PhotoImage(img_pil)

        if image_label:
            image_label.configure(image=img_tk)
            image_label.image = img_tk
        else:
            image_label = tk.Label(root, image=img_tk)
            image_label.pack()

    root.mainloop()


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


# Chuyen tu chu sang loi noi
def text_to_speech():
    speech = pyttsx3.init()
    def onWord(name, location, length):
        print ('word', name, location, length)
        if keyboard.is_pressed("esc"):
            speech.stop()

    speech.connect('started-word', onWord)
    speech.say(detected_texts)
    speech.runAndWait()


# Khoi tao cac thanh phan GUI
save_button = tk.Button(button_frame, text="Lưu kết quả", command=save_result)
save_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
save_button.pack(side=tk.LEFT,padx=10,pady=10)

open_button = tk.Button(button_frame, text="Chọn ảnh", command=open_image)
open_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
open_button.pack(side=tk.LEFT,padx=10,pady=10)

speech_button = tk.Button(button_frame, text="Chuyển sang lời nói", command=text_to_speech)
speech_button.configure(background='#63B8FF', foreground='black',font=('arial',10,'bold'))
speech_button.pack(side=tk.LEFT,padx=10,pady=10)

heading = tk.Label(root, text="Trích xuất chữ từ ảnh",pady=20, font=('arial',20,'bold'))
heading.configure(background='#F3F3F3',foreground='black')
heading.pack(side=tk.TOP)

root.mainloop()
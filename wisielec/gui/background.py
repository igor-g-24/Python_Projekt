from PIL import Image, ImageTk
import os
import tkinter as tk

def set_background(root):
    image_path = os.path.join("obrazy", "kartka.png")
    img = Image.open(image_path)
    background = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=background)
    label.image = background  # zapamiętaj referencję
    label.place(relwidth=1, relheight=1)
    return label  # zwracamy label, żeby był pod spodem
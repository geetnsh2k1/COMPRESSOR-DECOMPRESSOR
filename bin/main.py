import tkinter as tk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

# main loop
root = tk.Tk()
root.geometry("750x750")
root.minsize(750, 750)
root.maxsize(750, 750)
root.title("File-Compressor")

# size of window
canvas = tk.Canvas(root, width=720, height= 480)
canvas.grid(columnspan=3, rowspan=3)

# image
logo = Image.open('./logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# instructions
instructions = tk.Label(root, text="Select a file on your computer and compress/decompress it.", font="Montserrat-Medium")
instructions.grid(columnspan=3, column=0, row=1)

# functions
def open_file():
    browse_text.set("Loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file")
    if file:
        # text box
        page_content = "File read successfully!"
        text_box = tk.Text(root, height=10, width=80, padx=15, pady=15)
        text_box.insert(1.0, page_content)
        text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=1, row=3)

        browse_text.set("Browse")

def compress():
    pass
def decompress():
    pass

# browse button 
browse_text = tk.StringVar() 
compress_btn = tk.Button(root, textvariable=browse_text, command=lambda:compress(), font="Montserrat-Medium", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Compress")
compress_btn.grid(column=1, row=2)

browse_text = tk.StringVar() 
decompress_btn = tk.Button(root, textvariable=browse_text, command=lambda:decompress(), font="Montserrat-Medium", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Decompress")
decompress_btn.grid(column=1, row=3)

canvas = tk.Canvas(root, width=720, height= 240)
canvas.grid(columnspan=3)

root.mainloop()
# main loop ends
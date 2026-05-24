import os
import torch

from PIL import Image as PILImage
from PIL import ImageTk

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class ImageCaptionAI:

    def __init__(self, root):

        self.root = root

        self.root.title("AI Image Caption Generator")

        self.root.geometry("900x700")

        self.root.configure(bg="#0f172a")

        self.root.resizable(False, False)

        self.image_path = ""

        self.processor = None

        self.model = None

        self.create_title()

        self.create_frame()

        self.create_buttons()

        self.create_image_label()

        self.create_caption_box()

        self.create_status_bar()

        self.load_model()

    def create_title(self):

        self.title_label = Label(
            self.root,
            text="AI IMAGE CAPTION GENERATOR",
            font=("Segoe UI", 24, "bold"),
            bg="#0f172a",
            fg="white"
        )

        self.title_label.pack(pady=20)

    def create_frame(self):

        self.main_frame = Frame(
            self.root,
            bg="#1e293b",
            width=850,
            height=500
        )

        self.main_frame.pack(pady=10)

        self.main_frame.pack_propagate(False)

    def create_buttons(self):

        self.button_frame = Frame(
            self.main_frame,
            bg="#1e293b"
        )

        self.button_frame.pack(pady=20)

        self.upload_button = Button(
            self.button_frame,
            text="Upload Image",
            font=("Segoe UI", 14, "bold"),
            bg="#2563eb",
            fg="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.upload_image
        )

        self.upload_button.grid(
            row=0,
            column=0,
            padx=20
        )

        self.generate_button = Button(
            self.button_frame,
            text="Generate Caption",
            font=("Segoe UI", 14, "bold"),
            bg="#16a34a",
            fg="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.generate_caption
        )

        self.generate_button.grid(
            row=0,
            column=1,
            padx=20
        )

        self.clear_button = Button(
            self.button_frame,
            text="Clear",
            font=("Segoe UI", 14, "bold"),
            bg="#dc2626",
            fg="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_all
        )

        self.clear_button.grid(
            row=0,
            column=2,
            padx=20
        )

    def create_image_label(self):

        self.image_frame = Frame(
            self.main_frame,
            bg="#334155",
            width=600,
            height=250
        )

        self.image_frame.pack(pady=10)

        self.image_frame.pack_propagate(False)

        self.image_label = Label(
            self.image_frame,
            text="No Image Selected",
            font=("Segoe UI", 16),
            bg="#334155",
            fg="white"
        )

        self.image_label.pack(expand=True)

    def create_caption_box(self):

        self.caption_title = Label(
            self.main_frame,
            text="Generated Caption",
            font=("Segoe UI", 18, "bold"),
            bg="#1e293b",
            fg="white"
        )

        self.caption_title.pack(pady=10)

        self.caption_box = ScrolledText(
            self.main_frame,
            width=70,
            height=5,
            font=("Segoe UI", 14),
            bg="#f8fafc",
            fg="black",
            wrap=WORD
        )

        self.caption_box.pack(pady=10)

    def create_status_bar(self):

        self.status = StringVar()

        self.status.set("Loading AI Model...")

        self.status_bar = Label(
            self.root,
            textvariable=self.status,
            font=("Segoe UI", 11),
            bg="#111827",
            fg="white",
            anchor=W
        )

        self.status_bar.pack(
            side=BOTTOM,
            fill=X
        )

    def load_model(self):

        try:

            self.processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )

            self.model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )

            self.status.set(
                "AI Model Loaded Successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Model Error",
                str(e)
            )

            self.status.set(
                "Failed To Load AI Model"
            )

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if file_path:

            self.image_path = file_path

            image = PILImage.open(file_path)

            image = image.resize((350, 220))

            photo = ImageTk.PhotoImage(image)

            self.image_label.config(
                image=photo,
                text=""
            )

            self.image_label.image = photo

            self.status.set(
                "Image Uploaded Successfully"
            )

    def generate_caption(self):

        if self.image_path == "":

            messagebox.showwarning(
                "Warning",
                "Please Upload An Image First"
            )

            return

        try:

            self.status.set(
                "Generating Caption..."
            )

            self.root.update()

            image = PILImage.open(
                self.image_path
            ).convert("RGB")

            inputs = self.processor(
                image,
                return_tensors="pt"
            )

            output = self.model.generate(
                **inputs
            )

            caption = self.processor.decode(
                output[0],
                skip_special_tokens=True
            )

            self.caption_box.delete(
                1.0,
                END
            )

            self.caption_box.insert(
                END,
                caption
            )

            self.status.set(
                "Caption Generated Successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status.set(
                "Error Generating Caption"
            )

    def clear_all(self):

        self.image_path = ""

        self.image_label.config(
            image="",
            text="No Image Selected"
        )

        self.caption_box.delete(
            1.0,
            END
        )

        self.status.set(
            "Cleared Successfully"
        )


class SplashScreen:

    def __init__(self, root):

        self.root = root

        self.root.title("Loading")

        self.root.geometry("500x300")

        self.root.configure(bg="#020617")

        self.root.resizable(False, False)

        self.title = Label(
            self.root,
            text="IMAGE CAPTIONING AI",
            font=("Segoe UI", 28, "bold"),
            bg="#020617",
            fg="white"
        )

        self.title.pack(pady=70)

        self.loading = ttk.Progressbar(
            self.root,
            orient=HORIZONTAL,
            length=300,
            mode='indeterminate'
        )

        self.loading.pack(pady=20)

        self.loading.start()

        self.text = Label(
            self.root,
            text="Initializing Artificial Intelligence...",
            font=("Segoe UI", 12),
            bg="#020617",
            fg="#cbd5e1"
        )

        self.text.pack()

        self.root.after(
            3000,
            self.open_main
        )

    def open_main(self):

        self.root.destroy()

        main_root = Tk()

        app = ImageCaptionAI(main_root)

        main_root.mainloop()


def main():

    splash_root = Tk()

    splash = SplashScreen(splash_root)

    splash_root.mainloop()


if __name__ == "__main__":

    main()
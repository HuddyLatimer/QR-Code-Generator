import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import customtkinter as ctk
import os


class QRCodeGenerator:
    def __init__(self):
        # Setup window
        self.root = ctk.CTk()
        self.root.title("QR Code Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.qr_image = None
        self.tk_image = None

        # Create main container
        self.create_widgets()

    def create_widgets(self):
        # Main container with padding
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            container,
            text="QR Code Generator",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=(0, 20))

        # Input frame
        input_frame = ctk.CTkFrame(container)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        # URL Entry with label
        url_label = ctk.CTkLabel(
            input_frame,
            text="Enter URL or Text:",
            font=("Helvetica", 14)
        )
        url_label.pack(anchor="w", pady=(10, 5))

        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="https://example.com",
            width=400,
            height=40
        )
        self.url_entry.pack(fill="x", pady=(0, 10))

        # Buttons frame
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.pack(fill="x", pady=10)

        # Generate button
        self.generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr,
            width=200,
            height=40,
            font=("Helvetica", 14)
        )
        self.generate_btn.pack(side="left", padx=5)

        # Save button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save QR Code",
            command=self.save_qr,
            state="disabled",
            width=200,
            height=40,
            font=("Helvetica", 14)
        )
        self.save_button.pack(side="left", padx=5)

        # QR Code display frame
        self.display_frame = ctk.CTkFrame(container, fg_color=("gray90", "gray16"))
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # QR Code display label
        self.qr_display = ctk.CTkLabel(self.display_frame, text="")
        self.qr_display.pack(expand=True)

        # Status bar
        self.status_label = ctk.CTkLabel(
            container,
            text="Ready to generate QR code",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=(10, 0))

    def generate_qr(self):
        url = self.url_entry.get().strip()
        if not url:
            self.show_error("Please enter a URL or text")
            return

        try:
            self.status_label.configure(text="Generating QR code...")
            self.root.update()

            # Generate QR code with style
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            self.qr_image = qr.make_image(fill_color="black", back_color="white")

            # Resize for display
            display_size = (300, 300)
            self.qr_image = self.qr_image.resize(display_size, Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.qr_image)

            # Update display
            self.qr_display.configure(image=self.tk_image)
            self.save_button.configure(state="normal")
            self.status_label.configure(text="QR code generated successfully!")

        except Exception as e:
            self.show_error(f"Error generating QR code: {str(e)}")

    def save_qr(self):
        if not self.qr_image:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qr_code.png"
        )

        if file_path:
            try:
                self.qr_image.save(file_path)
                self.status_label.configure(text="QR code saved successfully!")
                messagebox.showinfo("Success", "QR Code saved successfully!")
            except Exception as e:
                self.show_error(f"Error saving QR code: {str(e)}")

    def show_error(self, message):
        self.status_label.configure(text=message)
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()


def main():
    app = QRCodeGenerator()
    app.run()


if __name__ == "__main__":
    main()
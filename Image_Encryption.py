import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet
from PIL import Image
import os

# Generate or load the encryption key
if os.path.exists("key.key"):
    with open("key.key", "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

def encrypt_image(input_path, output_path):
    with open(input_path, "rb") as image_file:
        image_data = image_file.read()

    encrypted_image_data = cipher_suite.encrypt(image_data)

    with open(output_path, "wb") as encrypted_image_file:
        encrypted_image_file.write(encrypted_image_data)

def decrypt_image(input_path, output_path):
    with open(input_path, "rb") as encrypted_image_file:
        encrypted_image_data = encrypted_image_file.read()

    decrypted_image_data = cipher_suite.decrypt(encrypted_image_data)

    with open(output_path, "wb") as decrypted_image_file:
        decrypted_image_file.write(decrypted_image_data)

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, file_path)

def encrypt_and_save():
    input_path = entry_input.get()
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Encrypted Image files", "*.png")])
        if output_path:
            encrypt_image(input_path, output_path)
            messagebox.showinfo("Success", "Image encrypted and saved successfully!")
    else:
        messagebox.showerror("Error", "Please select an image to encrypt.")

def decrypt_and_save():
    input_path = entry_input.get()
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png")])
        if output_path:
            decrypt_image(input_path, output_path)
            messagebox.showinfo("Success", "Image decrypted and saved successfully!")
    else:
        messagebox.showerror("Error", "Please select an image to decrypt.")

# Create the main application window
app = tk.Tk()
app.title("Image Encryption Tool")

# Add GUI elements
label_input = tk.Label(app, text="Select an Image:")
label_input.grid(row=0, column=0)
entry_input = tk.Entry(app, width=30)
entry_input.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(app, text="Browse", command=browse_image)
button_browse.grid(row=0, column=2, padx=5, pady=5)

button_encrypt = tk.Button(app, text="Encrypt Image", command=encrypt_and_save)
button_encrypt.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

button_decrypt = tk.Button(app, text="Decrypt Image", command=decrypt_and_save)
button_decrypt.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Start the main loop
app.mainloop()

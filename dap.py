import customtkinter as ctk
import requests
import os
from tkinter import messagebox

# Function to download the PDF
def download_pdf():
    url = 'https://atns.com/wp-content/uploads/2019/09/DAP.pdf'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the current working directory
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, 'DAP.pdf')
            
            # Save the PDF to the current directory
            with open(file_path, 'wb') as file:
                file.write(response.content)
            messagebox.showinfo("Success", f"PDF downloaded successfully to {current_directory}")
        else:
            messagebox.showwarning("Failed", f"Failed to download PDF. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main window
ctk.set_appearance_mode("dark")  # Set to dark mode

app = ctk.CTk()  # Create the main window
app.geometry("400x300")
app.title("PDF Downloader")

# Add a label
label = ctk.CTkLabel(app, text="Download PDF", font=("Arial", 20))
label.pack(pady=20)

# Add a download button
download_button = ctk.CTkButton(app, text="Download DAP PDF", command=download_pdf, width=200, height=40, corner_radius=10)
download_button.pack(pady=20)

# Start the application
app.mainloop()

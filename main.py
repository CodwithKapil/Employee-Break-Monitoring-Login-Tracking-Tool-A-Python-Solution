import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import win32api
from PIL import Image, ImageTk
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from bg import BackgroundMonitoring  # Assuming bg.py contains the BackgroundMonitoring class
from Dashboard import Dashboard, json_file_path  # Assuming Dashboard.py contains the Dashboard class


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
json_file = os.path.join(current_dir, '


class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')
        # Initialize background task variable
        self.background_task = None
        # Background image
        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # Logo image
        try:
            self.logo_image = Image.open('images\\logo.png').convert('RGBA').resize((1, 1))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = Label(self.window, image=self.logo_photo, bg=self.window.cget('bg'))
            self.logo_label.image = self.logo_photo
            self.logo_label.place(x=1, y=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Logo image not found. Please check 'images/logo.png' exists.")

        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=250, y=70)

        self.heading = Label(self.lgn_frame, text="Welcome to Crystalvoxx's Employee Management Tool",
                             font=('yu gothic ui', 18, "bold"), bg="#040405", fg='orange', bd='0', relief=GROOVE)
        self.heading.place(x=10, y=1, width=600, height=60)

        # Vector image
        self.side_image = Image.open('images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # Username label, entry, and icon
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405",
                                    fg="#6b6a69", font=("yu gothic ui ", 12, "bold"), insertbackground='#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)

        # Username icon
        self.username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # Password label, entry, and icon
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405",
                                    fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*",
                                    insertbackground='#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        # Password icon
        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)

        # Show/hide password button
        self.show_image = ImageTk.PhotoImage(file='images\\show.png')
        self.hide_image = ImageTk.PhotoImage(file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

        # Login button
        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',
                            command=self.authenticate)
        self.login.place(x=20, y=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            # Simulating successful login
            messagebox.showinfo("Login Successful", "Welcome, {}!".format(username))
            self.update_google_sheet(username)
            self.open_dashboard()  # Open Dashboard after successful login
            self.start_background_task(username)  # Start background task here
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def start_background_task(self, username):
        # Create and start the background task
        self.background_task = BackgroundMonitoring(username)
        self.background_task.start_monitoring()  # Start background task here

    def stop_background_task(self):
        # Stop the background task if it is running
        if self.background_task:
            self.background_task.stop_monitoring()  # Stop background task here
            self.background_task = None

    def open_dashboard(self):
        # Close the current window
        self.window.destroy()
        # Open the Dashboard window
        window = Tk()
        Dashboard(window)  # Assuming Dashboard takes no arguments
        window.mainloop()

    def logout(self):
        # Stop the background task on logout
        self.stop_background_task()

    def main(self):
        username = win32api.GetUserName()
        background_monitoring = BackgroundMonitoring(username)
        background_monitoring.start()  # Start monitoring

    def update_google_sheet(self, username):
        # Google Sheets API authentication
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('c',
                                                                       scope)
        client = gspread.authorize(credentials)

        # Find the correct Google Sheet based on username (case insensitive)
        username_lower = username.lower()
        spreadsheets = client.list_spreadsheet_files()
        sheet_found = False
        sheet_name = None  # Initialize sheet_name variable
        for spreadsheet in spreadsheets:
            if username_lower in spreadsheet['name'].lower():
                sheet_name = spreadsheet['name']
                sheet_found = True
                break

        if not sheet_found:
            messagebox.showerror("Error", "Google Sheet for user '{}' not found.".format(username))
            return

        # Update the spreadsheet with user information and timestamp
        sheet = client.open(sheet_name).sheet1
        row = [datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), username, "Logged In", "-",
               "-", "-", "-", "-"]
        sheet.append_row(row)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=624, y=413)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=624, y=413)
        self.password_entry.config(show='*')


def page():
    window = Tk()
    login_page = LoginPage(window)
    window.protocol("WM_DELETE_WINDOW", login_page.logout)  # Call logout on window close
    window.mainloop()


if __name__ == '__main__':
    page()

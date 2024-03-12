import logging
import time
import gspread
from google.oauth2.service_account import Credentials
import win32api
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard, mouse

# Configure logging
logging.basicConfig(filename='background_monitoring.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - '
                                                                                     '%(message)s')

# Google Sheets credentials
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('', scopes=scope)
gc = gspread.authorize(creds)


class BackgroundMonitoring:
    def __init__(self, username):
        self.running = False
        self.idle_start_time = None
        self.username = username
        self.total_idle_duration = 0  # Initialize total idle duration
        self.last_activity_time = time.time()  # Initialize last activity time
        self.error_count = 0
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main Tkinter window
        # Initialize listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity_detected)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity_detected, on_click=self.on_activity_detected)

    def start_monitoring(self):
        try:
            self.running = True
            # Start listeners
            self.keyboard_listener.start()
            self.mouse_listener.start()
            while self.running:
                try:
                    current_time = time.time()
                    if self.idle_start_time is not None and current_time - self.idle_start_time >= 30:  # 30 seconds
                        # threshold for idle detection
                        idle_duration = current_time - self.idle_start_time
                        logging.info(f"Idle detected: {idle_duration} seconds")
                        self.show_idle_popup(idle_duration)
                        self.update_google_sheet_idle_time(self.idle_start_time, idle_duration)
                        self.idle_start_time = None
                    time.sleep(1)  # Check every 1 second for activity
                except Exception as e:
                    self.error_count += 1
                    logging.error(f"Error in monitoring loop: {e}")
                    if self.error_count > 3:
                        logging.error("Too many errors encountered. Exiting monitoring.")
                        break
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def stop_monitoring(self):
        self.running = False
        # Stop listeners
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_activity_detected(self, *args):
        self.idle_start_time = None
        self.last_activity_time = time.time()

    def update_google_sheet_idle_time(self, start_time, duration):
        try:
            sheet = gc.open(self.username).sheet1
            duration_minutes = int(duration // 60)
            duration_seconds = int(duration % 60)
            duration_str = f"{duration_minutes} minutes {duration_seconds} seconds"
            sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
                              self.username, "Idle", duration_str])
            logging.info("Idle time updated successfully")
            self.total_idle_duration += duration
            sheet.update('G1', f'Total Idle Time: {self.total_idle_duration} seconds')  # Update total idle time
        except Exception as e:
            logging.error(f"Error updating idle time in Google Sheet: {e}")

    def show_idle_popup(self, idle_duration):
        try:
            duration_minutes = int(idle_duration // 60)
            duration_seconds = int(idle_duration % 60)
            idle_message = f"System is idle for {duration_minutes} minutes {duration_seconds} seconds."
            messagebox.showinfo("Idle Detected", idle_message, parent=self.root)
        except Exception as e:
            logging.error(f"Error displaying idle popup: {e}")

    def start(self):
        pass


def main():
    try:
        username = win32api.GetUserName()
        background_monitoring = BackgroundMonitoring(username)
        background_monitoring.start_monitoring()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

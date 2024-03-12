import logging
from pkg_resources import resource_filename
import time
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import requests
import gspread
import urllib3
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import logging
import win32api
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
import threading  # Import threading for background process
def get_resource_path(relative_path):
    return resource_filename(__name__, relative_path)

# Use the function to get the path of your JSON file
json_file_path = get_resource_path('cybernetic-muse-415516-b7d0927056.json')

# Configure logging
logging.basicConfig(filename='dashboard.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Dashboard:
    def __init__(self, window):
        self.window = window
        window.title("Employee Dashboard")
        window.configure(bg="#DCE6F1")  # Soft blue background color
        self.last_activity_time = None  # Initialize last activity time
        self.total_login_duration = datetime.timedelta(0)  # Initialize to zero duration
        self.cumulative_break_duration = datetime.timedelta(0)  # Initialize to zero duration

        # Initialize Google Sheet authentication
        self.init_google_sheet()

        # Button Frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Start Break Button
        self.start_break_button = tk.Button(
            self.button_frame, text="Start Break", command=self.start_break_and_update_google_sheet
        )
        self.table.pack(fill="both", expand=True)
        self.start_break_button.grid(row=0, column=0, padx=5, pady=5)

        # End Break Button (Initially disabled)
        self.end_break_button = tk.Button(
            self.button_frame, text="End Break", command=self.end_break_and_update_google_sheet, state=tk.DISABLED
        )
        self.end_break_button.grid(row=0, column=1, padx=5, pady=5)

        # Logout Button
        self.logout_button = tk.Button(
            self.button_frame, text="Logout", command=self.logout
        )
        self.logout_button.grid(row=0, column=2, padx=5, pady=5)

        # Red and Green Light Labels
        self.red_light = tk.Label(self.button_frame, bg="red", width=5, height=2)
        self.red_light.grid(row=0, column=3, padx=5, pady=5)
        self.green_light = tk.Label(self.button_frame, bg="green", width=5, height=2)
        self.green_light.grid(row=0, column=4, padx=5, pady=5)
        self.green_light.grid()  # Initially show green light
        self.red_light.grid_forget()  # Initially hide red light

        # Data Table Frame
        self.data_frame = tk.Frame(self.window)
        self.data_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=25, pady=5)

        # Table
        self.table = ttk.Treeview(
            self.data_frame,
            columns=(
            "Date", "Time", "Username", "Activity Type", "Duration", "Total Login", "Total Break", "Total Idle Time",
            "Actual Login"),
            show="headings",
        )
        self.table.heading("Date", text="Date")
        self.table.heading("Time", text="Time")
        self.table.heading("Username", text="Username")
        self.table.heading("Activity Type", text="Activity Type")
        self.table.heading("Duration", text="Duration")
        self.table.heading("Total Login", text="Total Login")
        self.table.heading("Total Break", text="Total Break")
        self.table.heading("Total Idle Time", text="Total Idle Time")
        self.table.heading("Actual Login", text="Actual Login")

        # Graph and Quote Frame
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=25, pady=5)

        # Graph Frame
        self.graph_frame = tk.Frame(self.bottom_frame)
        self.graph_frame.pack(side="left", padx=5, pady=5)

        # Create a figure for the graph
        self.fig, self.ax = plt.subplots(figsize=(6, 3))  # Set initial figure size
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Ensure the graph stays within the tool's limit
        self.canvas.get_tk_widget().config(width=600, height=300)  # Set initial canvas size
        self.canvas_size_label = tk.Label(self.graph_frame, text="Graph size: 600x300")
        self.canvas_size_label.pack(side="bottom", padx=5, pady=5)

        # Quote Frame
        self.quote_frame = tk.Frame(self.bottom_frame)
        self.quote_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Quote Label
        self.quote_label = tk.Label(self.quote_frame,
                                    text="Everything you've ever wanted is sitting on the other side of fear",
                                    fg="black")
        self.quote_label.pack(fill="both", expand=True)

        # Start the main event loop
        window.after(0, self.display_random_quote)  # Display initial quote
        window.after(120000, self.display_random_quote_loop)  # Start quote loop after 2 minutes

        # Fetch data from Google Spreadsheet
        self.fetch_data_from_google_sheet()

        # Background process thread (for example)
        self.background_process_thread = threading.Thread(target=self.background_process)
        self.background_process_thread.daemon = True  # Daemonize the thread
        self.background_process_thread.start()  # Start the thread

        import logging

        # Configure logging
        logging.basicConfig(filename='dashboard.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')


        def fetch_data_from_google_sheet(self):
            try:
                # Fetch data from Google Sheet
                username = win32api.GetUserName()
                try:
                    sheet = self.gc.open(username).sheet1
                    values = sheet.get_all_values()
                    self.data = pd.DataFrame(values[1:], columns=values[0])

                    # Update table and graph
                    self.update_table_and_graph()
                except gspread.exceptions.SpreadsheetNotFound:
                    logging.error(f"Google Sheet for user '{username}' not found.")
                    messagebox.showerror("Error", f"Google Sheet for user '{username}' not found.")
                except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError) as e:
                    logging.error(f"Connection error occurred while fetching data: {e}")
                    messagebox.showerror("Error",
                                         "Connection error occurred while fetching data. Please try again later.")
                    self.data = pd.DataFrame(columns=["Date", "Time", "Username", "Activity Type", "Duration"])
                    self.update_table_and_graph()
            except Exception as e:
                # Log any unexpected errors
                logging.error(f"An unexpected error occurred: {e}")
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def start_break_and_update_google_sheet(self):
        # Get the current time
        self.last_activity_time = datetime.datetime.now()

        # Show message box
        messagebox.showinfo("Break Started", "You have started your break.")

        # Update Google Sheets
        username = win32api.GetUserName()
        activity_type = "Start Break"
        self.update_google_sheet(activity_type, username, self.last_activity_time)

        # Disable the Start Break button
        self.start_break_button.config(state=tk.DISABLED)

        # Enable the End Break button
        self.end_break_button.config(state=tk.NORMAL)

        # Update lights
        self.red_light.grid_forget()
        self.green_light.grid(row=0, column=4, padx=5, pady=5)  # Use grid instead of pack

    def end_break_and_update_google_sheet(self):
        current_time = datetime.datetime.now()

        # Calculate duration in seconds
        if self.last_activity_time:
            duration = current_time - self.last_activity_time
            duration_seconds = duration.total_seconds()
            duration_str = f"{int(duration_seconds // 3600)}:{int((duration_seconds // 60) % 60):02d}"  # Format duration as HH:MM
        else:
            duration_seconds = 0  # Default to 0 if no previous activity time is available
            duration_str = "0:00"

        # Show message box with duration
        duration_message = f"Duration: {duration_str} (HH:MM)"
        messagebox.showinfo("Break Ended", f"You have ended your break.\n{duration_message}")
        # Update lights
        self.green_light.pack_forget()
        self.red_light.pack()

        # Update Google Sheets
        username = win32api.GetUserName()
        activity_type = "End Break"
        end_time = current_time

        # Ensure self.last_activity_time is not None
        if self.last_activity_time is not None:
            self.update_google_sheet(activity_type, username, self.last_activity_time, end_time, duration_str)

        # Update last activity time to current time
        self.last_activity_time = current_time

        # Reset last activity time
        self.last_activity_time = None

        # Enable the Start Break button
        self.start_break_button.config(state=tk.NORMAL)

        # Disable the End Break button
        self.end_break_button.config(state=tk.DISABLED)

        # Update lights
        self.red_light.grid_forget()
        self.green_light.grid(row=0, column=4, padx=5, pady=5)

    def logout(self):
        # Run update and destroy process in a separate thread
        threading.Thread(target=self.update_and_destroy).start()

    def update_and_destroy(self):
        # Update Google Sheets before logging out
        self.update_google_sheet("Logout", win32api.GetUserName(), datetime.datetime.now())

        # Close the window
        self.window.destroy()

    def update_google_sheet(self, activity_type, username, start_time, end_time=None, duration_str=None):
        if activity_type != "":
            current_time = datetime.datetime.now()
            date = current_time.strftime("%Y-%m-%d")
            start_time_str = start_time.strftime("%H:%M:%S")

            if end_time:
                end_time_str = end_time.strftime("%H:%M:%S")
                duration_str = str(end_time - start_time)  # Calculate duration if end time is provided
            else:
                end_time_str = ""
                duration_str = ""

            # Find the correct Google Sheet based on username
            try:
                sheet = self.gc.open(username).sheet1
            except gspread.exceptions.SpreadsheetNotFound:
                messagebox.showerror("Error", "Google Sheet for user '{}' not found.".format(username))
                return

            # Update total login duration if it's a login or logout event
            if activity_type in ["Login", "Logout"]:
                self.update_total_login_duration(username, start_time, end_time)

            # Update cumulative break duration if it's a break start or break end event
            elif activity_type in ["Start Break", "End Break"]:
                self.update_cumulative_break_duration(username, start_time, end_time)

            data = [date, start_time_str, username, activity_type, duration_str, str(self.total_login_duration),
                    str(self.cumulative_break_duration)]
            sheet.append_row(data)

    def update_total_login_duration(self, username, start_time, end_time):
        if end_time:
            self.total_login_duration += end_time - start_time

    def update_cumulative_break_duration(self, username, start_time, end_time):
        if start_time and end_time:
            self.cumulative_break_duration += end_time - start_time

    def fetch_data_from_google_sheet(self):
        # Fetch data from Google Sheet
        username = win32api.GetUserName()
        try:
            sheet = self.gc.open(username).sheet1
            values = sheet.get_all_values()
            self.data = pd.DataFrame(values[1:], columns=values[0])

            # Update table and graph
            self.update_table_and_graph()
        except gspread.exceptions.SpreadsheetNotFound:
            messagebox.showerror("Error", "Google Sheet for user '{}' not found.".format(username))
        except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError) as e:
            messagebox.showerror("Error", "Connection error occurred while fetching data. Please try again later.")
            self.data = pd.DataFrame(columns=["Date", "Time", "Username", "Activity Type", "Duration"])
            self.update_table_and_graph()

    def update_table_and_graph(self):
        # Update table with fetched data
        self.table.delete(*self.table.get_children())
        for index, row in self.data.iterrows():
            # Check if 'Date' column exists before accessing it
            date = row.get('Date', 'N/A')
            time = row.get('Time', 'N/A')
            username = row.get('Username', 'N/A')
            activity_type = row.get('Activity Type', 'N/A')
            duration = row.get('Duration', 'N/A')
            total_login = row.get('Total Login', 'N/A')
            total_break = row.get('Total Break', 'N/A')
            total_idle_time = row.get('Total Idle Time', 'N/A')
            actual_login = row.get('Actual Login', 'N/A')
            self.table.insert("", "end", values=(date, time, username, activity_type, duration,
                                                 total_login, total_break, total_idle_time, actual_login))

        # Update graph with fetched data
        if not self.data.empty:
            # Clear existing plot
            self.ax.clear()

            # Plot the graph (example)
            self.ax.plot(self.data['Date'], self.data['Duration'])  # Plotting Duration for example

            # Customize graph appearance if needed
            self.ax.set_xlabel('Activity Type')
            self.ax.set_ylabel('Duration')
            self.ax.set_title('Activity Duration')

            # Draw the plot on the canvas
            self.canvas.draw()

    def display_random_quote_loop(self):
        self.display_random_quote()
        self.window.after(120000, self.display_random_quote_loop)

    def display_random_quote(self):
        url = "https://zenquotes.io/api/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            quote = f"{data[0]['q']} - {data[0]['a']}"  # Combine quote and author
            # Display quote on the GUI
            self.quote_label.config(text=quote)
        else:
            quote = "Failed to retrieve quote."
            self.quote_label.config(text=quote)

    def init_google_sheet(self):
        # Google Sheets credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('',
                                                                       scope)
        self.gc = gspread.authorize(credentials)

    def background_process(self):
        while True:
            try:
                # Perform background process tasks here
                # Placeholder for other background process tasks

                # Example: Print a message every 5 seconds
                print("Background process running...")

                # Simulate an error for demonstration
                # Uncomment the line below to simulate an error
                # raise Exception("Simulated error in background process")

                # Example: Log the background process activity
                logging.info("Background process running...")

                # Example: Send a notification about the background process
                self.send_notification("Background process is running")

            except Exception as e:
                # Handle any exceptions gracefully
                logging.error(f"Error in background process: {e}")

            # Add a delay to prevent CPU usage
            time.sleep(5)  # Sleep for 5 seconds

    def send_notification(self, message):
        # Placeholder for sending notifications
        print(f"Notification: {message}")

# For testing
if __name__ == "__main__":
    window = tk.Tk()
    Dashboard(window)
    window.mainloop()

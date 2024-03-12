# Employee Monitor
The Crystalvoxx Employee Monitor is a comprehensive tool designed to enhance productivity and ensure transparency in the workplace. It offers a range of features that provide valuable insights into employee activities during work hours. Key features include user authentication, idle time monitoring, activity tracking, break monitoring, and employee management. This tool is designed with a focus on user privacy and data security, ensuring that all monitoring is done ethically and in compliance with relevant regulations.

#Features
User Authentication: Secure login system to authenticate users.
Idle Time Monitoring: Tracks and logs idle time to identify unproductive periods.
Activity Tracking: Records user activity to monitor work progress.
Break Monitoring: Tracks break periods to ensure adherence to company policies.
Employee Management: Manages employee data and activity logs for effective monitoring.
Data Storage: Stores employee activity data in Google Sheets for easy access and analysis.
Requirements
Python 3.x
pandas~=2.2.1
matplotlib~=3.8.3
requests==2.26.0
gspread==4.0.1
urllib3==1.26.7
oauth2client==4.1.3
datetime==4.3
pywin32~=306
pynput==1.7.3
Pillow~=10.2.0
logging~=0.4.9.6
google-api-python-client~=2.120.0
Installation
Clone the repository to your local machine:

#bash
Copy code
git clone https://github.com/your_username/Crystalvoxx-Employee-Monitor.git
Navigate to the project directory:

#bash
Copy code
cd Crystalvoxx-Employee-Monitor
Install the required dependencies:

#bash
Copy code
pip install -r requirements.txt
Usage
Ensure all dependencies are installed.

Run the main script to start the Employee Monitor:

bash
Copy code
python main.py
Log in with your credentials.

The Employee Monitor will start tracking your activities and providing insights into your work habits.

#Data Storage
Employee activity data is stored in Google Sheets, allowing for easy access and analysis. Each employee has their own Google Sheet where their activity logs are recorded.
Python Files
main.py
The main entry point of the Crystalvoxx Employee Monitor. This script initializes the user interface, handles user authentication, and coordinates the monitoring process.

#dashboard.py
Responsible for creating the user interface of the Employee Dashboard. It contains functions to start and end breaks, fetch data from Google Sheets, update the dashboard table and graph, and handle background processes.

#bg.py
Implements background monitoring functionality, including tracking idle time and updating Google Sheets with idle time data. This script runs as a separate background process to continuously monitor user activity.

#Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

#License
This project is licensed under the MIT License - see the LICENSE file for details.

#Acknowledgments
This project was inspired by the need for transparent employee monitoring solutions in modern workplaces.

from setuptools import setup, find_packages

setup(
    name='Crystalvoxx employee monitor',
    version='0.1',
    description='''The Crystalvoxx Employee Monitor is a comprehensive tool designed to enhance productivity and 
    ensure transparency in the workplace. It offers a range of features that provide valuable insights into employee 
    activities during work hours. Key features include user authentication, idle time monitoring, activity tracking, 
    break monitoring, and employee management. This tool is designed with a focus on user privacy and data security, 
    ensuring that all monitoring is done ethically and in compliance with relevant regulations.''',
    packages=find_packages(),
    install_requires=[
        'time',
        'tkinter',
        'pandas',
        'matplotlib',
        'requests',
        'gspread',
        'urllib3',
        'oauth2client',
        'datetime',
        'logging',
        'pywin32',
        'pynput',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'monitor=your_main_script:main',
        ],
    },
    author='Kapil Kumar',
    author_email='Kapil.k@crystalvoxx.com',
    url='
)

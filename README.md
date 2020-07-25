Dependencies: Python 2.7+

Packages:

requests

bs4 

pandas

time

datetime

openpyxl 

numpy 

os

wordcloud

Usage: 

*IMPORTANT!!*

Edit your local copy of scrape_stats.py to include your username (NOT email address!) and password into the 'login' dictionary (lines 159 and 160)

Ex:

    login_data = {
    'username': 'your_username NOT email',
    'password': 'your_password'
    }
    
becomes:

    login_data = {
    'username': 'a_fake_username',
    'password': '@fakePA$$w0rd'
    }

Edit your local copy of scrape_stats.py to include the FULL PATH (unless you plan on running this from the same directory every time) and name of the spreadsheet you want to write the data to. Path can be found by typing pwd into a terminal.

Ex:

    xls_file='/path/to/file/filename.xlsx'
    
becomes:

    xls_file='/Users/my_computer_name/Documents/my_folder/my_stats.xlsx'
    
To run:

From the command line, type:

python scrape_stats.py

Extra: Make it a cron job!

Using python: https://stackabuse.com/scheduling-jobs-with-python-crontab/

On OSX Catalina.... coming soon to the wiki


Plots:

Basic example in wiki

GUI coming soon 

# Project Title: "HR Connect: Automated Email Communication and Data Scraping System"

## Description
This project is an automated system for mass email communication. It uses Python and Selenium WebDriver for email automation. The system reads email addresses from a file, composes an email using a predefined template, and sends the email. It also keeps track of the emails that have been sent to avoid sending duplicate emails.

## Getting Started

### Dependencies
* Python
* Selenium WebDriver
* Chrome Browser

### Installing
* Install Python from [Python's official site](https://www.python.org/downloads/)
* Install Selenium WebDriver using pip:
  ```
  pip install selenium
  ```
* Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and add it to your system PATH.

### Executing Program
* Update the `username` and `password` variables in the script with your ProtonMail login credentials.
* Update the `documents/emails.txt` file with the email addresses you want to send emails to.
* Update the `documents/emailtemplate.txt` file with the email content you want to send.
* Include your `resume.pdf` in the `documents` directory and update the directory name in the Python script if necessary.
* Run the script:
  ```
  python sendmail.py
  ```

## Help
If you encounter any problems or have any questions about this project, please open an issue in this repository.


## Acknowledgments
* [Selenium WebDriver](https://www.selenium.dev/documentation/en/webdriver/)
* [Python](https://www.python.org/)
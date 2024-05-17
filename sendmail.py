import time
import datetime
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
username = "creds"
password = "creds"


logging.basicConfig(filename='documents/logs.log', level=logging.INFO, format='%(message)s')



# Start a Chrome instance
driver = webdriver.Chrome()
# Navigate to ProtonMail login page
driver.get('https://account.proton.me/login')
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'username')))
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
# Click on the 'Sign in' button
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(15)
# Navigate to the inbox
driver.get('https://mail.proton.me/u/0/inbox')
# Wait for the inbox to load
time.sleep(7)
# Read log file and store the emails sent 
sent_emails = set()
with open('documents/logs.log', 'r') as f:
    lines = f.readlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            sent_emails.add(stripped_line)

print(sent_emails)
# Read the email ids from the file
with open('documents/emails.txt', 'r') as f:
    lines = f.readlines()
# Read the email template
with open('documents/emailtemplate.txt', 'r') as f:
    email_template = f.read()


print(lines)
try:
    for line in lines:
        print(line)
        email, *greeting = line.strip().split('-')
        email = email.strip()
        print(email, greeting)
        if email in sent_emails:
            print(f'Skipping {email} because it has already been sent.')
            continue
        greeting = "Hello " + (greeting[0] if greeting else ' there')
        # greeting = greeting[0] if greeting else 'Hello there'
        email_body = f'{greeting},<br><br>{email_template}'

        time.sleep(1)
        xpath_new_message = "/html/body/div[1]/div[3]/div/div[2]/div/div[1]/div[2]/button";
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_new_message)))
        new_message_button = driver.find_element(By.XPATH, xpath_new_message)
        new_message_button.click()
        # Fill in the recipient's email address but keeping edge case that numerical id is not static and can change eg. to-composer-6910 - 6910 is dynamic
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id^='to-composer-']")))
        email_input = driver.find_element(By.CSS_SELECTOR, "input[id^='to-composer-']")
        email_input.send_keys(email)
        # Fill in the subject but keeping edge case that numerical id is not static and can change eg. subject-composer-6831 - 6831 is dynamic
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id^='subject-composer-']")))
        subject_input = driver.find_element(By.CSS_SELECTOR, "input[id^='subject-composer-']")
        subject_input.send_keys('Job Application')

        # --------------------------------------------------------------
        greeting = greeting.replace('"', '\\"')
        time.sleep(5)

        # Attach the resume
        upload_file = os.path.abspath('documents/Resume.pdf')
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(upload_file)

        # Locate the iframe
        xpath_iframe = "/html/body/div[1]/div[4]/div/div/div/div/section/div/div[1]/div[1]/div/iframe"
        iframe = driver.find_element(By.XPATH, xpath_iframe)
        # Switch to the iframe
        driver.switch_to.frame(iframe)
        # Now you can interact with the elements inside the iframe
        rooster_editor = driver.find_element(By.XPATH, "//*[@id=\"rooster-editor\"]")
        #driver.execute_script("var ele=arguments[0]; ele.innerHTML = '<div>" + greeting + ",<br>I want to apply for a java developer role.<br>I have attached my resume. Please check and refer me.<br>Regards,<br>XYZ</div>';", rooster_editor)
        driver.execute_script("var ele=arguments[0]; ele.innerHTML = arguments[1];", rooster_editor, email_body)
        driver.switch_to.default_content()
        # Send the email by clicking the 'Send' button of below xpath
        xpath_send = "/html/body/div[1]/div[4]/div/div/div/footer/div/div[1]/button[1]";
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_send)))
        send_button = driver.find_element(By.XPATH, xpath_send)
        send_button.click()
        print('Email sent to', email)
        logging.info(f'\n{email}')
        sent_emails.add(email)
        # Wait for the email to be sent
        time.sleep(10)
        print('Done......')
except Exception as e:
    print(e)
    # logging.error(f'Error: {e}')

# Close the browser
driver.quit()
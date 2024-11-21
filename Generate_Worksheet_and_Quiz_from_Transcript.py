import os
import google.generativeai as genai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def prompt_genai(prompt):
    text = ''
    load_dotenv() # Load variables from .env
    api_key = os.getenv("API_KEY")  # Access the API key
    genai.configure(api_key=api_key) # Replace with your own Gemini API Key
    model = genai.GenerativeModel("gemini-1.5-flash")
    responses = model.generate_content([prompt])
    for response in responses:
        text += ' ' + response.text
    
    return text

def create_Webdriver_for_Google_Forms():
    driver = webdriver.Chrome(executable_path='C:\\webdriver\\chromedriver.exe')
    driver.get("https://docs.google.com/forms/u/0/")
    time.sleep(3)

    driver.find_element(By.XPATH, '//div[@class="docs-homescreen-templates-templateview-preview docs-homescreen-templates-templateview-preview-island"]/div').click()
    time.sleep(3)

    title_input = driver.find_element(By.XPATH, '//*[@aria-label="Form title"]')
    title_input.send_keys("Sample Form Title")
    description_input = driver.find_element(By.XPATH, '//*[@aria-label="Form description"]')
    description_input.send_keys("This is a sample form description.")
    question_input = driver.find_element(By.XPATH, '//*[@aria-label="Question title"]')
    question_input.send_keys("What is your name?")
    time.sleep(2)

    send_button = driver.find_element(By.XPATH, '//*[@aria-label="Send form"]')
    send_button.click()
    time.sleep(3)

    driver.quit()


if __name__ == "__main__":
    print(prompt_genai("hello"))
    create_Webdriver_for_Google_Forms()



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import os

class Utils():
    def get_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless=old')
        chrome_options.add_argument('--disable-web-security')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def read_json_file(self, filepath):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(current_dir, "..", "static", filepath)
            full_path = os.path.normpath(full_path)

            with open(full_path, 'r') as file:
                data = json.load(file)
                return data
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


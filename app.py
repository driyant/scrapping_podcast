# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random import choice
from art import art

class Scrapping():
  print(f"{art}")
  print("Enter desired podcast url. E.g: https://podcasts.apple.com/us/podcast/xxxxxxxx/idxxxxxxxx \n")
  # Uncomment this line and select the path of chrome driver
  # path = r"C:\\YOUR_PATH_FOLDER_HERE\\chromedriver.exe" #
  user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
  ]
  prompt_url = input("Enter url podcasts apple below ⬇: \n")
  titles = []
  links = []
  dates = []
  descriptions = []
  durations = []
  
  def __init__(self):
    # Uncomment this line if you prefer to open browser locally
    # self.driver = webdriver.Chrome(executable_path=self.path)
    # self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    
    self.chrome_options = Options()
    self.chrome_options.add_experimental_option("detach", True)
    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
  def starting_machine(self, url):
    print("============= Opening Browser =============")
    if not self.prompt_url:
      print("URL is required to launch this app")
      print("Exit the program")
      exit()
    self.driver.get(url)
    time.sleep(1)
    print("============= Starting The Engine Machine On =============")
    time.sleep(1)
    self.driver.maximize_window()
    time.sleep(1)
    print("============= DON'T CLOSE THE BROSER - THIS IS VERY IMPORTANT =============")
    time.sleep(1)
    print("============= PLEASE WAIT =============")
    try:
      btn_load_more = self.driver.find_element(By.XPATH, '/html/body/div[3]/main/div[2]/div/section[1]/div/div[2]/div[4]/div/div/button')
      while btn_load_more:
        btn_load_more.click()
    except Exception as e:
      print('Load more does not exist!')
    finally:
      print("============= SAVING SOURCE FILE =============")
      # Get Title
      title = self.driver.find_element(By.CSS_SELECTOR, "h1 > span.product-header__title").text
      time.sleep(1)
      # Get Page Source
      page_source = self.driver.page_source
      # Save it to html
      with open(f"{title.lower().replace(' ', '-')}.html", "w", encoding='utf8') as file_w:
        file_w.write(page_source)
      # Opening File
      with open(f"{title.lower().replace(' ', '-')}.html", "r", encoding='utf8') as file_r:
        contents = file_r.read()
      soup = BeautifulSoup(contents, 'html.parser')
      print("============= BEGINS SCRAPPING =============")
      time.sleep(1)
      print("============= GETTING TITLES =============")
      # Get Titles
      get_titles = soup.find_all("a", class_="link tracks__track__link--block")
      self.titles = [ x.getText().strip() if x else "-" for x in get_titles ]
      time.sleep(1)
      print("============= GETTING LINKS =============")
      # Get Links
      get_links = soup.find_all("a", 'link tracks__track__link--block')
      self.links = [x.get("href") if x else "-" for x in get_links ]
      time.sleep(1)
      print("============= GETTING DATES =============")
      # Get Date
      get_dates = soup.find_all("time", {
        "class" : "",
        "data-test-we-datetime" : ""
      })
      self.dates = [ x.getText() for x in get_dates ]
      # Get Description 
      get_desc = soup.find_all("div", {
          'class' : 'we-clamp we-clamp--visual',
          'style' : '--clamp-lines: 3'
        })
      self.descriptions = [ x.getText().strip() if x else "-" for x  in get_desc ]
      time.sleep(1)
      print("============= GETTING DURATIONS =============")
      # Get Durations
      get_durations = soup.find_all("li", class_="inline-list__item inline-list__item--margin-inline-start-small")      
      self.durations = [x.getText().strip() if x else "-" for x in get_durations]
      print("============= FINISH SCRAPPING =============")
      print("============= GETTING THE RESULT =============")
      time.sleep(3)
      print(f"title: {len(self.titles)} items, date: {len(self.dates)} items, duration: {len(self.durations)} items, link: {len(self.links)} items, description: {len(self.descriptions)} items")   
      print("============= GETTING OUTPUT FILES =============")
      data_to_dict = dict(title=self.titles, duration=self.durations, date=self.dates,link=self.links, description=self.descriptions)
      df = pd.DataFrame({ k: pd.Series(v) for k, v in data_to_dict.items() })
      # Generating to excel
      print("============= GENERATING INTO EXCEL FORMAT =============")
      try:
        df.to_excel(f"podcast_{title.lower().replace(' ', '-')}.xlsx")
        print(f"Filename is : podcast_{title.lower().replace(' ', '-')}.xlsx has been generated successfully!")
      except Exception as e:
        print(f"Something went wrong! When tying to generate excel format {e}")
      # Generating to csv
      print("============= GENERATING INTO CSV FORMAT =============")
      try:
        df.to_csv(f"podcast_{title.lower().replace(' ', '-')}.csv", index=True)
        print(f"Filename is : PODCAST_{title.lower().replace(' ', '-')}.csv has been generated successfully!")
      except Exception as e:
        print(f"Something went wrong! When trying to generate csv format {e}")
      self.driver.quit()
      print("============= PROGRAM EXIT =============")
      exit()
if __name__ == "__main__": 
  dvr = Scrapping()
  dvr.starting_machine(dvr.prompt_url)
  

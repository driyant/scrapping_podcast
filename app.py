from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
import pandas as pd
from bs4 import BeautifulSoup
from random import choice
from art import art
from spinner import Spinner

class Scrapping():
  print(f"{art}")
  print("Enter desired podcast URL. E.g: https://podcasts.apple.com/us/podcast/xxxxxxxx/idxxxxxxxx \n")
  user_agents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
  ]
  prompt_url = input("Enter URL podcasts apple below ⬇ \n")
  titles = []
  links = []
  dates = []
  descriptions = []
  durations = []
  def __init__(self):
    self.chrome_options = Options()
    self.chrome_options.add_experimental_option("detach", True)
    self.chrome_options.add_argument("--disable-gpu")
    self.chrome_options.add_argument("--headless")
    self.chrome_options.add_argument("--window-size=1920x1080")
    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)
  def start(self, url):
    if not self.prompt_url:
      print("URL is required to launch this app")
      print("Exit the program")
      exit()
    spinner = Spinner("STARTING THE ENGINE 🔥")
    spinner.start()
    self.driver.get(url)
    time.sleep(1)
    spinner.stop()
    # self.driver.maximize_window()
    spinner = Spinner("PLEASE WAIT")
    spinner.start()
    try:
      while True:
        btn_load_more = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/main/div[2]/div/section[1]/div/div[2]/div[4]/div/div/button"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", btn_load_more)
        btn_load_more.click()
        time.sleep(3)
    except Exception as e:
      print('\n✨ LOAD MORE DOES NOT EXIST!')
      spinner.stop()
    finally:
      spinner = Spinner("SAVING SOURCE FILE")
      spinner.start()
      # Get Title
      title = self.driver.find_element(By.CSS_SELECTOR, "h1 > span.product-header__title").text
      time.sleep(1)
      # Get Page Source
      page_source = self.driver.page_source
      # Save it to HTML
      with open(f"{title.lower().replace(' ', '-')}.html", "w", encoding='utf8') as file_w:
          file_w.write(page_source)
      self.driver.quit()
      spinner.stop()
      # Opening File
      with open(f"{title.lower().replace(' ', '-')}.html", "r", encoding='utf8') as file_r:
          contents = file_r.read()
      soup = BeautifulSoup(contents, 'html.parser')
      spinner = Spinner("BEGINS SCRAPPING")
      spinner.start()
      time.sleep(2)
      spinner.stop()
      spinner = Spinner("GETTING TITLES")
      spinner.start()
      # Get Titles
      get_titles = soup.find_all("a", class_="link tracks__track__link--block")
      self.titles = [x.getText().strip() if x else "-" for x in get_titles]
      time.sleep(2)
      spinner.stop()
      spinner = Spinner("GETTING LINKS")
      spinner.start()
      # Get Links
      get_links = soup.find_all("a", 'link tracks__track__link--block')
      self.links = [x.get("href") if x else "-" for x in get_links]
      time.sleep(2)
      spinner.stop()
      spinner = Spinner("GETTING DATES")
      spinner.start()
      # Get Date
      get_dates = soup.find_all("time", {
          "class": "",
          "data-test-we-datetime": ""
      })
      self.dates = [x.getText() for x in get_dates]
      # Get Description
      get_desc = soup.find_all("div", {
          'class': 'we-clamp we-clamp--visual',
          'style': '--clamp-lines: 3'
      })
      self.descriptions = [x.getText().strip() if x else "-" for x in get_desc]
      time.sleep(2)
      spinner.stop()
      spinner = Spinner("GETTING DURATIONS")
      spinner.start()
      # Get Durations
      get_durations = soup.find_all("li", class_="inline-list__item inline-list__item--margin-inline-start-small")
      self.durations = [x.getText().strip() if x else "-" for x in get_durations]
      time.sleep(2)
      spinner.stop()
      spinner = Spinner("FINISH SCRAPPING")
      spinner.start()
      time.sleep(3)
      spinner.stop()
      spinner = Spinner("GETTING THE RESULT")
      spinner.start()
      print(f"\n Total Title: {len(self.titles)} items, Total Date: {len(self.dates)} items, Total Duration: {len(self.durations)} items, Total Link: {len(self.links)} items, Total Description: {len(self.descriptions)} items")
      spinner.stop()
      time.sleep(2)
      data_to_dict = dict(title=self.titles, duration=self.durations, date=self.dates, link=self.links, description=self.descriptions)
      df = pd.DataFrame({k: pd.Series(v) for k, v in data_to_dict.items()})
      try:
        # Generating to excel
        spinner = Spinner("GENERATING INTO EXCEL FORMAT")
        spinner.start()
        df.to_excel(f"podcast_{title.lower().replace(' ', '-')}.xlsx")
        print(f"\n Filename: podcast_{title.lower().replace(' ', '-')}.xlsx has been generated successfully!")
      except Exception as e:
        print(f"Something went wrong! When tying to generate excel format {e}")
      finally:
        spinner.stop()
      try:
        spinner = Spinner("GENERATING INTO CSV FORMAT")
        spinner.start()
        # Generating to csv
        df.to_csv(f"podcast_{title.lower().replace(' ', '-')}.csv", index=True)
        print(f"\n Filename: PODCAST_{title.lower().replace(' ', '-')}.csv has been generated successfully!")
      except Exception as e:
        print(f"Something went wrong! When trying to generate csv format {e}")
      finally:
        spinner.stop()
        print("✨ PROGRAM EXIT")
        exit()
      
if __name__ == "__main__": 
  dvr = Scrapping()
  dvr.start(dvr.prompt_url)
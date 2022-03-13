from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

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
  def __init__(self):
    # Uncomment this line if you prefer to open browser locally
    # self.driver = webdriver.Chrome(executable_path=self.path)
    self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    
  def driver_get(self, url):
    self.driver.get(url)
  
if __name__ == "__main__": 
  d = Scrapping()
  d.driver_get(d.prompt_url)
  print("============= Starting The Engine Machine On =============")
  time.sleep(1)
  d.driver.maximize_window()
  time.sleep(1)
  print("============= Opening The Browser =============")
  time.sleep(1)
  print("============= DON'T CLOSE THE BROSER - THIS IS VERY IMPORTANT =============")
  time.sleep(1)
  print("Begins......")
  time.sleep(1)
  print("============= PLEASE WAIT =============")
  btn_xpathc = d.driver.find_elements(By.XPATH, '/html/body/div[5]/main/div[2]/div/section[1]/div/div[2]/div[4]/div/div/button')
  count_btns = len(btn_xpathc)
  try:
    while count_btns > 0:
      btn_path = d.driver.find_element(By.XPATH, '/html/body/div[5]/main/div[2]/div/section[1]/div/div[2]/div[4]/div/div/button')
      btn_path.click()
      time.sleep(3)
  except Exception as e:
    print("It's fully loaded, button does not exist!")
  finally:
    try:
      get_the_url = d.prompt_url
      title = get_the_url.split("/")[-2]
      print("Trying to save data source.............")
      # Get Page Source
      page_source = d.driver.page_source
      # Save it to html
      with open(f"{title.lower().replace(' ', '-')}.html", "w", encoding='utf8') as file_w:
        file_w.write(page_source)
      # Opening File
      with open(f"{title.lower().replace(' ', '-')}.html", "r", encoding='utf8') as file_r:
        contents = file_r.read()
      soup = BeautifulSoup(contents, 'html.parser')
      # Get Titles
      get_titles = soup.find_all("a", class_="link tracks__track__link--block")
      titles = [ x.getText().strip() for x in get_titles ]
      # Get Links
      get_links = soup.find_all("a", 'link tracks__track__link--block')
      links = [x.get("href") for x in get_links ]
      # Get Date
      get_dates = soup.find_all("time", {
        "class" : "",
        "data-test-we-datetime" : ""
      })
      dates = [ x.getText() for x in get_dates ]
      # Get Description 
      get_desc = soup.find_all("div", {
          'class' : 'we-clamp we-clamp--visual',
          'style' : '--clamp-lines: 3'
        })
      descs = [ x.getText().strip() for x in get_desc ]
      # Get Durations
      get_durations = soup.find_all("li", class_="inline-list__item inline-list__item--margin-inline-start-small")      
      durations = [ x.getText().strip() for x in get_durations ]
      print("Finish Scrapping...............")
      print("Getting the result ............")
      time.sleep(3)
      print(f"title: {len(titles)} items, date: {len(dates)} items, duration: {len(durations)} items, link: {len(links)} items, description: {len(descs)} items")   
      # Checking
      len_titles_invalid = len(titles) != len(dates) or len(titles) != len(dates) or len(titles) != len(durations) or len(titles) != len(links) or len(titles) != len(descs)
      len_dates_invalid = len(dates) != len(titles) or len(dates) != len(durations) or len(dates) != len(links) or len(titles) != len(descs)
      len_durations_invalid = len(durations) != len(titles) or len(durations) != len(dates) or len(durations) != len(links) or len(durations) != len(descs)
      len_links_invalid = len(links) != len(titles) or len(links) != len(dates) or len(links) != len(durations) or len(links) != len(descs)
      len_desc_invalid = len(descs) != len(titles) or len(descs) != len(dates) or len(descs) != len(durations) or len(descs) != len(links)
      if len_titles_invalid or len_dates_invalid or len_durations_invalid or len_links_invalid or len_desc_invalid:
        print("> Total items are the the same, which means there must be something missing element")
        print("> Suggestion : You might want to double check the result.................")
      time.sleep(1)
      try:
        # data_to_dict = dict(title=titles)
        print("Plase wait generating the output files......................")
        data_to_dict = dict(title=titles, duration=durations, date=dates,link=links, description=descs)
        df = pd.DataFrame({ k: pd.Series(v) for k, v in data_to_dict.items() })
        # Generating to excel
        print("Generating into excel format................")
        try:
          df.to_excel(f"podcast_{title}.xlsx")
          print(f"Filename is : podcast_{title}.xlsx has been generated successfully!")
        except Exception as e:
          print(f"Something went wrong! When tying to generate excel format {e}")
          d.driver.quit()
        # Generating to csv
        print("Generating into csv format..................")
        try:
          df.to_csv(f"podcast_{title}.csv", index=True)
          print(f"Filename is : podcast_{title}.csv has been generated successfully")
        except Exception as e:
          print(f"Something went wrong! When trying to generate csv format {e}")
          d.driver.quit()
      except Exception as e:
        print(f"Ups sorry, something went wrong! {e}")
        print(f"Suggestion : Please try again with another podcast url")
        print("Exit the program......")
        d.driver.quit()
        exit()
      print("Thank you, quitting the program....")
      d.driver.quit()
      exit()
    except Exception as e:
      print(f"Something went wrong! {e}")
      d.driver.quit()
      exit()

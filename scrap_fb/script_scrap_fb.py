
import pymongo
import datetime
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import random
PATH = "C:\Program Files (x86)\chromedriver.exe"

with open("C:/Users/Youssef/Documents/MyCode/scrap_fb/Configurations_fb.txt") as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]    
    
def hachage(ch):
    h = hashlib.new('ripemd160')
    h.update(ch.encode('utf-8'))
    ch1= h.hexdigest()
    return(ch1)

def _login(browser, email, password):
    '''
    This function allow you to login in Facebook .
    :param browser : this is an instance of webdriver
    :param email : this is an email Facebook
    :param password : this is a password account

    '''
    #browser.maximize_window()
    browser.find_element_by_id("email").send_keys(email)
    time.sleep(random.randint(4,7))
    browser.find_element_by_name("pass").send_keys(password)
    time.sleep(random.randint(4,7))
    browser.find_element_by_name("login").click()
    time.sleep(random.randint(4,7))

    
#fonction scraping fb    
def Scrap_facebook(page,nb_scroll):
      option = Options()
      option.add_argument("--disable-infobars")
      option.add_argument("start-maximized")
      option.add_argument("--disable-extensions")


      option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
      }) 
      browser = webdriver.Chrome(PATH, options=option)
      browser.get("https://www.facebook.com/")
      
      _login(browser, EMAIL, PASSWORD)
      time.sleep(random.randint(8,12))
      browser.get(page)
      nom_page=page.split('/')[3]
      print(nom_page)
      time.sleep(random.randint(6,9))
      _scroll(browser, False,nb_scroll)  # contient une parametre !!!!!!!!!!!!!!
      
      time.sleep(4)
      #avoir le code source du page
      source_data = browser.page_source
      bs_data = bs(source_data, 'html.parser')
      with open('./bs.html',"w", encoding="utf-8") as file:
        file.write(str(bs_data.prettify()))
      #list_html contient tous les posts trouvés
      list_html = bs_data.find_all(class_="story_body_container")
      data=dict()
      data['posts']= list()
      l= data['posts']
      #pour chaque post on extrait leur info
      for i in list_html:
        #    data["_id"]=hachage(page)
           data['url']=page
           data['scraping_date'] = datetime.datetime.now()
           post = dict()
           post["post_url"] =extract_url_post(i);
           post["post_date"]=extract_post_date(i);
        
           l.append(post)
           
      browser.close()
      return(data)




# extraire l'url de la post
def extract_url_post (post):
    urls = post.find("div",class_= "_52jc _5qc4 _78cz _24u0 _36xo")
    cible = urls.find("a")
    url = "https://m.facebook.com" + str(cible["href"])
    return url

def extract_post_date(post):
    div = post.find(class_="_52jc _5qc4 _78cz _24u0 _36xo")
    if div :
            dat = div.text
            
            return(dat)


def _scroll(browser, infinite_scroll, lenOfPage):
    lastCount = -1
    
    while (lenOfPage > lastCount):   
        time.sleep(random.randint(1,4))
        lastCount += 1
        browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        time.sleep(random.randint(1,3))
        
            


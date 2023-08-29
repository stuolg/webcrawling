import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re



def extract_articles():
    chromeDriver = "/Users/ijeonghwan/chromedriver"
    driver = webdriver.Chrome(chromeDriver)
    driver.get("https://techcrunch.com/?guccounter=10&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAIOMuxTfblbgU-rHrfLYFfJ-MwlUMSCCnSsUYvyOIiLG3bKT00cW3CHQErI_QOXXME6iI9LMbeO5bPOZ_6N1buuqRIA8p1YRGHXCW2fusxLpeL1iUZvqbUrn3_d398MqFJJsp_VQD_wQ8vScpalVnBCERuCmExorQf9qehHyxQTC")
    loadmore = driver.find_element_by_class_name("load-more ")

    articles =[]
    page=1
    # 정규 표현식 : 필요한 단어 키워드 추가, 대문자 소문자 구분 없앰
    keyword = re.compile("tiktok|iqiyi|tencent|viki|prime video|amazon tv|fire tv|firetv|hulu|apple tv|hbo now|youtube|netflix|twitch|hotstar|disney|disney+|disney plus|disney +|disneyplus|streaming|stream|thailand|wetv|we tv|vod|avod|svod|ott|video|ad|advertising|advertise|tv|cord cutter",re.IGNORECASE)

    src = driver.page_source
    #가져온 html 소스를 뷰티풀숲으로 객채화
    soup_more_load = BeautifulSoup(src, 'html.parser')
    #기사 div box 모두 찾기
    soup_more_load_article=soup_more_load.find_all("article", {"class": "post-block"})
    #기사 div box 마지막 기사 전체 정보 가져오기
    last_article = soup_more_load_article[-1]
    #기사 div box 마지막 기사 날짜 정보 가져오기
    date_check = last_article.find("div", {"class": "post-block__meta"}).find("div", {"class": "river-byline__full-date-time__wrapper"}).get_text()


    while True :
        #마지막 기사 날짜 정보에서 February가 있는 경우 멈춤
        if "April " in date_check:
            break

        #그렇지 않은 경우, 반복문으로 페이지 로딩 지속시키기 / 2월 까지 기사까지 페이지 로드 완료, -> 모든 기사 box 리스트로 가져옴
        else :
            src = driver.page_source
            soup_more_load = BeautifulSoup(src, 'html.parser')
            #driver.execute_script("document.getElementsByClassName('announcement-banner-wrapper')[0].style.display='none';")

            loadmore.click()
            print("loading page, "+str(page))
            page+=1
            time.sleep(3)
            driver.implicitly_wait(3)
            # 기사 div box 모두 찾기
            soup_more_load_article = soup_more_load.find_all("article", {"class": "post-block"})
            # 기사 div box 마지막의 날짜 정보 가져오기
            last_article = soup_more_load_article[-1]
            date_check=last_article.find("div", {"class": "post-block__meta"}).find("div", {"class": "river-byline__full-date-time__wrapper"}).get_text()
            ##print(last_article)
            ##print(date_check)

    for article in soup_more_load_article :
        article_title = article.find("header", {"class": "post-block__header"}).find("h2", {"class": "post-block__title"}).get_text()

        if keyword.match(article_title) :      #article_title.find(search[i]):
            article_date = article.find("div", {"class": "post-block__meta"}).find("div", {"class": "river-byline__full-date-time__wrapper"}).get_text()
            article_link = "techcrunch.com" + article.find("header", {"class": "post-block__header"}).find("a")["href"]
            load = {
                "title": article_title,
                "date": article_date,
                "link": article_link
            }
            articles.append(load)
    driver.close()
    return (articles)

'''
time.sleep(3)
driver.implicitly_wait(3)
'''

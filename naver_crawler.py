from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
# 브라우저 생성
browser = webdriver.Chrome('C:/chromedriver.exe')

# 웹 사이트 열기
browser.get('https://www.naver.com')
browser.implicitly_wait(10) # 로딩이 끝날 때 까지 10초 동안 기다려 줌

# 쇼핑 메뉴 클릭
browser.find_element_by_css_selector('a.nav.shop').click()
time.sleep(2)
# 검색 창 클릭
search = browser.find_element_by_css_selector('input.co_srh_input._input')
search.click()

# 검색어 입력
search.send_keys('옷')
search.send_keys(Keys.ENTER)

# 파일 생성
f = open(r"C:\Users\kym59\Desktop\창업\크롤러\data.csv", 'w', encoding='CP949', newline='')
csvWriter = csv.writer(f)

# 20페이지 정도
for n in range(1, 20):
    time.sleep(1)
    # 스크롤 전 높이
    before_h = browser.execute_script("return window.scrollY")

    # 무한 스크롤
    while True:
        # 맨 아래로 스크롤을 내린다.
        browser.find_element_by_css_selector("body").send_keys(Keys.END)

        # 스크롤 사이 페이지 로딩 시간
        time.sleep(1)

        # 스크롤 후 높이
        after_h = browser.execute_script("return window.scrollY")

        if after_h == before_h:
            break
        before_h = after_h

    page_bar = browser.find_elements_by_css_selector("#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.pagination_pagination__6AcG4 > div > *")
    print(n)


    # 상품 정보 div
    items = browser.find_elements_by_css_selector(".basicList_inner__eY_mq")

    for item in items:
        if item.find_element_by_css_selector(".basicList_mall_title__3MWFY > a").text == "쇼핑몰별 최저가": # 가격 비교 있는 상품만 취급
            name = item.find_element_by_css_selector(".basicList_title__3P9Q7").text
            try:
                price = item.find_element_by_css_selector(".price_num__2WUXn").text
            except:
                price = "판매중단"
            link = item.find_element_by_css_selector(".basicList_title__3P9Q7 > a").get_attribute('href')
            categories = item.find_elements_by_css_selector(".basicList_category__wVevj")
            category = []
            for some in categories:
                category.append(some.text)
            print(name, price, link, category)
            # 데이터 쓰기
            csvWriter.writerow([name, price, link, category])
        else:
            print("스킵")
    
    if n < 6:
        page_bar[n].click()
    else:
        page_bar[5].click()

# 파일 닫기
f.close()
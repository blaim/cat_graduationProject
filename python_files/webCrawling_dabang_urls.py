from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import webCrawling_dabang_particial as WB

import json
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.Room
db.OneRoom.drop()
room = db.OneRoom

'''중개사무소 페이지를 입력하면 해당 중개사무소의 방들의 url을 읽어오는 크롤링'''
'''다방'''

'''보여주는 최대 방의 수는 가로 4개, 세로 6개'''


'''셀레니움 사용시 크롬 버젼에 맞는 크롬 드라이버 설치 필요'''

my_options = webdriver.ChromeOptions()
'''크롬 창 안뜨도록 설정'''
my_options.add_argument("headless")

#test_url = ['https://www.dabangapp.com/agent/61c2c99c43a25a09c06e5ee7','http://www.dabangapp.com/agent/584e63f471813e44e1467e02','http://www.dabangapp.com/agent/602a18a1b394646bd96669c0','http://www.dabangapp.com/agent/5a20e2dff4fc6a557b70dafb','http://www.dabangapp.com/agent/61b2d27b6b2a4b50a0eeeb93','http://www.dabangapp.com/agent/61ca6100f6773a39c4e7bb52','http://www.dabangapp.com/agent/5ad698e171ad9f3c6e382211','http://www.dabangapp.com/agent/61920339cc439926f5d31ef4']
test_url = ['http://www.dabangapp.com/agent/61c2c99c43a25a09c06e5ee7']
for l in test_url:
    print(l)

    '''이 파일과 동일 위치에 있다면 path에 파일명만 입력해도 됨'''

    driver = webdriver.Chrome(executable_path='chromedriver' , options = my_options)
    driver.get(url = l)

    try:
        '''내부 요소 따로 로딩되기 때문에 로딩 될때까지 wait'''
        '''content box 내부도 로딩 시간에 차이가 있음에 주의하자'''
        WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a')))

        name_of_agency = driver.find_element(By.CSS_SELECTOR,'#content > div > div > ul > li:nth-child(1) > div').get_attribute('innerText')
        agency_number = driver.find_element(By.CSS_SELECTOR,'#content > div > div > ul > li:nth-child(4) > div').get_attribute('innerText')
        number_of_rooms = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > div.styled__TabWrap-sc-1j5nm8l-1.bKTJew > p.styled__Tab-sc-1j5nm8l-2.gYpPYH > span').get_attribute('innerText')

        '''숫자로 변환'''
        number_of_rooms = int(number_of_rooms[1:-1])
        print(number_of_rooms)
        '''방 개수 크롤링 '''
        room_lists = 0
        '''
        url가져오는 로직 -> 방개수/24번 화살표 클릭.
        마지막 화살표를 클릭 한 다음은 방개수의 나머지만큼 읽고, 그 이전에는 24개씩 읽는다.
        '''

        room_urls = [] # 방의 url 목록을 저장한다.
        room_lists = 0 # 방에 대한 링크의 개수를 저장한다.

        while True:
            room_list = driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li')
            room_list = len(room_list)
            room_lists += room_list
            for single_div in range(1, room_list + 1): # 현재 페이지에 대해, 방 링크의 수 만큼 루프를 돌면서 url을 목록에 추가한다.
                room_urls.append(driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child('+ str(single_div) +') > div > a').get_attribute('href'))
            # 다음 페이지가 존재하지 않는다면 루프를 빠져나간다.
            nextButton = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > div.styled__PaginWrap-sc-1u1e15y-0.eOczmr > ul > li:nth-last-child(1) > button')
            if nextButton.get_attribute('disabled'):
                break
            # 다음 페이지가 있다면 버튼을 눌러서 이동한다. 버튼 로딩 시간은 생각보다 긴 편이다.
            else:
                nextButton.click()
                WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a')))

        '''제대로 크롤링해서 DB에 저장할때마다 터미널에 url 출력'''
        for i in room_urls:
            WB.get_room_information(i)
            print(i)

        # 크롤링이 끝난 후에는 창을 닫는다.
        driver.quit()

    except TimeoutException:
        print("Web Connection Failed(다방, TIMEOUT during url crawling)")

# 모든 방에 대해서 정보를 얻었다면, json에 값을 넣는다.

j = 0
# json에 넣을 값들만을 찾는다.
fd = room.find({}, {'_id': 0, 'URL': 1, '월세': 1, '주소': 1})
dict = {}
dict = list(dict.items())
print(dict)
# json 파일 경로는 추후 수정
with open('../static/json/data.json', 'w' ,encoding='utf-8-sig')as f:
    for i in fd:
        dict.insert(j, i)
        print(dict[j])
        j += 1
    json.dump(dict, f, ensure_ascii=False,indent=3)
f.close()

'''방 url selector'''
#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a
#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(2) > div > a

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import webCrawling_dabang_particial as WB


'''중개사무소 페이지를 입력하면 해당 중개사무소의 방들의 url을 읽어오는 크롤링'''
'''다방'''

'''보여주는 최대 방의 수는 가로 4개, 세로 6개'''


'''셀레니움 사용시 크롬 버젼에 맞는 크롬 드라이버 설치 필요'''

my_options = webdriver.ChromeOptions()
'''크롬 창 안뜨도록 설정'''
my_options.add_argument("headless")

test_url = 'https://www.dabangapp.com/agent/602a18a1b394646bd96669c0'

'''이 파일과 동일 위치에 있다면 path에 파일명만 입력해도 됨'''
driver = webdriver.Chrome(executable_path='chromedriver' , options = my_options)
driver.get(url = test_url)

try:
    '''내부 요소 따로 로딩되기 때문에 로딩 될때까지 wait'''
    '''content box 내부도 로딩 시간에 차이가 있음에 주의하자'''
    #driver.find_element(By.CSS_SELECTOR,'').get_attribute('innerText')
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a')))

    name_of_agency = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-11kevv2-0.iEoaqL > p').get_attribute('innerText')
    agency_number = driver.find_element(By.CSS_SELECTOR,'#content > div > div > ul > li:nth-child(3) > div').get_attribute('innerText')
    number_of_rooms = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > div.styled__TabWrap-sc-1j5nm8l-1.bKTJew > p.styled__Tab-sc-1j5nm8l-2.gYpPYH > span').get_attribute('innerText')

    '''숫자로 변환'''
    number_of_rooms = int(number_of_rooms[1:-1])

    '''
    url가져오는 로직 -> 방개수/24번 화살표 클릭.
    마지막 화살표를 클릭 한 다음은 방개수의 나머지만큼 읽고, 그 이전에는 24개씩 읽는다.
    '''
    room_urls = []
    for page in range(0, number_of_rooms//24):
        for single_div in range(1, 25):
            room_urls.append(driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child('+ str(single_div) +') > div > a').get_attribute('href'))

        '''다음 방 목록 리스트로 이동'''
        driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > div.styled__PaginWrap-sc-1u1e15y-0.eOczmr > ul > li:nth-child(7) > button').click()
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a')))

    '''남은 방 목록 크롤링'''
    for one_room in range(1, (number_of_rooms - 24 * (number_of_rooms//24))+1):
        room_urls.append(driver.find_element(By.CSS_SELECTOR,'#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(' + str(one_room) + ') > div > a').get_attribute('href'))

    print(room_urls)
    print(len(room_urls))
    print(name_of_agency)
    print(number_of_rooms)


except TimeoutException:
    print("Web Connection Failed(다방, TIMEOUT during url crawling)")


'''방 url selector'''
#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(1) > div > a
#content > div > div > div.styled__Wrap-sc-1j5nm8l-0.dWqXbC > ul > li:nth-child(2) > div > a
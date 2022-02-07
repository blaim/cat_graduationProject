from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.Room

my_options = webdriver.ChromeOptions()
my_options.add_argument("headless")


def get_room_information(url):
    test_url = url
    driver = webdriver.Chrome(executable_path='chromedriver', options=my_options)
    driver.get(url=test_url)

    try:
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located
                                        ((By.CSS_SELECTOR,'#content > div > div > div:nth-child(1) > ul > li:nth-child(1) > div > h1')))

        def check_if_element_exists(selector):
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                return False
            return True

        '''기본 정보 크롤링'''
        agent = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(1) > ul > li:nth-child(4) > div > p').get_attribute('innerText')
        monthly_pay = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(1) > ul > li:nth-child(1) > div > h1').get_attribute('innerText')
        floor = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(1) > div').get_attribute('innerText')
        area = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(2) > div').get_attribute('innerText')
        rooms = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(3) > div').get_attribute('innerText')
        facing_where = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(4) > div').get_attribute('innerText')
        heater = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(5) > div').get_attribute('innerText')
        built_in = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(6) > div').get_attribute('innerText')
        parking_lot_per_building = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(7) > div').get_attribute('innerText')
        parking_lot_per_room = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(8) > div').get_attribute('innerText')
        elevator_exists = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(9) > div').get_attribute('innerText')
        balcony = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(10) > div').get_attribute('innerText')
        possible_moving_into_date = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(11) > div').get_attribute('innerText')
        main_purpose = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(12) > div').get_attribute('innerText')
        usage_approval_date = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(13) > div').get_attribute('innerText')
        first_registration_date = driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(2) > div > ul > li:nth-child(14) > div').get_attribute('innerText')

        '''바로는 세부 위치 안나옴, 버튼 없다면 세부주소 없는것'''
        if (check_if_element_exists('#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button')):
            driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button').click()
            room_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ ').get_attribute('innerText')
            driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button').click()
            street_name_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ').get_attribute('innerText')
        else:
            room_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ ').get_attribute('innerText')
            street_name_location = "???"


        '''세부 정보 크롤링'''
        detailed_description = \
            driver.find_element(By.CSS_SELECTOR,'#content > div > div > div:nth-child(4) > div > div.styled__MemoDivide-sc-1bzcxhb-3.dENHR > div > div').get_attribute('innerText')

        '''옵션 크롤링'''
        number_of_option_list = driver.find_elements(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(1) > div > div')
        number_of_options = len(number_of_option_list)
        options = []
        for i in range(1, number_of_options + 1):
            options.append(driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(1) > div > div:nth-child(' + str(i) + ') > p').get_attribute('innerText'))
        '''보안/ 안전시설 크롤링'''
        number_of_security_system_list = driver.find_elements(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(2) > div > div')
        number_of_security_system = len(number_of_security_system_list)
        security_system = []
        for i in range(1, number_of_security_system + 1):
            security_system.append(driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(2) > div > div:nth-child(' + str(i) + ') > p').get_attribute('innerText'))

        '''월세 정보 텍스트 수정'''
        monthly_pay = monthly_pay[3:]

        '''평수 텍스트 수정'''
        area = area[:-2]

        '''방향 텍스트 수정'''
        facing_where = facing_where[:-10]

        #주소 뒤에 붙는 도로명,지번 같은거 지워줌 - 지도 검색 할때 방해되서 만듬
        room_location = room_location.replace('\n도로명','')
        room_location = room_location.replace('\n위치정보','')
        room_location = room_location.replace('\n지번','')
        street_name_location = street_name_location.replace('\n도로명','')
        street_name_location = street_name_location.replace('\n위치정보','')
        street_name_location = street_name_location.replace('\n지번','')


        informations = []
        informations.append(agent)
        informations.append(monthly_pay)
        informations.append(floor)
        informations.append(area)
        informations.append(rooms)
        informations.append(facing_where)
        informations.append(heater)
        informations.append(built_in)
        informations.append(parking_lot_per_building)
        informations.append(parking_lot_per_room)
        informations.append(elevator_exists)
        informations.append(balcony)
        informations.append(possible_moving_into_date)
        informations.append(main_purpose)
        informations.append(usage_approval_date)
        informations.append(first_registration_date)
        informations.append(detailed_description)
        informations.append(room_location)
        informations.append(street_name_location)
        informations.append(number_of_options)
        informations.extend(options)
        informations.append(number_of_security_system)
        informations.extend(security_system)

        # DB에는 리스트로 숫자처럼 생긴 문자열 형태로 저장됨
        doc = {
            '공인중개사': agent,
            '월세': monthly_pay,
            '층': floor,
            '방 면적': area,
            '방/욕실 수': rooms,
            '방향': facing_where,
            '난방종류': heater,
            '빌트인': built_in,
            '건물 주차수': parking_lot_per_building,
            '세대 당 주차수':parking_lot_per_room,
            '엘레베이터': elevator_exists,
            '베란다/발코니': balcony,
            '입주가능일': possible_moving_into_date,
            '주용도': main_purpose,
            '사용승인일': usage_approval_date,
            '최초등록일': first_registration_date,
            '상세설명': detailed_description,
            '주소': room_location,
            '도로명주소': street_name_location,
            '옵션 수': (number_of_options,options),
            '보안시설 수': (number_of_security_system,security_system)
        }

        # 입력
        room = db.OneRoom
        room.insert_one(doc)
        '''
            출력되는 리스트 순서
            공인중개사,월세, 층, 방 면적, 방 수/욕실 수, 방향, 난방종류, 빌트인,
            건물 주차수, 세대당 주차수, 엘리베이터, 베란다/발코니, 입주가능일, 주용도
            사용승인일, 최초등록일, 상세설명, 주소, 도로명주소 순서대로 저장 후

            옵션과 보안시설은 방마다 개수가 다르기 때문에
            옵션 수, 옵션들
            보안시설 수, 보안시설들
            순으로 저장한다.

            중개 의로인의 위치 표기 동의를 받지 않은 매물은 정확한 위치가 없으므로, 주소 부분에 대략적인 주소만 적고 
            도로명 주소 란에는 ???를 저장한다.
        '''
        return informations

        #db.ra.insert_one(doc)
    except TimeoutException:
        print("Web Connection Failed(다방, TIMEOUT during single room crawling)")


#a = get_room_information('https://www.dabangapp.com/room/61f257ace9ec8b627a2341d8')
#print(a)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

'''방 하나의 정보들을 불러오는 크롤링 '''
'''다방'''


'''셀레니움 사용시 크롬 버젼에 맞는 크롬 드라이버 설치 필요'''

my_options = webdriver.ChromeOptions()
'''크롬 창 안뜨도록 설정'''
my_options.add_argument("headless")




def get_room_information(url):
    test_url = url

    '''이 파일과 동일 위치에 있다면 path에 파일명만 입력해도 됨'''
    driver = webdriver.Chrome(executable_path='chromedriver' , options = my_options)
    driver.get(url = test_url)

    try:
        '''내부 요소 따로 로딩되기 때문에 로딩 될때까지 wait'''
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located
                                             ((By.CSS_SELECTOR, '#content > div > div > div:nth-child(1) > ul > li:nth-child(1) > div > h1')))

        def check_if_element_exists(selector):
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                return False
            return True

        '''기본 정보 크롤링'''
        monthly_pay = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(1) > ul > li:nth-child(1) > div > h1').get_attribute('innerText')
        floor = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(1) > div').get_attribute('innerText')
        area = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(2) > div').get_attribute('innerText')
        rooms = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(3) > div').get_attribute('innerText')
        facing_where = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(4) > div').get_attribute('innerText')
        heater = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(5) > div').get_attribute('innerText')
        built_in = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(6) > div').get_attribute('innerText')
        parking_lot_per_building = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(7) > div').get_attribute('innerText')
        pariking_lot_per_room = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(8) > div').get_attribute('innerText')
        elevator_exists = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(9) > div').get_attribute('innerText')
        balcony = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(10) > div').get_attribute('innerText')
        possible_moving_into_date = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(11) > div').get_attribute('innerText')
        main_purpose = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(12) > div').get_attribute('innerText')
        usage_approval_date = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(13) > div').get_attribute('innerText')
        first_registration_date = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(2) > div > ul > li:nth-child(14) > div').get_attribute('innerText')

        '''바로는 세부 위치 안나옴, 버튼 없다면 세부주소 없는것'''
        if(check_if_element_exists('#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button')):
            driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button').click()
            room_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ').get_attribute('innerText')
            driver.find_element(By.CSS_SELECTOR, '#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ > button').click()
            street_name_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ').get_attribute('innerText')
        else:
            room_location = driver.find_element(By.CSS_SELECTOR,'#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div:nth-child(3) > div > div.styled__Address-sc-8pfhii-2.kmHfVJ').get_attribute('innerText')
            street_name_location = "???"


        '''세부 정보 크롤링'''
        detailed_description = \
            driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(4) > div > div.styled__MemoDivide-sc-1bzcxhb-3.dENHR > div > div').get_attribute('innerText')

        '''옵션 크롤링'''
        number_of_option_list = driver.find_elements(By.CSS_SELECTOR, '#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(1) > div > div')
        number_of_options = len(number_of_option_list)
        options = []
        for i in range(1, number_of_options+1):
            options.append(driver.find_element(By.CSS_SELECTOR, '#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(1) > div > div:nth-child('+str(i)+') > p').get_attribute('innerText'))

        '''보안/ 안전시설 크롤링'''
        number_of_security_system_list = driver.find_elements(By.CSS_SELECTOR, '#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(2) > div > div')
        number_of_security_system = len(number_of_security_system_list)
        security_system = []
        for i in range(1, number_of_security_system+1):
            security_system.append(driver.find_element(By.CSS_SELECTOR, '#roomDetail > div.styled__MutableWrap-sc-11huzff-2.lhOOEc > div.styled__Block-rtvnk4-2.styled__OptionBlock-sc-1m95zms-0.ftreVo.dINcLV > div:nth-child(2) > div > div:nth-child('+str(i)+') > p').get_attribute('innerText'))

        '''월세 정보 텍스트 수정'''
        monthly_pay = monthly_pay[3:]

        '''평수 텍스트 수정'''
        area = area[:-2]

        '''방향 텍스트 수정'''
        facing_where = facing_where[:-10]

        for i in range(0, number_of_options):
            print(options[i])

        for i in range(0, number_of_security_system):
            print(security_system[i])

        informations = []
        informations.append(monthly_pay)
        informations.append(floor)
        informations.append(area)
        informations.append(rooms)
        informations.append(facing_where)
        informations.append(heater)
        informations.append(built_in)
        informations.append(parking_lot_per_building)
        informations.append(pariking_lot_per_room)
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


        '''
            출력되는 리스트 순서
            월세, 층, 방 면적, 방 수/욕실 수, 방향, 난방종류, 빌트인,
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


    except TimeoutException:
        print("Web Connection Failed(다방, TIMEOUT during single room crawling)")


a = get_room_information('https://www.dabangapp.com/room/61c53b9c0212123261327df5')
print(a)
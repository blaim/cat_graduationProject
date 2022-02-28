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
        WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(6) > div > div > p.title')))

        def check_if_element_exists(selector):
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                return False
            return True

        '''기본 정보 크롤링'''
        # 사진 url들을 구한다.
        script = "return window.getComputedStyle(document.querySelector('#content > div.styled__Wrap-t81k0-0.hAoXkk > div > div > div.styled__BigWrap-t81k0-3.fxstzP > div'),'::after').getPropertyValue('background-image')"
        scripts = "list = document.querySelectorAll('#content > div.styled__Wrap-t81k0-0.hAoXkk > div > div > div.styled__SmallWrap-t81k0-5.bBMySi > div');images = [];list.forEach(function(item){images.push(window.getComputedStyle(item, '::after').getPropertyValue('background-image'))});return images"

        image_url = []

        image_url.append(driver.execute_script(script))
        small = driver.execute_script(scripts)
        for i in range(len(small)):
            image_url.append(small[i])
        image_num = len(image_url)
        for i in range(image_num):

            image_url[i] = image_url[i][5:-2]

        # 공인중개사 정보를 구한다.
        agent = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__StickySideContainer-sc-1a06c6n-0.TVcfR > div > div > div.styled__LessorWrap-cvrpi1-13.jVGbJb > div > p').get_attribute('innerText')


        # 들어있는 가격 정보의 수를 구한다.
        price_list = driver.find_elements(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li')
        price_num = len(price_list)
        # 가격 정보를 임시로 넣을 딕셔너리를 만든다.
        price_list = {}
        # 딕셔너리에 정보들을 집어넣는다.
        for i in range(price_num):
            b = ""

            a = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li:nth-child(' + str((i + 1)) + ') > div.styled__Name-rtvnk4-8.eFgXRF').get_attribute('innerText')
            a = a.replace('\n\n', ' ')
            if a == '관리비':
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li:nth-child(' + str(
                                            (i + 1)) + ') > div.styled__Content-rtvnk4-9.haTbsj > p:nth-child(1)').get_attribute(
                    'innerText')
            elif a == '한달 예상 주거비용':
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li:nth-child(' + str((i + 1)) + ') > div.styled__Content-rtvnk4-9.haTbsj > p.costContent').get_attribute(
                    'innerText')
            elif a == '주차':
                continue
            elif a == '단기임대':
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li:nth-child(' + str((i + 1)) + ') > div.styled__Content-rtvnk4-9.haTbsj').get_attribute('innerText')
            else:
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(1) > div > div > li:nth-child(' + str((i + 1)) + ') > div.styled__Content-rtvnk4-9.haTbsj > p').get_attribute('innerText')
            price_list[a] = b

        # 월세
        monthly_pay = price_list.get('월세')
        # 관리비
        care_cost = price_list.get('관리비')
        # 단기임대
        Short_rental = price_list.get('단기임대')
        # 한달 예상 주거비용

        cost_per_month = price_list.get('한달 예상 주거비용')

        '''상세 정보 크롤링'''
        # 들어있는 상세 정보의 수를 구한다.
        detailed_list = driver.find_elements(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(2) > div > div.styled__Ul-rtvnk4-7.iAUaiU > li')
        detailed_num = len(detailed_list)
        # 상세 정보를 임시로 넣을 딕셔너리를 만든다.
        detailed_list = {}
        # 딕셔너리에 정보들을 집어넣는다.
        for i in range(detailed_num - 1):
            b = ""
            a = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(2) > div > div.styled__Ul-rtvnk4-7.iAUaiU > li:nth-child(' + str((i + 2)) + ') > div.styled__Name-rtvnk4-8.eFgXRF').get_attribute('innerText')
            if a == '전용/공급면적':
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(2) > div > div.styled__Ul-rtvnk4-7.iAUaiU > li:nth-child(' + str((i + 2)) + ') > div.styled__Content-rtvnk4-9.haTbsj > label').get_attribute('innerText')
            else:
                b = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(2) > div > div.styled__Ul-rtvnk4-7.iAUaiU > li:nth-child(' + str((i + 2)) + ') > div.styled__Content-rtvnk4-9.haTbsj').get_attribute('innerText')

            detailed_list[a] = b
        # 각 정보에 대해, 존재하면 값을 얻는다.
        floor = detailed_list.get('해당층/건물층')
        area = detailed_list.get('전용/공급면적')
        rooms = detailed_list.get('방 수 / 욕실 수')
        facing_where = detailed_list.get('방향')[:-8]
        heater = detailed_list.get('난방종류')
        built_in = detailed_list.get('빌트인')
        parking_lot_per_building = detailed_list.get('건물 주차')
        elevator_exists = detailed_list.get('엘리베이터')
        balcony = detailed_list.get('베란다/발코니')
        possible_moving_into_date = detailed_list.get('입주가능일')
        main_purpose = detailed_list.get('주용도')
        usage_approval_date = detailed_list.get('사용승인일')
        first_registration_date = detailed_list.get('최초등록일')

        '''바로는 세부 위치 안나옴, 버튼 없다면 세부주소 없는것'''
        if (check_if_element_exists('#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC > button')):
            driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC > button').click()
            room_location = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC').get_attribute('innerText')
            driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC').click()
            street_name_location = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC').get_attribute('innerText')
        else:
            room_location = driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(5) > div > div.styled__NewAddress-sc-8pfhii-4.bXgTrC').get_attribute('innerText')
            street_name_location = "???"


        '''상세설명 크롤링'''
        detailed_description = \
            driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(6) > div > div').get_attribute(
                'innerText')

        '''옵션 크롤링'''
        number_of_option_list = driver.find_elements(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(3) > div > div > div')
        number_of_options = len(number_of_option_list)
        options = []
        for i in range(1, number_of_options + 1):
            options.append(driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(3) > div > div > div:nth-child(' + str(i) + ') > p').get_attribute('innerText'))
        '''보안/ 안전시설 크롤링'''
        number_of_security_system_list = driver.find_elements(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(4) > div > div > div')
        number_of_security_system = len(number_of_security_system_list)
        security_system = []
        for i in range(1, number_of_security_system + 1):
            security_system.append(driver.find_element(By.CSS_SELECTOR,'#content > div.styled__StickyTopContainer-sc-1tkfz70-0.gnAkun > div > div > div.styled__Content-sc-11huzff-5.dmotyw > div:nth-child(4) > div > div > div:nth-child(' + str(i) + ') > p').get_attribute('innerText'))

        # 정보 획득이 끝난 후에는 창을 닫는다.
        driver.quit()

        '''월세 정보 텍스트 수정'''
        #monthly_pay = monthly_pay[3:]

        '''평수 텍스트 수정'''
        area = area[:-2]

        '''방향 텍스트 수정'''
        # facing_where = facing_where[:-8]

        # 주소 뒤에 붙는 도로명,지번 같은거 지워줌 - 지도 검색 할때 방해되서 만듬
        room_location = room_location.replace('\n도로명', '').replace('\n위치정보', '').replace('\n지번', '')
        street_name_location = street_name_location.replace('\n도로명', '').replace('\n위치정보', '').replace('\n지번', '')
        facing_where = facing_where.replace('주실 방향 기준', '')

        informations = []
        informations.append(url)
        informations.append(image_url)
        informations.append(agent)
        informations.append(monthly_pay)
        informations.append(care_cost)
        informations.append(Short_rental)
        informations.append(cost_per_month)
        informations.append(floor)
        informations.append(area)
        informations.append(rooms)
        informations.append(facing_where)
        informations.append(heater)
        informations.append(built_in)
        informations.append(parking_lot_per_building)
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
            'URL': url,
            '사진 url': image_url,
            '공인중개사': agent,
            '월세': monthly_pay,
            '관리비': care_cost,
            '단기임대': Short_rental,
            '한달 예상 주거비용': cost_per_month,
            '층': floor,
            '방 면적': area,
            '방/욕실 수': rooms,
            '방향': facing_where,
            '난방종류': heater,
            '빌트인': built_in,
            '건물 주차수': parking_lot_per_building,
            '엘레베이터': elevator_exists,
            '베란다/발코니': balcony,
            '입주가능일': possible_moving_into_date,
            '주용도': main_purpose,
            '사용승인일': usage_approval_date,
            '최초등록일': first_registration_date,
            '상세설명': detailed_description,
            '주소': room_location,
            '도로명주소': street_name_location,
            '옵션 수': (number_of_options, options),
            '보안시설 수': (number_of_security_system, security_system)
        }
        # 입력
        room = db.OneRoom
        room.insert_one(doc)
        '''
            출력되는 리스트 순서
            URL,공인중개사,월세,관리비,단기임대,한달 예상 주거비용, 층, 방 면적, 방 수/욕실 수, 방향, 난방종류, 빌트인,
            건물 주차수, 엘리베이터, 베란다/발코니, 입주가능일, 주용도
            사용승인일, 최초등록일, 상세설명, 주소, 도로명주소 순서대로 저장 후
            옵션과 보안시설은 방마다 개수가 다르기 때문에
            옵션 수, 옵션들
            보안시설 수, 보안시설들
            순으로 저장한다.
            중개 의로인의 위치 표기 동의를 받지 않은 매물은 정확한 위치가 없으므로, 주소 부분에 대략적인 주소만 적고 
            도로명 주소 란에는 ???를 저장한다.
        '''
        # def index(request):
        #    info = {'addrees': room_location, 'monthly_pay': monthly_pay}
        #    return render(request, 'main/main.html', info)

        return informations

    except TimeoutException:
        print("Web Connection Failed(다방, TIMEOUT during single room crawling)")

#a = get_room_information('http://www.dabangapp.com/room/61fc8496872b9405c3b2b3d4')
#print(a)
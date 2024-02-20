from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep
import json
import requests    # requests라는 외부 라이브러리는 서버에 데이터를 전송할떄 사용한다.

#terminal에 명령어 실행해서 디버깅용 크롬창 생성 후 실행필요
#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

# 상품 url list
prd_url_list = []
# Page count
obj_cnt = 0;

# TODO random user_agents
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent_index = random.choice(list(range(0, len(user_agents), 1)))

# driver = webdriver.Chrome() 

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--window-size=1920x1080')
# options.add_argument('--disable-gpu')
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-setuid-sandbox")
# options.add_argument(user_agents[user_agent_index])
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
 
driver = webdriver.Chrome()
# driver = webdriver.Chrome(options=options)
# # service = Service(executable_path=r'../chromedriver_mac_arm64/chromedriver')
# service = Service()
# driver = webdriver.Chrome(service=service, options=options)
# #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

court_dic = {
    "만석공원" : "https://share.gg.go.kr/sports/view?instiCode=1010009&facilityId=F0001&searchArea=4111&searchArea2=%EC%88%98%EC%9B%90%EC%8B%9C&searchType=S1_1&searchType2=%ED%85%8C%EB%8B%88%EC%8A%A4%EC%9E%A5&searchDate=&searchFacilityNm=&curPage=1&reservAvailable=&pCode=&pCodeNm=",
    "연암배수지" : "https://share.gg.go.kr/sports/view?instiCode=1010010&facilityId=F0005&searchArea=4111&searchArea2=%EC%88%98%EC%9B%90%EC%8B%9C&searchType=S1_1&searchType2=%ED%85%8C%EB%8B%88%EC%8A%A4%EC%9E%A5&searchDate=&searchFacilityNm=&curPage=1&reservAvailable=&pCode=&pCodeNm="
}

while True:
    driver.get("https://share.gg.go.kr/index")
    driver.implicitly_wait(5)

    avail_courts = [];

    for c in range(0, len(court_dic.keys())):

        driver.get(list(court_dic.values())[c])
        driver.implicitly_wait(5)

        sunday_cnt = len(driver.find_elements(By.CSS_SELECTOR, ".viewOption .ui-datepicker-calendar tr td:first-child:not(.ui-datepicker-unselectable)"))
        # obj_cnt = len(driver.find_elements(By.CSS_SELECTOR, ".viewOption .ui-datepicker-calendar tr td:nth-child(2):not(.ui-datepicker-unselectable)"))

        for i in range(1, sunday_cnt + 1):
            avail_courts.append(list(court_dic.keys())[c])

        saturday_cnt = len(driver.find_elements(By.CSS_SELECTOR, ".viewOption .ui-datepicker-calendar tr td:nth-child(7):not(.ui-datepicker-unselectable)"))

        for i in range(1, saturday_cnt + 1):
            avail_courts.append(list(court_dic.keys())[c])

        otherdays_cnt = len(driver.find_elements(By.CSS_SELECTOR, ".viewOption .ui-datepicker-calendar tr td:not(:first-child):not(:nth-child(7)):not(.ui-datepicker-unselectable)"))

        for i in range(1, otherdays_cnt + 1):
            driver.find_elements(By.CSS_SELECTOR, ".viewOption .ui-datepicker-calendar tr td:not(:first-child):not(:nth-child(7)):not(.ui-datepicker-unselectable)")[i-1].click()
            driver.find_elements(By.CSS_SELECTOR, "#oneClick2")[0].click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
            except :
                print("no alert")

    if len(avail_courts) > 0:
        api_url = "https://notify-api.line.me/api/notify"
        token = "BWbxx2NgmUxhLAgIzT48dfSV110nA2DOeIgFHvPsTRD" # 앞서 발급 받은 토큰을 여기 넣음

        headers = {'Authorization':'Bearer '+token}

        message = {
            "message" : ', '.join(avail_courts)
        }

        requests.post(api_url, headers= headers , data = message, verify=False)
        
    sleep(10)



#coding=utf-8
import json
import random
import traceback
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class WebLogin_Chrome:
    def __init__(self, username, password):
        self.cookies = None
        self.session = requests.session()
        self.userInfo = None
        self.visit = None
        self.visitor = None

        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        self.origin = 'https://www.nike.com'
        self.session.headers.update({'user-agent':self.useragent, 'origin': self.origin})



        self.username = username
        self.password = password

    def login(self):
        try:
            chromeOptions = webdriver.ChromeOptions()
            # 无界面
            # chromeOptions.add_argument('--headless')
            # 禁用gpu加速
            chromeOptions.add_argument('--disable-gpu')
            # 关闭图片
            prefs = {"profile.managed_default_content_settings.images": 2}
            # chromeOptions.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(chrome_options=chromeOptions)

            w_h = driver.get_window_size()
            width = w_h["width"]
            height = w_h["height"]

            clickWidth1 = (width - 500) / 2
            clickWidth2 = width / 2 + 250

            driver.get("https://www.nike.com/cn/zh_cn/")
            WebDriverWait(driver, 15).until(lambda x: x.find_element_by_class_name('login-text'))
            driver.find_element_by_class_name('login-text').click()

            # 随机位置点击绕过验证
            for i in range(random.randint(2, 5)):
                ActionChains(driver).move_by_offset(clickWidth1,
                                                    random.randint(0, height)).click().perform()
                ActionChains(driver).move_by_offset(clickWidth2,
                                                    random.randint(0, height)).click().perform()

            driver.find_element_by_name('verifyMobileNumber').send_keys(self.username)
            driver.find_element_by_name('password').send_keys(self.password)
            driver.find_element_by_class_name('nike-unite-submit-button').click()

            # 随机位置点击绕过验证
            for i in range(random.randint(2, 5)):
                ActionChains(driver).move_by_offset(clickWidth1,
                                                    random.randint(0, height)).click().perform()
                ActionChains(driver).move_by_offset(clickWidth2,
                                                    random.randint(0, height)).click().perform()
            try:
                WebDriverWait(driver, 5).until_not(
                    lambda x: x.find_element_by_class_name('exp-join-login').is_displayed())
            except:
                # print("等待超时...")
                pass
            if not driver.find_element_by_xpath('//*[@id="nike-unite-mobileLoginForm"]/div[1]').is_displayed():
                WebDriverWait(driver, 10).until_not(
                    lambda x: x.find_element_by_class_name('exp-join-login').is_displayed())

                self.cookies = driver.get_cookies()

                driver.get("https://unite.nike.com/session.html")
                userInfo = driver.execute_script(
                    "return localStorage.getItem('com.nike.commerce.nikedotcom.web.credential');")
                self.userInfo = json.loads(userInfo)
                self.userService = self.userInfo['user']
        except:
            traceback.print_exc()
        finally:
            driver.close()
            driver.quit()

    def getCookies(self):
        cookies = ""
        if self.cookies != None:
            for cookie in self.cookies:
                cookies += (cookie['name'] + "=" + cookie['value'] + ";")
        return cookies
    
    def getCookiesDict(self):
        dict_cookies = {}
        if self.cookies != None:
            for cookie in self.cookies:
                dict_cookies[cookie['name']] = cookie['value']
        return dict_cookies

    def getUserService(self):
        params = {
            'appVersion': 543,
            'experienceVersion': 441,
            'uxid': 'com.nike.commerce.nikedotcom.web',
            'locale': 'zh_CN',
            'backendEnvironment': 'identity',
            'browser': 'Google Inc.',
            'os': 'undefined',
            'mobile': 'false',
            'native': 'false',
            'visit': self.visit,
            'visitor': self.visitor,
            'viewId': 'unite',
            'atgSync': 'true',
        }

        cookie = self.getCookies()

        self.referer = 'https://www.nike.com/cn/zh_cn/'
        self.authorization = 'Bearer ' + self.userInfo['access_token']

        self.session.headers.update({'referer':self.referer,  'authorization':self.authorization })

        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.getCookiesDict())

        r = self.session.get('https://unite.nike.com/getUserService', params=params)

        self.userService = r.json();
        print(self.userService)


    def addAddress(self):
        params = {
            'additionalPhoneNumber': "",
            'address1': "九华路中央景城26dong",
            'address2': "",
            'address3': "",
            'city': "苏州市",
            'country': "CN",
            'countyDistrict': "园区",
            'district': "15483",
            'firstName': "娇娇",
            'id': 'null',
            'lastName': "蔡",
            'otherName': 'null',
            'phoneNumber': "18501588607",
            'postalCode': "230000",
            'preferred': 'true',
            'state': "CN-32",
            'type': "SHIPPING",
        }
        cookie = self.getCookies()

        self.session = requests.Session()
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        self.origin = 'https://www.nike.com'
        self.referer = 'https://www.nike.com/cn/zh_cn/p/settings/'
        self.authorization = 'CPC'

        self.session.headers.update({'user-agent':self.useragent, 'origin': self.origin, 'referer':self.referer,  'authorization':self.authorization })

        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.getCookiesDict())

        r = self.session.get('https://unite.nike.com/getUserService', params=params)

        print(r.text)

    def getUtcTime(self):
        utcTime = time.gmtime()
        return utcTime

    def gwtProductFeed(self):
        r = requests.get(
            "https://api.nike.com/commerce/productfeed/products/snkrs/threads?country=CN&limit=5&locale=zh_CN&skip=0&withCards=true").json()
        return r
    
    
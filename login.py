
import requests
from bs4 import BeautifulSoup
import random

class snkrs:
    def __init__(self, passport, password):
        self.passport = "+86" + passport
        self.password = password
        self.app_version = 543
        self.experience_version = 441
        self.data_baseurl = 'https://s3.nikecdn.com/'
        self.session = requests.Session()
        self.uuid = self.generateUuid()
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        self.origin = 'https://www.nike.com'
        self.referer = 'https://www.nike.com/cn/zh_cn/'
        self.session.headers.update({'user-agent':self.useragent, 'origin': self.origin, 'referer':self.referer})
        


    def initParameters(self):
        url = 'https://www.nike.com/cn/zh_cn/'
        r = self.session.get(url, verify = False)
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find(id='nike-unite')
        self.clientId = tag['data-clientid']
        self.locale = tag['data-locale']
        self.uxid = tag['data-uxid']
        

    def generateUuid(self):
        uuid = []
        basecode = '0123456789abcdef'
        for idx in range(36):
            uuid.append(basecode[random.randint(0, len(basecode)-1)])
        uuid[14] = '4'
        uuid[19] = basecode[random.randint(8,11)]
        uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-'
        ret = ''
        for idx in range(36):
            ret += uuid[idx]
        return ret

    def appInitialization(self):
        url = 'https://unite.nike.com/appInitialization'
        params = {
            'appVersion' : self.app_version,
            'experienceVersion' : self.experience_version,
            'uxid' : self.uxid,
            'locale' : self.locale,
            'backendEnvironment' : 'identity',
            'browser' : 'Google Inc.',
            'os' : 'undefined',
            'mobile' : 'false',
            'native' : 'false',
            'visit' : '',
            'visitor' : '',
            'clientId' : self.clientId,
            'status' : 'success',
            'uxId' : self.uxid,
            'isAndroid' : 'false',
            'isIOS' : 'false',
            'isMobile' : 'false',
            'isNative' : 'false',
            'timeElapsed' : '629',
        }

        r = self.session.get(url, params=params)
        print(r.status_code)

    def login(self):
        url = 'https://unite.nike.com/login'
        params = {
            'appVersion' : self.app_version,
            'experienceVersion' : self.experience_version,
            'uxid' : self.uxid,
            'locale' : self.locale,
            'backendEnvironment' : 'identity',
            'browser' : 'Google Inc.',
            'os' : 'undefined',
            'mobile' : 'false',
            'native' : 'false',
            'visit' : '1',
            'visitor' : self.uuid,
        }
        r = self.session.request('OPTIONS', url, params=params)
        print(r.status_code)

        body = {
            'client_id': self.clientId,
            'grant_type': "password",
            'password': self.password,
            'username': '+86' + self.passport,
            'ux_id': self.uxid, 
        }
        r = self.session.post(url, params=params, json=body)
        print(r.status_code)



        
        



import requests
from bs4 import BeautifulSoup
import random

class snkrs:
    def __init__(self, passport, password):
        self.passport = "+86" + passport
        self.password = password
        self.session = requests.Session()
        self.uuid = self.generateUuid()


    def initParameters(self):
        url = 'https://www.nike.com/cn/zh_cn/'
        r = self.session.get(url, verify = False)
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.find(id='nike-unite'))

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
        


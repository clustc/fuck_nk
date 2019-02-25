import threading, sqlite3
from webLogin import WebLogin_Chrome

users = [
    '18501588607',
    '13776922446',
    '13228892088',
    '13775292891',
    '13228892298',
    '17706255126',
    '13584718828',
    '13587048871']

userLock = threading.Lock()
dbLock = threading.Lock()

conn = sqlite3.connect("nike.db")
cursor = conn.cursor()
userTb = cursor.execute('select * from nike')

def login():
    global users
    userLock.acquire()
    passport = users.pop()
    userLock.release()

    webLogin = WebLogin_Chrome(passport, 'CaiLi1225')
    webLogin.login()
    webLogin.getUserService()

    userid = webLogin.visitor
    refreshToken = webLogin.userService['refresh_token']
    username = passport
    password = 'CaiLi1225'

    c.execute("INSERT INTO nike (userid,refreshToken,username,password) \
      VALUES ({0},{1},{2},{3})".format(''));

threads = []
for i in range(len(users)):
    thread = threading.Thread(target=login)
    threads.append(thread)

for thread in threads:
    print('feww')
    thread.start()

for thread in threads:
    thread.join()

print('done..')


    




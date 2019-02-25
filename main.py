from login import snkrs
from webLogin import *
import time

utcTime = time.gmtime();


app = WebLogin_Chrome('18501588607', 'CaiLi1225')
app.login()
app.getUserService()
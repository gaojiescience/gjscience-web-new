import urllib.request, http.client, json, time, datetime
import os
import settings
import django
import sys
import time
import tushare as ts
# 300875
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'gjsicence.settings' 
django.setup()

from server.models import UserProfile

user_list = UserProfile.objects.filter(
	email_tips_active=0
)

def calc_beta(stock):
	
	return 0

def create_email_html():

	return 0
	

for user in user_list:
	
	print(user.email_str)
	
import requests
import json
import os
import datetime
import smtplib
# first get an access token, you will need to have a 90 day valid refresh token, 
# that will need to be updated in the TD Developer UI https://developer.tdameritrade.com/authentication/apis/post/token-0

working_dir = os.path.dirname(__file__)
print(working_dir)
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'grant_type': 'refresh_token',
  # USE REFRESH_TOKEN FROM HERE https://developer.tdameritrade.com/authentication/apis/post/token-0 USING THIS https://developer.tdameritrade.com/content/simple-auth-local-apps 
  'refresh_token': 'REFRESHTOKEN',
  'access_type': '',
  'code': '',
  # INSERT YOUR CLIENT APP ID FROM TD DEVELOPER MY APPS
  'client_id': 'APPCODE@AMER.OAUTHAP',
  'redirect_uri': ''
}

response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)

print(response.status_code)

token = response.json()

access_token = token['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
}

params = (
    ('fields', 'positions'),
)
  # INSERT YOUR TD ACCOUNT ID
account_id = ACCOUNTID#

position_response = requests.get(f'https://api.tdameritrade.com/v1/accounts/{account_id}', headers=headers, params=params)

account = position_response.json()

working_date = str(datetime.datetime.now())

securities = account['securitiesAccount']
positions = securities['positions']
positions_string = ''
for x in positions:
    if x['currentDayProfitLossPercentage'] > 50 :
        print(x['currentDayProfitLossPercentage'] , x['instrument']['underlyingSymbol'])

f = open(working_dir + "\\positions.csv", "a")
for i in positions:
    if i['currentDayProfitLossPercentage'] > 50 :
        f.write(working_date + ',' + i['instrument']['description'] + ',' + str(i['currentDayProfitLossPercentage']) + "\n")
        positions_string += working_date + ',' + i['instrument']['description'] + ',' + str(i['currentDayProfitLossPercentage']) + "\n"
f.close()

#Use link below to Set up SMTP relay service
#https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-gmail-smtp-server

# to = 'phonenumber@@txt.att.net'
# gmail_user = 'gmail@gmail.com'
# gmail_pwd = 'gmail_developer_app_code'
# smtpserver = smtplib.SMTP('smtp.gmail.com',587)
# smtpserver.ehlo()
# smtpserver.starttls()
# smtpserver.ehlo() # extra characters to permit edit
# smtpserver.login(gmail_user, gmail_pwd)
# header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
# print(header)
# msg = header + '\n' + positions_string
# smtpserver.sendmail(gmail_user, to, msg)
# print('done!')
# smtpserver.quit()

# print(positions)
# results = json.dumps(positions)
# py_results = json.loads(results)
# print(py_results)

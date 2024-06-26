import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import uuid
import time
import requests
import os



def generate_device_id():
    # 生成 UUID
    device_id = uuid.uuid4()
    # 將 UUID 轉換為無連字符的16進位字串
    hex_string = str(device_id).replace('-', '')
    return hex_string[:32]

#env
class Enviroment:
    def __init__(self):
        # 取得環境變數, if ENVIRONMENT None, 則預設為 uat
        self.env = os.environ.get('ENVIRONMENT', "uat") 
        self.urls = {
            "prod": "https://api.imser5yw.com",
            "uat": "http://uat-homews.imdevs.net",
            "stg": "https://im-stg.imdevs.net",
            "dev": "https://im-dev.imdevs.net",
        }

        self.wallet_urls = {
            "prod": "https://svzyyges3qk6b6s62v88qts.letsgomars.com",
            "uat": "https://im-uat-aaj7xg4ds.imdevs.net",
            "stg": "https://im-stg-pzx.imdevs.net",
            "dev": "https://im-dev-pzx.imdevs.net",
        }

        self.phone_number = {
            "prod": "0928215519",
            "uat": "0975916010",
            "stg": "0975916010",
            "dev": "0909317920"
        }
        
    def get_base_url(self):
        return self.urls.get(self.env)
    
    def get_wallet_url(self):
        return self.wallet_urls.get(self.env)
    
    def get_phone_number(self):
        return self.phone_number.get(self.env)

class ReadCSV:
    def __init__(self):
        # 初始化类的属性
        self.token = None
        self.user_id = None
        self.sid = None
        self.client_secret = None
        self.wallet_password = None

    def read_csv(self):
        # 从 CSV 文件中读取设置并将其存储在类的属性中
        with open("token.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == "token":
                    self.token = row[1]
                elif row[0] == "user_id":
                    self.user_id = row[1]
                elif row[0] == "sid":
                    self.sid = row[1]
                elif row[0] == "client_secret":
                    self.client_secret = row[1]
                elif row[0] == "wallet_password":
                    self.wallet_password = row[1]


def send_email(subject_prefix, body):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #subject_prefix 由 Login , Wallet 帶入prefix 
    subject = f"{subject_prefix} Test failed  {formatted_time}"
    recipients = ["frandyfancy@gmail.com"]
    sender = "frandyfancy@gmail.com"
    password = "mwwdsbtomalgcmbh"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def send_shaberi_message(global_token, message):
    get_environment_url = Enviroment().get_base_url
    current_time = int(time.time())
    # API details
    url = f"{get_environment_url}/_matrix/client/r0/rooms/!183481292480:shaberi.com/send/m.room.message/m{current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "msgtype": "m.text",
        "body": message
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    response_data = response.json()
    print("Response Data :" , response_data)

def send_signal_message(message):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    body = f"{formatted_time}\n{message}"
    # API details
    url = f"https://signal.callmebot.com/signal/send.php?phone=04f47b04-894a-44d8-b6d5-e8fad5264015&apikey=992318&text={body}"
    print("url:" , url)
    # Make the POST requests
    response = requests.post(url)



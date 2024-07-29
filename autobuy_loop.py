import requests, time, random, json, wget, os
from colorama import init, Fore
from audioplayer import AudioPlayer
init(autoreset=True)

price1 = 0
t1me = 0
c1 = 0

def login():
    global c1, acs_tkn, rfr_tkn, uid
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.MAGENTA + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 2
        elif mail.count('@') == 1:
            pw = input(Fore.MAGENTA + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={replaces(pw)}").json()
                if 'data' in lrqst:
                    if lrqst['code'] == 0:
                        if 'totp_session_token' in lrqst['data']:
                            tfa = ''
                            while True:
                                while tfa == "":
                                    tfa = input('Введите код 2FA:')
                                else:
                                    auth2 = requests.get(f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                    if auth2['code'] == 0:
                                        c1 = 1
                                        acs_tkn = auth2['data']['access_token']
                                        rfr_tkn = auth2['data']['refresh_token']
                                        uid = auth2['data']['user_id']
                                        return acs_tkn, rfr_tkn, uid
                                    else:
                                        print(Fore.RED + 'Ошибка')
                                        tfa = ''
                        else:
                            c1 = 1
                            acs_tkn = lrqst['data']['access_token']
                            rfr_tkn = lrqst['data']['refresh_token']
                            uid = lrqst['data']['user_id']
                            return acs_tkn, rfr_tkn, uid

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={maild}&password={replaces(pwd)}").json()
            #print(lrqst)
            if 'data' in lrqst:
                if lrqst['code'] == 0:
                    if 'totp_session_token' in lrqst['data']:
                        tfa = ''
                        while True:
                            while tfa == "":
                                tfa = input('Введите код 2FA:')
                            else:
                                auth2 = requests.get(
                                    f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                if auth2['code'] == 0:
                                    c1 = 1
                                    acs_tkn = auth2['data']['access_token']
                                    rfr_tkn = auth2['data']['refresh_token']
                                    uid = auth2['data']['user_id']
                                    return acs_tkn, rfr_tkn, uid
                                else:
                                    print(Fore.RED + 'Ошибка')
                                    tfa = ''
                    else:
                        c1 = 1
                        acs_tkn = lrqst['data']['access_token']
                        rfr_tkn = lrqst['data']['refresh_token']
                        uid = lrqst['data']['user_id']
                        return acs_tkn, rfr_tkn, uid
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')

def params():
    global border, id, rprice, t2, t1, ttp, qual, offers, summ
    if num == 0:
        id = input(Fore.MAGENTA + "Введите id прототипа:")
        border = input(Fore.MAGENTA + "Введите максимальную цену:")
        rprice = float(input(Fore.MAGENTA + 'Введите минимальную цену перепродажи(0 - если без)'))
        t1 = int(input(Fore.MAGENTA + "Введите время опроса(в секундах):")) * 100
        t2 = int(t1 * 1.2)
    else:
        ttp = input(
            Fore.LIGHTWHITE_EX + "Введите тип вещи(" + Fore.RED + "0 - карточка, " + Fore.YELLOW + "1 - набор, " + Fore.GREEN + "2 - кейс):")
        if int(ttp) == 1 or int(ttp) == 2 or int(ttp) == 3:
            qual = 1
        else:
            qual = int(input(
                Fore.LIGHTWHITE_EX + "Введите качество прототипа(" + Fore.CYAN + "1 - голубь, " + Fore.MAGENTA + "2 - синяя, " + Fore.MAGENTA + "3 - фиол, " + Fore.RED + "4 - красная, " + Fore.YELLOW + "5 - голд):"))
        offers = int(input(Fore.MAGENTA + 'Сколько смотрим предложений?'))
        border = float(input(Fore.MAGENTA + "Введите максимальную цену:"))
        if offers == '':
            offers = 1
        t1 = int(input(Fore.MAGENTA + "Введите время опроса(в секундах):")) * 100
        t2 = int(t1 * 1.2)

def check():
    global price1
    revprice = rprice
    while True:
        summ = 0
        glst = requests.get(f"https://monopoly-one.com/api/market.getListing?thing_prototype_id={id}").json()['data']['things'][0]
        #print(glst)
        price = glst['price']
        if price != price1:
            print(Fore.LIGHTBLACK_EX + f"Цена: {price}₽")
        cprice = str(float(price) * 100)
        if float(price) <= float(border):
            tid = glst['thing_id']
            buy = requests.get(f"https://monopoly-one.com/api/market.buy?thing_id={tid}&price={cprice}&access_token={acs_tkn}").json()
            err = buy['code']
            if err != 0:
                print(Fore.RED + f'Ошибка {err}')
                if err == 1:
                    refresh()
            else:
                balance = requests.get(f'https://monopoly-one.com/api/execute.wallet?access_token={acs_tkn}').json()['result']['info']['balance']
                summ = float(summ) + float(price)
                print(Fore.GREEN + f"Купил за {price}₽. На балансе осталось: {balance}₽. Потрачено:{round(summ,2)}₽")
                if revprice > 0:
                    time.sleep(random.randint(1,500)/100)
                    if (revprice*0.85) <= price:
                        revprice = round((price+0.1)/0.85,2)
                    rebuy = requests.get(f'https://monopoly-one.com/api/market.sell?thing_id={tid}&access_token={acs_tkn}&price={revprice}').json()['code']
                    if rebuy == 0:
                        print(Fore.GREEN + f'Выставил за {revprice}₽')
                    else:
                        print(Fore.RED + 'Ошибка перепродажи')
                time.sleep(random.randint(300,500)/100)
            time.sleep(1)
        price1=price
        time.sleep(random.randint(t1, t2)/100)

def checkmulti():
    global price1
    summ = 0
    while True:
        if ttp == '' or qual == '':
            exit()
        else:
            ms = requests.get(f"https://monopoly-one.com/api/market.search?access_token={acs_tkn}&thing_type={ttp}&quality={qual}&offset=0&count={offers}").json()
            if 'data' in ms:
                for i in range(0,offers):
                    mst = ms['data']['things'][i]
                    price = mst['price']
                    print(Fore.LIGHTBLACK_EX + f'Цена: {price}₽')
                    if float(price) <= float(border):
                        cprice = str(float(price) * 100)
                        tid = mst['thing_prototype_id']
                        tid = requests.get(f"https://monopoly-one.com/api/market.getListing?thing_prototype_id={tid}&count=1").json()['data']['things'][0]['thing_id']
                        brand = mst['title']
                        buy = requests.get(f"https://monopoly-one.com/api/market.buy?thing_id={tid}&price={cprice}&access_token={acs_tkn}").json()
                        err = buy['code']
                        if err != 0:
                            print(Fore.RED + f'Ошибка {err}')
                            if err == 1:
                                refresh()
                        else:
                            balance = requests.get(f'https://monopoly-one.com/api/execute.wallet?access_token={acs_tkn}').json()['result']['info']['balance']
                            summ = float(summ) + float(price)
                            print(Fore.GREEN + f"Купил {Fore.LIGHTWHITE_EX + brand}"+Fore.GREEN+f" за {price}₽. На балансе осталось: {balance}₽. Потрачено:{round(summ, 2)}₽")
                            time.sleep(random.randint(300,500)/100)
                        time.sleep(1)
                price1=price
                time.sleep(random.randint(t1, t2)/100)

def read():
    global maild, pwd, idd
    with open("config.txt",'r',-1,'utf-8') as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']

def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

def error():
    print('Токен недействителен, либо лимиты')
    if not os.path.exists('error.mp3'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/error.mp3')
    AudioPlayer('error.mp3').play(block=True)
    os.remove('error.mp3')
    exit()


def replaces(var):
    var = var.replace('!','%21')
    var = var.replace('\"', '%22')
    var = var.replace('#', '%23')
    var = var.replace('$', '%24')
    var = var.replace('&', '%26')
    var = var.replace('\'', '%27')
    var = var.replace('(', '%28')
    var = var.replace(')', '%29')
    var = var.replace('!', '%21')
    var = var.replace('*', '%2A')
    var = var.replace('+', '%2B')
    var = var.replace('/', '%2F')
    return var

def refresh():
    global acs_tkn,rfr_tkn
    if c1 == 1:
        refreshh = requests.get(f'https://monopoly-one.com/api/auth.refresh?refresh_token={rfr_tkn}').json()
        if refreshh['code'] == 0:
            print('Обновил токены')
            acs_tkn = refreshh['data']['access_token']
            rfr_tkn = refreshh['data']['refresh_token']
            time.sleep(random.randint(400,800)/100)
            return acs_tkn,rfr_tkn
    else:
        error()

print(Fore.LIGHTWHITE_EX + "Autobuy. Made by AssKiss Studio https://github.com/AssKissStudio/M1Autobuy")
config()
login()
num = int(input(Fore.MAGENTA + 'Включить мульти-версию?:'))
params()
if num == 0:
    while True:
        try:
            check()
        except:
            if c1 == 1:
                refresh()
            else:
                error()
else:
    while True:
        try:
            checkmulti()
        except:
            if c1 == 1:
                refresh()
            else:
                error()
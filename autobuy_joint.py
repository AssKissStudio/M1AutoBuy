import requests, time, random, json, wget, os
from colorama import init, Fore
init(autoreset=True)

price1 = 0
t1me = 0
c1 = 0
def login():
    global c1, acs_tkn
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.BLUE + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 1
        elif mail.count('@') == 1:
            pw = input(Fore.BLUE + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
                if lrqst['code'] == 0:
                    c1 = 1
                    acs_tkn = lrqst['data']['access_token']
                    return acs_tkn
                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            mail = maild
            pw = pwd
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
            if lrqst['code'] == 0:
                c1 = 1
                acs_tkn = lrqst['data']['access_token']
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')
        print(Fore.LIGHTYELLOW_EX + acs_tkn)

def check():
    global price1
    id = input(Fore.BLUE + "Введите id прототипа:")
    border = input(Fore.BLUE + "Введите максимальную цену:")
    rprice = float(input(Fore.BLUE + 'Введите минимальную цену перепродажи(0 - если без)'))
    t1 = int(input(Fore.BLUE + "Введите время опроса(в секундах):")) * 100
    t2 = int(t1 * 1.2)
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
            else:
                balance = requests.get(f'https://monopoly-one.com/api/execute.wallet?access_token={acs_tkn}').json()['result']['info']['balance']
                summ = float(summ) + float(price)
                print(Fore.GREEN + f"Купил за {price}₽. На балансе осталось: {balance}₽. Потрачено:{round(summ,2)}₽")
                if rprice > 0:
                    time.sleep(random.randint(1,500)/100)
                    if (rprice*0.85) <= price:
                        rprice = round((price+0.1)/0.85,2)
                    rebuy = requests.get(f'https://monopoly-one.com/api/market.sell?thing_id={tid}&access_token={acs_tkn}&price={rprice}').json()['code']
                    if rebuy == 0:
                        print(Fore.GREEN + f'Выставил за {rprice}₽')
                    else:
                        print(Fore.RED + 'Ошибка перепродажи')
                time.sleep(random.randint(300,500)/100)
            time.sleep(1)
        price1=price
        time.sleep(random.randint(t1, t2)/100)

def checkmulti():
    ttp = input(Fore.LIGHTWHITE_EX + "Введите тип вещи("+Fore.RED+"0 - карточка, "+Fore.YELLOW+"1 - набор, "+Fore.GREEN+"2 - кейс):")
    if int(ttp) == 1 or int(ttp) == 2 or int(ttp) == 3:
        qual = 1
    else:
        qual = input(Fore.LIGHTWHITE_EX + "Введите качество прототипа("+Fore.CYAN+"1 - голубь, "+Fore.BLUE+"2 - синяя, "+Fore.MAGENTA+"3 - фиол, "+Fore.RED+"4 - красная, "+Fore.YELLOW+"5 - голд):")
    border = input(Fore.BLUE + "Введите максимальную цену:")
    t1 = int(input(Fore.BLUE + "Введите время опроса(в секундах):")) * 100
    t2 = int(t1 * 1.2)
    summ = 0
    global price1
    while True:
        if ttp == '' or qual == '':
            exit()
        else:
            ms = requests.get(f"https://monopoly-one.com/api/market.search?access_token={acs_tkn}&thing_type={ttp}&quality={qual}&offset=0&count=1").json()
            if 'data' in ms:
                mst = ms['data']['things'][0]
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
    with open("config.txt") as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']

def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

print(Fore.LIGHTWHITE_EX + "Autobuy. Made by AssKiss Studio https://github.com/AssKissStudio/M1Autobuy")
config()
login()
num = int(input(Fore.BLUE + 'Включить мульти-версию?:'))
if num == 0:
    check()
else:
    checkmulti()
check()
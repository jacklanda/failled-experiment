# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import os, re, sys, csv, time, base64, random, binascii
import http.cookiejar as cookie
from urllib.parse import quote_plus
sys.path.append('..')

import rsa, csv, requests
from PIL import Image

from src.database import db
from src.crawler import config

HEADERS = config.head('weibo')

class Weibo(object):
    '''
    登陆 weibo.com，重定向至 m.weibo.cn
    '''
    # 构建初始化函数
    def __init__(self):
        super(Weibo, self).__init__()
        self.username = input('请输入你的微博用户名：')
        self.password = input('请输入你的微博密码：')
        self.cookie_path = config.addr('weibo_cookie')
        self.session = requests.Session()
        #通过LWPCookieJar管理cookie
        self.session.cookies = cookie.LWPCookieJar(filename=self.cookie_path)
        self.index_url = "http://weibo.com/login.php"
        self.session.get(self.index_url, headers=HEADERS, timeout=2)
        self.postdata = dict()

    # 微博登陆
    def run_(self):
        #  尝试无capcha情况下登录
        try:
            sever_data = self.pre_login()
            login_url = config.URL('weibo_login') + str(time.time() * 1000)
            login_page = self.session.post(login_url, data=self.postdata, headers=HEADERS)
            ticket_js = login_page.json()
            ticket = ticket_js["ticket"]
        except Exception as e:
            sever_data = self.pre_login()
            login_url = config.URL('weibo_login') + str(time.time() * 1000)
            pcid = sever_data["pcid"]
            self.get_captcha(pcid)
            self.postdata['door'] = input(u"请输入验证码：")
            login_page = self.session.post(login_url, data=self.postdata, headers=HEADERS)
            ticket_js = login_page.json()
            #print(ticket_js)
            ticket = ticket_js["ticket"]
        #  处理登陆后的重定向链接
        save_pa = r'==-(\d+)-'
        ssosavestate = int(re.findall(save_pa, ticket)[0]) + 3600 * 7
        jump_ticket_params = {
            "callback": "sinaSSOController.callbackLoginStatus",
            "ticket": ticket,
            "ssosavestate": str(ssosavestate),
            "client": "ssologin.js(v1.4.19)",
            "_": str(time.time() * 1000),
        }
        jump_url = config.URL('weibo_jump')
        jump_headers = config.head('weibo_jump')
        jump_login = self.session.get(jump_url, params=jump_ticket_params, headers=jump_headers)
        uuid = jump_login.text
        uuid_pa = r'"uniqueid":"(.*?)"'
        uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
        web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
        weibo_page = self.session.get(web_weibo_url, headers=HEADERS)
        Mheaders = config.head('weibo_mheader')

        # m.weibo.cn 登录的 url 拼接
        _rand = str(time.time())
        mParams = {
            "url": "https://m.weibo.cn/",
            "_rand": _rand,
            "gateway": "1",
            "service": "sinawap",
            "entry": "sinawap",
            "useticket": "1",
            "returntype": "META",
            "sudaref": "",
            "_client_version": "0.6.26",
        }
        murl = config.URL('weibo_murl')
        mhtml = self.session.get(murl, params=mParams, headers=Mheaders)
        mhtml.encoding = mhtml.apparent_encoding
        mpa = r'replace\((.*?)\);'
        mres = re.findall(mpa, mhtml.text)

        # 关键的跳转步骤，这里不出问题，基本就成功了。
        Mheaders["Host"] = "passport.weibo.cn"
        self.session.get(eval(mres[0]), headers=Mheaders)
        mlogin = self.session.get(eval(mres[0]), headers=Mheaders)
        # print(mlogin.status_code)
        # 进过几次 页面跳转后，m.weibo.cn 登录成功，下次测试是否登录成功
        Mheaders["Host"] = "m.weibo.cn"
        Set_url = config.URL('weibo_cn')
        pro = self.session.get(Set_url, headers=Mheaders)
        pa_login = r'isLogin":true,'
        login_res = re.findall(pa_login, pro.text)
        # print(login_res)

        # 可以通过 session.cookies 对 cookies 进行下一步相关操作
        self.session.cookies.save()
        ID = config.string('mid')
        start_crawl(ID)
        # print("*"*50)
        # print(self.cookie_path)

    #获取加密后的用户名
    def get_su(self):
        """
        对 email 地址和手机号码 先 javascript 中 encodeURIComponent
        对应 Python 3 中的是 urllib.parse.quote_plus
        然后在 base64 加密后decode
        """
        username_quote = quote_plus(self.username)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 通过预登陆获取：servertime, nonce, pubkey, rsakv
    def get_server_data(self, su):
        pre_url = config.URL('weibo_pre') + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=" + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=HEADERS)
        sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
        return sever_data

    # 加密密码
    def get_pw(self, servertime, nonce, pubkey):
        # 通过RSA算法对密码进行加密
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)  # 拼接明文js加密文件中得到
        message = message.encode("utf-8")
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    # 返回验证码
    def get_captcha(self, pcid):
        # 获取验证码，并且用PIL打开
        addr_ = config.addr('cap_addr')
        cap_url = config.URL('weibo_cap') + str(int(random.random() * 100000000)) + "&s=0&p=" + pcid
        cap_page = self.session.get(cap_url, headers=HEADERS)
        with open(addr_, 'wb') as f:
            f.write(cap_page.content)
            f.close()
        try:
            im = Image.open(addr_)
            im.show()
            im.close()
        except Exception as e:
            print(u"请到自定目录下，找到验证码后输入")

    # 预登陆
    def pre_login(self):
        # su 是加密后的用户名
        su = self.get_su()
        sever_data = self.get_server_data(su)
        servertime = sever_data["servertime"]
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        showpin = sever_data["showpin"]  # 这个参数的意义待明确
        password_secret = self.get_pw(servertime, nonce, pubkey)
        self.postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "https://passport.weibo.com",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password_secret,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            "cdult": "38",
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'TEXT'
        }
        return sever_data

# 加载cookie
def get_cookies():
    addr_ = config.addr('weibo_cookie')
    cookies = cookie.LWPCookieJar(addr_)
    cookies.load(ignore_discard=True, ignore_expires=True)
    # 将cookie转换为字典对象
    cookie_dict = requests.utils.dict_from_cookiejar(cookies)
    return cookie_dict

# 构造post请求参数
def info_parser(data):
    id,time,text =  data['id'],data['created_at'],data['text']
    user = data['user']
    uid,username,following,followed,gender = \
        user['id'],user['screen_name'],user['follow_count'],user['followers_count'],user['gender']
    return {
        'wid':id,
        'time':time,
        'text':text,
        'uid':uid,
        'username':username,
        'following':following,
        'followed':followed,
        'gender':gender
    }

# 执行爬取任务
def start_crawl(ID):
    base_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'
    next_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}'
    page = 1
    id_type = 0
    comment_count = 0
    requests_count = 1
    create_csv()
    cookie_dict = get_cookies()
    res = requests.get(url=base_url.format(ID,ID), headers=HEADERS, cookies=cookie_dict)
    while True:
        print('正在解析页面：{}'.format(page))
        page += 1
        try:
            max_id, comment_count, wdata = parse_data(res, comment_count)
        except:
            max_id = 0
            print('本页面解析失败咯~')
            id_type += 1
        time.sleep(5)
        res = requests.get(url=next_url.format(ID, ID, max_id, id_type), headers=HEADERS, cookies=cookie_dict)
        requests_count += 1
        if page > 200:
            break
        #print(res.status_code)

def parse_data(res, comment_count):
    data = res.json()['data']
    wdata = []
    id_ = data['max_id']
    #print(id_)
    for c in data['data']:
        comment_count += 1
        row = info_parser(c)
        wdata.append(row)
        if c.get('comments', None):
            temp = []
            for cc in c.get('comments'):
                temp.append(info_parser(cc))
                wdata.append(info_parser(cc))
                comment_count += 1
            row['comments'] = temp
        #print(row)
        store_db(row)
    return id_, comment_count, wdata

# 将数据写入数据库
def store_db(dic):
    try:
        client = db.client()
        database_ = client['data_experiment']
        col_ = database_['weibo']
    except:
        print('MongoDB未启动!')
        return None
    text = re.findall('[\u4e00-\u9fa5]+', dic['text'])
    text = ''.join(text)
    dic_ = {
            'username': dic['username'],
            'gender': dic['gender'],
            'content': text
            }
    store_csv(dic_)
    db.insert(dic_, col_)
    store_txt(dic_['content'])

# 将数据写入到.txt文件中
def store_txt(data):
    with open('./metadata/raw_txt/weibo.txt', mode='w+', encoding='utf-8') as f:
        f.write(f'{data}\n')

# 创建.csv文件
def create_csv():
    with open('./metadata/微博评论.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['用户名', '性别', '评论内容'])

# 将数据写入.csv文件中
def store_csv(data):
    with open('./metadata/微博评论.csv', mode='w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['username'], data['gender'], data['content']])


if __name__ == '__main__':
    username =""  # 用户名（注册的手机号）
    password = ""  # 密码
    cookie_path = "../../metadata/cookie.txt"  # 保存cookie 的文件名称
    mid = '4526713860918359'  #  肖战工作室致歉声明(新浪娱乐)评论页面 mid
    Weibo(username, password, cookie_path).run_()
    start_crawl(get_cookies(), mid)
    print('「微博」爬取完成')

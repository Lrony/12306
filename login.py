import requests
import json
import utils
from fake_useragent import UserAgent
from urllib import parse

class LoginTic(object):

    def __init__(self):
        self.session = requests.session()
        self.ua = UserAgent(verify_ssl=False)
        self.headers = {
            "User-Agent": self.ua.random,
            "Host":"kyfw.12306.cn",
            "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
        }

    # 登陆
    def login(self):
        # 打开登陆页面
        url = "https://kyfw.12306.cn/otn/login/init"
        self.session.get(url, headers=self.headers)

        data = {
            "username":USERNAME,
            "password":PASSWORD,
            "appid":"otn"
        }
        # 发送登陆信息
        url = "https://kyfw.12306.cn/passport/web/login"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            # TODO 登陆失败几率大，无解
            if response.text.find("<ul id=\"error\" >")>0:
                utils.print_error_info('登陆失败，请确认信息无误后重新提交')
                exit()
            result = json.loads(response.text)
            # print(result.get("result_message"), result.get("result_code"))
            if result.get("result_code") != 0:
                return False

        data = {
            "appid":"otn"
        }
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        response = self.session.post(url, headers=self.headers, data=data)
        newapptk = ""
        if response.status_code == 200:
            result = json.loads(response.text)
            newapptk = result.get("newapptk")

        data = {
            "tk":newapptk
        }
        url = "https://kyfw.12306.cn/otn/uamauthclient"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            try:
                result = json.loads(response.text)
            except:
                utils.print_error_info('登陆解析错误，请重新提交')
                exit()
            if result.get("result_message") == "验证通过":
                return True
            return False

        # url = "https://kyfw.12306.cn/otn/index/initMy12306"
        # response = self.session.get(url, headers=self.headers)
        # print(response.text)
        # if response.status_code == 200 and response.text.find("我的12306") != -1:
        #     return True
        # return False

    # 查询未出行票
    def queryOrder(self):
        url = 'https://kyfw.12306.cn/otn/queryOrder/queryMyOrder'
        data = {
            'queryType':2,
            'queryStartDate':'2018-01-18',
            'queryEndDate':'2018-02-21',
            'come_from_flag':'my_order',
            'pageSize':8,
            'pageIndex':0,
            'query_where':'G',
            'sequeue_train_name':''
        }
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            try:
                result = json.loads(response.text)
            except:
                utils.print_error_info("查询余票解析错误，请重新提交")
                exit()
            print("当前未出行余票：",result.get("data").get("order_total_number"))

    # 请求验证码
    def captcha(self):
        data = {
            "login_site": "E",
            "module": "login",
            "rand": "sjrand",
            "0.17231872703389062":""
        }
        param = parse.urlencode(data)
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?{}".format(param)
        response = self.session.get(url, headers=self.headers)
        with open('captcha.jpg','wb') as f:
            f.write(response.content)
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

    # 检查验证码
    def captcha_check(self, solution):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        soList = solution.split(',')
        yanSol = ['40,40','110,40','180,40','250,40','40,110','110,110','180,110','250,110']
        yanList = []
        for item in soList:
            yanList.append(yanSol[int(item)])
        yanStr = ','.join(yanList)
        data = {
            'login_site':'E',
            'rand':'sjrand',
            'answer':yanStr
        }
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            return True if result.get("result_code") == "4" else False
        return False


if __name__ == '__main__':
    login = LoginTic();
    captcha = login.captcha()
    if login.captcha_check(captcha):
        print("验证码校验成功！")
        print("正在登陆...")
        if login.login():
            print("登陆成功！")
        else:
            print("登陆失败！")
    else:
        print("验证码校验失败！")

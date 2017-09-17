# -*-coding:utf-8-*-
# 用于实现知乎页面的模拟登录，并保存cookie,下次直接使用cookie登录，等到失效了，再重新登录
# 类来实现
__author__ = "dream_01"

import re
import os
import time
import requests
import http.cookiejar as cookielib  # py2-> cookielib/ python3->http.cookiejar
from lxml import etree

# 登录功能
class ZhuhuLogin(object):
    def __init__(self):
        # 构造用于网络请求的session
        self.session = requests.session()
        self.account = "123@qq.com"  # 你自己的账号手机号或者邮箱
        self.password = "123456"  # 你自己的密码
        self.login_total = 3  # 尝试登录的次数

        # 构造请求头，注意，有时候电脑版本的知乎登录需要点击倒立字体，这时可以通过伪造手机的UA来跳过验证码环节
        # 好像利用手机的UA也需要输入验证码，不过不是倒立字体，这时候就把验证码保存到本地，手动输入
        computerUA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        phoneUA = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/60.0.3112.113 Mobile Safari/537.36"
        self.headers = {
            "Host": "www.zhihu.com",
            "Origin": "https://www.zhihu.com",
            "Referer": "https://www.zhihu.com/signin?next=/",
            "User-Agent": phoneUA
        }

    # 获取_xsrf参数
    def get_xsrf(self):
        response = self.session.get("https://www.zhihu.com/signin?next=/", headers=self.headers).content
        xsrf_token = etree.HTML(response).xpath("//input[@name='_xsrf']/@value")[0]  # 它返回了一个列表，包含三个，选第一个就好
        return xsrf_token

    # 验证码的处理
    # 参考了fuck-login里的代码
    def get_captcha(self):
        randomtime = str(int(time.time() * 1000))
        captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                     randomtime + "&type=login"
        captcharesponse = self.session.get(url=captchaurl, headers=self.headers)
        with open('checkcode.gif', 'wb') as f:
            f.write(captcharesponse.content)
            f.close()
        # os.startfile('checkcode.gif')  # 打开验证码 只能在window下使用
        captcha = input('请输入验证码：')
        print(captcha)
        return captcha

    # 进行登录的过程，分为邮箱登录和手机登录，可以通过正则表达式进行判断
    # 保存cookie,用于下次直接访问
    def zhihu_login(self):
        # 给请求头添加新的参数
        xsrf_token = self.get_xsrf()
        headers1 = dict(self.headers)
        headers1['X-Xsrftoken'] = xsrf_token
        headers1['X-Requested-With'] = 'XMLHttpRequest'
        post_data = {
            "_xsrf": xsrf_token,
            "captcha": self.get_captcha(),
            "password": self.password
        }
        # 正则表达式，1开头，然后接10位数字
        if re.match("^1\d{10}", self.account):
            print("手机号登录")
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data["phone_num"] = self.account
        elif "@" in self.account:
            post_url = "https://www.zhihu.com/login/email"
            post_data["email"] = self.account
        else:
            print("请输入正确的账号...")

        # 正式发出请求POST
        response = self.session.post(post_url, headers=headers1, data=post_data)
        print("服务器端返回响应码：", response.status_code)
        re_j = response.json()
        # 登录失败会返回这样的json
        # {'errcode': 1991829, 'r': 1, 'data': {'captcha': '请提交正确的验证码 :('}, 'msg': '请提交正确的验证码 :('}
        if re_j["r"] == 1:
            print("验证码问题，登录失败")
        print(re_j)

    # 判断是否登录,也是参考了fuck-login里的代码
    def is_login(self):
        profile_url = 'https://www.zhihu.com/settings/profile'
        # 拒绝给他重定向，看到最真实的状态码
        response = self.session.get(url=profile_url, headers=self.headers, allow_redirects=False)

        if response.status_code == 200:  # 200是数字，不是字符
            name = etree.HTML(response.content).xpath("//div[@id='rename-section']/span/text()")[0]
            print("登录成功！你好，{}!".format(name))
            return True

        else:
            print("第{}次登录失败,请重新登录".format(4-self.login_total))
            print(response.status_code)
            self.login_total -= 1  # 登录次数减一
            if self.login_total > 1:
                return self.login()
            print("很尴尬，连续3次你都没有登录成功。。")
            return False

    # cookies文件保存接口
    def save_cookies(self):
        self.session.cookies.save()

    # 登录接口，判断是否有cookie文件，如果有则直接加载cookie，如果没有则进行完整登录过程
    def login(self):
        self.session.cookies = cookielib.LWPCookieJar(filename='zhihucookie')
        try:
            self.session.cookies.load(ignore_discard=True)
            print("cookie 文件加载成功")
            if not self.is_login():  # 文件加载后，没有登录成功，可能cookies失效
                print("cookie文件好像有错...老老实实登录吧。")
                self.zhihu_login()  # 进行登录过程
        except:
            print('cookie 文件未能加载，请登录')
            self.zhihu_login()
            if self.is_login():
                self.save_cookies()  # 能够成功登录才保存它的cookies,如果有错就别保存了，害人

if __name__ == '__main__':
    # 实例化我们登录类
    zhuhu = ZhuhuLogin()
    # 调用登录接口
    zhuhu.login()


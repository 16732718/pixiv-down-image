# -*- coding:UTF-8 -*-
import requests, re
import os
import urllib.request
from imageType import ImageType as getType
import demjson
import shutil
import tools

# 获取项目跟路径
ap = os.path.abspath(
    os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../") + '/image/'

# proxy_addr = {'https': 'http://85.202.161.113:3128'}
proxy_addr = None


class ParseImage:
    def __init__(self, pid, url, cookie):
        self.url = url
        self.pid = pid
        self.cookie = cookie
        # 设置代理
        if proxy_addr is not None:
            proxy = urllib.request.ProxyHandler({'http': proxy_addr})
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
        # 设置请求链接次数
        requests.adapters.DEFAULT_RETRIES = 5

        # 解析长图


def parseMany(self):
    downUrl = self.url
    pid = self.pid
    cookie = self.cookie
    try:
        image = getType(downUrl, pid, cookie)
        pages_meta_src = image.verifyType()
        if len(pages_meta_src) <= 1:
            return False

        headers = {
            'Connection': 'close',
            "referer": downUrl,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            # 'cookie': 'first_visit_datetime_pc=2019-12-20+18%3A13%3A26; p_ab_id=7; p_ab_id_2=5; p_ab_d_id=306959876; yuid_b=IIkjOGE; __utmc=235335808; __utmz=235335808.1576833208.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=16f229551802fd-02abe7b03e2726-1d336b5a-1aeaa0-16f22955181546; _ga=GA1.2.1256740233.1576833208; _gid=GA1.2.357067091.1576834341; PHPSESSID=16632113_Hs9oMXw9sM5uAszjlFpcO1dCnc0XDzgT; device_token=badb9b870fd2d8ba5f3ac7275774c141; privacy_policy_agreement=1; c_type=21; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16632113=1^9=p_ab_id=7=1^10=p_ab_id_2=5=1^11=lang=zh=1; ki_r=; ki_s=202660%3A0.0.0.0.0; is_sensei_service_user=1; ki_t=1576834355073%3B1576910058277%3B1576950334828%3B2%3B52; __utma=235335808.1256740233.1576833208.1576949709.1576955702.15; CNZZDATA1276301425=462193367-1576830705-https%253A%252F%252Fwww.baidu.com%252F%7C1576953517; tag_view_ranking=8p2ehmu0sL~0xsDLqCEW6~RTJMXD26Ak~ZBoVMjk2oM~dHKaZSWbKf~jzPVr0N9Jq~6myIQ92SZ6~WY-Uhwrtfh~W4_X_Af3yY~JBqkgBEhOH~Ie2c51_4Sp~eLGuAzPy_R~-WrwnYvTU5~y6Qpy01Kgs~WTDFSL5kCR~8Mo6Wlb27P~KnQLb0cwLA~XRqQX2P5MM~n8NBqFBTsX~HSqq-q8tIk~ekrvdFpe1b~e6H2wjZ2SQ~fhgmb2xvlh~Bwd9sLjDel~ZXd7qGBw6J~9-BUhzFH84~ux8ydyywfL~VJhR4eHQ1N~TI6O3Ek8pJ~5oPIfUbtd6~dmEOWBaSxk~kmI1Ik3Jj1~BtXd1-LPRH~9XeTUIEp5o~l2ReAhbJw4~iktStcfLPR~g7sFAm80ep~EWR7JDW6jH~jsFcKOD1PR~ClLaegOm3j~osjGBvsNDJ~m6izElPb9F~IHcUtVa8fG~AgktOIHB78~mD2QlxPPH-~WlelQm0jTC~-B0wgi3Odg~nvF1pzp1dN~8P6NsTLoqe~yJmpGIDuUR~nV_SZr9njo~6293srEnwa~wpZyk6tXZD~QFH3XBi4J2~AnNKd2Rhiy~maeViZl0cX~V0wxmDLlG5~moEyDUmkHh~LxdXI7-B2R~ea8DYxYsty~pP1H19QjPk~Jl9T4xLTsV~afkK5n8h7Y~Lt-oEicbBr~cI9lsTcB1z~bcAbumoPKA~L27-AblyFD~gt5sOFt0UZ~011_f_ZdVQ~5sExEHA8P5~sQC4pGQx9E~jfnUZgnpFl~pxB8sVjqrS~z3OAa1RcDy~4yreIPS1XN~bUXHQY7zb4~3Anjjy8-8B~fOV5CUOQuW~ndw6L4JNet~Ls1hXMvZGb~_hSAdpN9rx~xjfPXTyrpQ~EYKvAzoQAp~gCo_8c0aW0~MM6RXH_rlN~3cT9FM3R6t~XlclKZZFlI~uHu-ITME2U~xmwljnQd6K~gppWzI_6Vi~VjfGRc-I2B~BAOGRD22OG~c9duRWuz2X~2XSW7Dtt5E~s7u3FUQEIO~UnkXx-XEph~xc1eoD9xjo~oTbzOa-MeZ~wUJ4yr_RfP~Ltq1hgLZe3; __utmb=235335808.23.10.1576955702'
        }
        for k, v in enumerate(pages_meta_src):
            request_header = urllib.request.Request(url=pages_meta_src[k]['urls']['regular'], headers=headers)
            f = urllib.request.urlopen(request_header)
            data = f.read()
            suffix = pages_meta_src[k]['urls']['regular'][
                     pages_meta_src[k]['urls']['regular'].rindex('.') + 1:len(pages_meta_src[k]['urls']['regular'])]
            savePath = ap + pid + '_' + str(k) + '.' + suffix
            print('ManySavePath:', savePath)
            with open(savePath, 'wb') as code:
                code.write(data)
    except IOError:
        print(IOError)
        return 'failed'

    return True

    # 解析单图


def parseOne(self):
    url = self.url
    pid = self.pid
    cookie = self.cookie
    headers = {
        "authority": "i.pximg.net",
        "referer": url,
        "scheme": "https",
        "accept": "image / webp, image / apng, image / *, * / *;q = 0.8",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "zh - CN, zh;q = 0.9, en;q = 0.8",
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        # 'cookie': 'first_visit_datetime_pc=2019-12-20+18%3A13%3A26; p_ab_id=7; p_ab_id_2=5; p_ab_d_id=306959876; yuid_b=IIkjOGE; __utmc=235335808; __utmz=235335808.1576833208.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=16f229551802fd-02abe7b03e2726-1d336b5a-1aeaa0-16f22955181546; _ga=GA1.2.1256740233.1576833208; _gid=GA1.2.357067091.1576834341; PHPSESSID=16632113_Hs9oMXw9sM5uAszjlFpcO1dCnc0XDzgT; device_token=badb9b870fd2d8ba5f3ac7275774c141; privacy_policy_agreement=1; c_type=21; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16632113=1^9=p_ab_id=7=1^10=p_ab_id_2=5=1^11=lang=zh=1; ki_r=; ki_s=202660%3A0.0.0.0.0; is_sensei_service_user=1; ki_t=1576834355073%3B1576910058277%3B1576950334828%3B2%3B52; __utma=235335808.1256740233.1576833208.1576949709.1576955702.15; CNZZDATA1276301425=462193367-1576830705-https%253A%252F%252Fwww.baidu.com%252F%7C1576953517; tag_view_ranking=8p2ehmu0sL~0xsDLqCEW6~RTJMXD26Ak~ZBoVMjk2oM~dHKaZSWbKf~jzPVr0N9Jq~6myIQ92SZ6~WY-Uhwrtfh~W4_X_Af3yY~JBqkgBEhOH~Ie2c51_4Sp~eLGuAzPy_R~-WrwnYvTU5~y6Qpy01Kgs~WTDFSL5kCR~8Mo6Wlb27P~KnQLb0cwLA~XRqQX2P5MM~n8NBqFBTsX~HSqq-q8tIk~ekrvdFpe1b~e6H2wjZ2SQ~fhgmb2xvlh~Bwd9sLjDel~ZXd7qGBw6J~9-BUhzFH84~ux8ydyywfL~VJhR4eHQ1N~TI6O3Ek8pJ~5oPIfUbtd6~dmEOWBaSxk~kmI1Ik3Jj1~BtXd1-LPRH~9XeTUIEp5o~l2ReAhbJw4~iktStcfLPR~g7sFAm80ep~EWR7JDW6jH~jsFcKOD1PR~ClLaegOm3j~osjGBvsNDJ~m6izElPb9F~IHcUtVa8fG~AgktOIHB78~mD2QlxPPH-~WlelQm0jTC~-B0wgi3Odg~nvF1pzp1dN~8P6NsTLoqe~yJmpGIDuUR~nV_SZr9njo~6293srEnwa~wpZyk6tXZD~QFH3XBi4J2~AnNKd2Rhiy~maeViZl0cX~V0wxmDLlG5~moEyDUmkHh~LxdXI7-B2R~ea8DYxYsty~pP1H19QjPk~Jl9T4xLTsV~afkK5n8h7Y~Lt-oEicbBr~cI9lsTcB1z~bcAbumoPKA~L27-AblyFD~gt5sOFt0UZ~011_f_ZdVQ~5sExEHA8P5~sQC4pGQx9E~jfnUZgnpFl~pxB8sVjqrS~z3OAa1RcDy~4yreIPS1XN~bUXHQY7zb4~3Anjjy8-8B~fOV5CUOQuW~ndw6L4JNet~Ls1hXMvZGb~_hSAdpN9rx~xjfPXTyrpQ~EYKvAzoQAp~gCo_8c0aW0~MM6RXH_rlN~3cT9FM3R6t~XlclKZZFlI~uHu-ITME2U~xmwljnQd6K~gppWzI_6Vi~VjfGRc-I2B~BAOGRD22OG~c9duRWuz2X~2XSW7Dtt5E~s7u3FUQEIO~UnkXx-XEph~xc1eoD9xjo~oTbzOa-MeZ~wUJ4yr_RfP~Ltq1hgLZe3; __utmb=235335808.23.10.1576955702'
        'cookie': cookie
    }
    s = requests.Session()  # 模拟登陆的Session
    try:
        if proxy_addr is not None:
            req = s.get(url, proxies=proxy_addr, headers=headers)
        else:
            req = s.get(url, headers=headers)
    except IOError:
        return str(IOError)
    image_url = re.findall('"regular":"https://i.pximg.net/img-master[\w\W]{1,100}.jpg"', req.text)
    regular = image_url[0][image_url[0].index(':"') + 2:len(image_url[0]) - 1]

    request_header = urllib.request.Request(url=regular, headers=headers)
    f = urllib.request.urlopen(request_header)
    data = f.read()
    suffix = regular[regular.rindex('.') + 1:len(regular)]
    savePath = ap + pid + '.' + suffix
    print('OneSavePath:', savePath)
    try:
        with open(savePath, 'wb') as code:
            code.write(data)
    except IOError:
        print(IOError)
        return False

    return True

    # 解析gif


def parseGif(self):
    ugoira_headers = {
        'Connection': 'close',
        "referer": self.url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        # 'cookie': 'first_visit_datetime_pc=2019-12-20+18%3A13%3A26; p_ab_id=7; p_ab_id_2=5; p_ab_d_id=306959876; yuid_b=IIkjOGE; __utmc=235335808; __utmz=235335808.1576833208.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=16f229551802fd-02abe7b03e2726-1d336b5a-1aeaa0-16f22955181546; _ga=GA1.2.1256740233.1576833208; _gid=GA1.2.357067091.1576834341; PHPSESSID=16632113_Hs9oMXw9sM5uAszjlFpcO1dCnc0XDzgT; device_token=badb9b870fd2d8ba5f3ac7275774c141; privacy_policy_agreement=1; c_type=21; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16632113=1^9=p_ab_id=7=1^10=p_ab_id_2=5=1^11=lang=zh=1; ki_r=; ki_s=202660%3A0.0.0.0.0; is_sensei_service_user=1; ki_t=1576834355073%3B1576910058277%3B1576950334828%3B2%3B52; __utma=235335808.1256740233.1576833208.1576949709.1576955702.15; CNZZDATA1276301425=462193367-1576830705-https%253A%252F%252Fwww.baidu.com%252F%7C1576953517; tag_view_ranking=8p2ehmu0sL~0xsDLqCEW6~RTJMXD26Ak~ZBoVMjk2oM~dHKaZSWbKf~jzPVr0N9Jq~6myIQ92SZ6~WY-Uhwrtfh~W4_X_Af3yY~JBqkgBEhOH~Ie2c51_4Sp~eLGuAzPy_R~-WrwnYvTU5~y6Qpy01Kgs~WTDFSL5kCR~8Mo6Wlb27P~KnQLb0cwLA~XRqQX2P5MM~n8NBqFBTsX~HSqq-q8tIk~ekrvdFpe1b~e6H2wjZ2SQ~fhgmb2xvlh~Bwd9sLjDel~ZXd7qGBw6J~9-BUhzFH84~ux8ydyywfL~VJhR4eHQ1N~TI6O3Ek8pJ~5oPIfUbtd6~dmEOWBaSxk~kmI1Ik3Jj1~BtXd1-LPRH~9XeTUIEp5o~l2ReAhbJw4~iktStcfLPR~g7sFAm80ep~EWR7JDW6jH~jsFcKOD1PR~ClLaegOm3j~osjGBvsNDJ~m6izElPb9F~IHcUtVa8fG~AgktOIHB78~mD2QlxPPH-~WlelQm0jTC~-B0wgi3Odg~nvF1pzp1dN~8P6NsTLoqe~yJmpGIDuUR~nV_SZr9njo~6293srEnwa~wpZyk6tXZD~QFH3XBi4J2~AnNKd2Rhiy~maeViZl0cX~V0wxmDLlG5~moEyDUmkHh~LxdXI7-B2R~ea8DYxYsty~pP1H19QjPk~Jl9T4xLTsV~afkK5n8h7Y~Lt-oEicbBr~cI9lsTcB1z~bcAbumoPKA~L27-AblyFD~gt5sOFt0UZ~011_f_ZdVQ~5sExEHA8P5~sQC4pGQx9E~jfnUZgnpFl~pxB8sVjqrS~z3OAa1RcDy~4yreIPS1XN~bUXHQY7zb4~3Anjjy8-8B~fOV5CUOQuW~ndw6L4JNet~Ls1hXMvZGb~_hSAdpN9rx~xjfPXTyrpQ~EYKvAzoQAp~gCo_8c0aW0~MM6RXH_rlN~3cT9FM3R6t~XlclKZZFlI~uHu-ITME2U~xmwljnQd6K~gppWzI_6Vi~VjfGRc-I2B~BAOGRD22OG~c9duRWuz2X~2XSW7Dtt5E~s7u3FUQEIO~UnkXx-XEph~xc1eoD9xjo~oTbzOa-MeZ~wUJ4yr_RfP~Ltq1hgLZe3; __utmb=235335808.23.10.1576955702'
    }
    headers = {
        "authority": "i.pximg.net",
        "referer": self.url,
        "scheme": "https",
        "accept": "image / webp, image / apng, image / *, * / *;q = 0.8",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "zh - CN, zh;q = 0.9, en;q = 0.8",
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        # 'cookie': 'first_visit_datetime_pc=2019-12-20+18%3A13%3A26; p_ab_id=7; p_ab_id_2=5; p_ab_d_id=306959876; yuid_b=IIkjOGE; __utmc=235335808; __utmz=235335808.1576833208.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=16f229551802fd-02abe7b03e2726-1d336b5a-1aeaa0-16f22955181546; _ga=GA1.2.1256740233.1576833208; _gid=GA1.2.357067091.1576834341; PHPSESSID=16632113_Hs9oMXw9sM5uAszjlFpcO1dCnc0XDzgT; device_token=badb9b870fd2d8ba5f3ac7275774c141; privacy_policy_agreement=1; c_type=21; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16632113=1^9=p_ab_id=7=1^10=p_ab_id_2=5=1^11=lang=zh=1; ki_r=; ki_s=202660%3A0.0.0.0.0; is_sensei_service_user=1; ki_t=1576834355073%3B1576910058277%3B1576950334828%3B2%3B52; __utma=235335808.1256740233.1576833208.1576949709.1576955702.15; CNZZDATA1276301425=462193367-1576830705-https%253A%252F%252Fwww.baidu.com%252F%7C1576953517; tag_view_ranking=8p2ehmu0sL~0xsDLqCEW6~RTJMXD26Ak~ZBoVMjk2oM~dHKaZSWbKf~jzPVr0N9Jq~6myIQ92SZ6~WY-Uhwrtfh~W4_X_Af3yY~JBqkgBEhOH~Ie2c51_4Sp~eLGuAzPy_R~-WrwnYvTU5~y6Qpy01Kgs~WTDFSL5kCR~8Mo6Wlb27P~KnQLb0cwLA~XRqQX2P5MM~n8NBqFBTsX~HSqq-q8tIk~ekrvdFpe1b~e6H2wjZ2SQ~fhgmb2xvlh~Bwd9sLjDel~ZXd7qGBw6J~9-BUhzFH84~ux8ydyywfL~VJhR4eHQ1N~TI6O3Ek8pJ~5oPIfUbtd6~dmEOWBaSxk~kmI1Ik3Jj1~BtXd1-LPRH~9XeTUIEp5o~l2ReAhbJw4~iktStcfLPR~g7sFAm80ep~EWR7JDW6jH~jsFcKOD1PR~ClLaegOm3j~osjGBvsNDJ~m6izElPb9F~IHcUtVa8fG~AgktOIHB78~mD2QlxPPH-~WlelQm0jTC~-B0wgi3Odg~nvF1pzp1dN~8P6NsTLoqe~yJmpGIDuUR~nV_SZr9njo~6293srEnwa~wpZyk6tXZD~QFH3XBi4J2~AnNKd2Rhiy~maeViZl0cX~V0wxmDLlG5~moEyDUmkHh~LxdXI7-B2R~ea8DYxYsty~pP1H19QjPk~Jl9T4xLTsV~afkK5n8h7Y~Lt-oEicbBr~cI9lsTcB1z~bcAbumoPKA~L27-AblyFD~gt5sOFt0UZ~011_f_ZdVQ~5sExEHA8P5~sQC4pGQx9E~jfnUZgnpFl~pxB8sVjqrS~z3OAa1RcDy~4yreIPS1XN~bUXHQY7zb4~3Anjjy8-8B~fOV5CUOQuW~ndw6L4JNet~Ls1hXMvZGb~_hSAdpN9rx~xjfPXTyrpQ~EYKvAzoQAp~gCo_8c0aW0~MM6RXH_rlN~3cT9FM3R6t~XlclKZZFlI~uHu-ITME2U~xmwljnQd6K~gppWzI_6Vi~VjfGRc-I2B~BAOGRD22OG~c9duRWuz2X~2XSW7Dtt5E~s7u3FUQEIO~UnkXx-XEph~xc1eoD9xjo~oTbzOa-MeZ~wUJ4yr_RfP~Ltq1hgLZe3; __utmb=235335808.23.10.1576955702'
    }
    videoPath=ap + self.pid + '.mp4'
    if os.path.exists(videoPath):
        os.remove(videoPath)


    ugoira_meta = 'https://www.pixiv.net/ajax/illust/' + self.pid + '/ugoira_meta'
    try:
        if proxy_addr is not None:
            ugoira_meta_body = requests.get(ugoira_meta, proxies=proxy_addr, headers=ugoira_headers,
                                            cookies={'PHPSESSID': self.cookie})
        else:
            ugoira_meta_body = requests.get(ugoira_meta, headers=ugoira_headers,
                                            cookies={'PHPSESSID': self.cookie})

        ugoira_meta_src = demjson.decode(ugoira_meta_body.text)['body']
        body_len = len(ugoira_meta_src)
        # 大于0代表是动图
        if body_len <= 0:
            return False

        session = requests.session()

        if proxy_addr is not None:
            zip_body = session.get(ugoira_meta_src['src'], proxies=proxy_addr, headers=headers,
                                   cookies={'PHPSESSID': self.cookie})
        else:
            zip_body = session.get(ugoira_meta_src['src'], headers=headers,
                                   cookies={'PHPSESSID': self.cookie})

        print('GifSavePath:', ap + self.pid)
        # 拿到ugoira_meta中的zip文件
        with open(ap + self.pid + '.zip', 'ab') as f:
            f.write(zip_body.content)
        # 压缩文件
        tools.unzipSingle(ap + self.pid + '.zip', ap + self.pid + '/', '')
        # 文件生成可以按需来设置
        # 生成html canvas
        tools.saveHtml(ap, self.pid)
        # 生成视频
        tools.saveVideo(ap, self.pid)
        # 生成gif
        tools.CreateShelltoGif(ap, self.pid)
        # 删除文件
        # shutil.rmtree(ap + self.pid)
        # shutil.rmtree(ap + self.pid + '.mp4')

    except IOError:
        return str(IOError)

    return True

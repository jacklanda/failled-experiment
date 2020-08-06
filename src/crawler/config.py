# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
def head(typ):
    if typ == 'zhihu':
        return {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'TE': 'Trailers',
                }
    elif typ == 'bilibili':
        return {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection': 'keep-alive',
                'Referer': 'https://www.bilibili.com/video/BV1QZ4y1M7Yt?from=search&seid=2802586105820332741',
                'TE': 'Trailers'
                }
    elif typ == 'weibo':
        return {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection': 'keep-alive',
                'Referer': 'https://www.weibo.com/',
                'TE': 'Trailers',
                }
    elif typ == 'weibo_jump':
        return {
                'Host': 'passport.weibo.com',
                'Referer': 'https://weibo.com/',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
                }
    elif typ == 'weibo_mheader':
        return {
                'Host': 'login.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
                }


def URL(typ):
    if typ == 'zhihu':
        return  'https://www.zhihu.com/api/v4/questions/406914039/'\
                'answers?include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info'\
                '%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason'\
                '%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent'\
                '%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time'\
                '%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized'\
                '%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content'\
                '%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[*].topics&limit=20&platform=desktop&sort_by=default'
    elif typ == 'bilibili':
        return 'https://api.bilibili.com/x/v2/reply?type=1&oid=371221592'
    elif typ == 'weibo_login':
        return 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_'
    elif typ == 'weibo_jump':
        return 'https://passport.weibo.com/wbsso/login'
    elif typ == 'weibo_murl':
        return 'https://login.sina.com.cn/sso/login.php'
    elif typ == 'weibo_cn':
        return 'https://m.weibo.cn'
    elif typ == 'weibo_pre':
        return 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su='
    elif typ == 'weibo_cap':
        return 'https://login.sina.com.cn/cgi/pin.php?r='

def addr(name):
    if name == 'cap_addr':
        return './metadata/img/captcha.jpg'
    if name == 'weibo_cookie':
        return './metadata/cookie.txt'

def string(name):
    if name == 'mid':
        return '4526713860918359'

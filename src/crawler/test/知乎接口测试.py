# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import time

import requests

target_url_zhihu = 'https://www.zhihu.com/question/406914039'

'''「?」问号后代表接口的查询参数，其中：
    参数include代表一系列的额外查询信息，
    参数limit代表一次请求查询的json数量，
    参数offset代表查询的起始位置，从零开始
    参数sort_by可选：默认排序/按发表时间排序'''
url_seq_zhihu = 'https://www.zhihu.com/api/v4/questions/406914039/'\
        'answers?include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info'\
        '%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason'\
        '%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent'\
        '%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time'\
        '%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized'\
        '%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content'\
        '%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[*].topics&limit=20&offset=15&platform=desktop&sort_by=default'

# 知乎采用最简单的反爬形式：限定User-Agent请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

print(time.strftime('%Y-%m-%d %H:%M:%S'))
try:
    res = requests.get(url_seq_zhihu, headers=HEADERS)
    status = res.status_code
    if status == 200:
        print(res.content.decode())
except requests.exceptions.RequestException as e:
    print(e)
print(time.strftime('%Y-%m-%d %H:%M:%S'))


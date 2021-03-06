import requests,json,urllib.parse
import pymysql,time,random

# 数据库
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1234',
    db = 'myjob',
    port = 3306,
    charset = 'utf8'
)
# 获取操作游标
cur = db.cursor()
# 目标网址
url = 'https://www.lagou.com/jobs/positionAjax.json?'
# 请求头
headers = {
    'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.2.1114654082.1544950720; user_trace_token=20181216165838-c70b7cab-0110-11e9-9329-525400f775ce; LGUID=20181216165838-c70b811e-0110-11e9-9329-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167b63d7224829-01102ae244bc01-2711639-1327104-167b63d72251b5%22%2C%22%24device_id%22%3A%22167b63d7224829-01102ae244bc01-2711639-1327104-167b63d72251b5%22%7D; LG_LOGIN_USER_ID=eb280d34abaf72630d88d9c0faccf41ccd3e44589f0096e1c522abe6ad7d86b3; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=15; index_location_city=%E5%8C%97%E4%BA%AC; _gid=GA1.2.469968022.1545359540; WEBTJ-ID=20181221103220-167ce9b44c110e-0774a1637c081a-2711639-1327104-167ce9b44c2205; JSESSIONID=ABAAABAAADEAAFI6EB026D8F6A7B3D55B75A5D65F7DD1E8; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544950720,1545359540,1545359547,1545359586; _putrc=E9804999C1C234C2123F89F2B170EADC; login=true; unick=%E9%82%B5%E6%99%93%E9%9B%AF; gate_login_token=1de814123a19f36ce52295ee4ce7fc09c309eaef5657d48ad4dd03159c2f9569; TG-TRACK-CODE=jobs_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545457160; _gat=1; LGSID=20181222133915-eae8b8f0-05ab-11e9-88ba-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; LGRID=20181222133915-eae8bbe2-05ab-11e9-88ba-525400f775ce; SEARCH_ID=d26cd01e02b34f798260df8b82c3f5e0'
}
# 初始页码
page = 1

# kd = 'Python'
# kd = 'Java'
# kd = 'PHP'
# kd = 'C'
# kd = 'iOS'
# kd = 'HTML5'
# kd = 'go'
kd = 'shell'
while True:
#     携带数据
    data = {
        'first': 'true',
        'pn': str(page),
        'kd': kd,
    }
    # 解析
    data = urllib.parse.urlencode(data)
    #发送请求
    response = requests.post(url,data=data,headers=headers)
    #获得json文件 并将其转python字典格式
    json_data = json.loads(response.text)
    result = json_data['content']['positionResult']['result']  # 职位信息
    resultSize = json_data['content']['positionResult']['resultSize']  # 当页职位条数
    print('正在爬取第' + str(page) + '页')
    for message in result:
        city = message['city']#城市
        jobname = message['positionName']#职位名
        company = message['companyFullName']#公司名称
        salary = message['salary']#工资
        welfare = message['positionAdvantage']#福利待遇
        address = message['district']#地址
        education = message['education']#学历要求
        workyear = message['workYear']#工作经历
        link = 'https://www.lagou.com/jobs/' + str(message['positionId']) + '.html'#详情地址
        createtime  = message['createTime']#发布时间
        # mysql语句
        try:
            db.ping(reconnect=True)
            cur.execute(
                "insert into job (city,jobname,company,salary,welfare,address,education,workyear,link,createtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (city, jobname, company, salary, welfare, address, education, workyear, link, createtime)
            )
            db.commit()#提交
        # 错误回滚
        except Exception as e:
            # 打印错误
            print(e)
            db.rollback()
    # 随机休眠
    time.sleep(random.randint(1,5))
    # 判断是否是最后一页 不是page+1
    if resultSize == 15:
        page += 1
    else:
        db.close()
        break




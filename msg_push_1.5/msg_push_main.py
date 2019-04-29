#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 邹浩文 <627622230@qq.com>
# +-------------------------------------------------------------------

#+--------------------------------------------------------------------
#|   宝塔消息推送
#+--------------------------------------------------------------------
import sys
sys.path.append('/www/server/panel/class')
import json, os, time, public, re, requests, psutil, threading, datetime, base64

os.chdir("/www/server/panel")


class msg_push_main:
    # 用户列表
    def __init__(self):
        self.__confPath = 'plugin/msg_push/config.json'
        self.__mail_list = 'plugin/msg_push/mail_list.json'
        self.__first_check = 'plugin/msg_push/firstcheck.json'
        self.setpath="/www/server/panel"
        self.disk_error_code = 0
        self.cpu_error_code = 0
        self.net_error_code = 0
        self.mem_error_code = 0
        self.url_error_code = 0
        self.site_error_code = 0
        self.mysql_error_code = 0
        self.site_dict = {}
        self.url_dict ={}
        self.r_list = []
        self.t_list = []
        self.r_tmp_list = []
        self.t_tmp_list = []
        self.process_cpu = {}
        self.process_mem = {}
        self.cpunum = 1
        self.hour = 0
        self.ed = {}
        self.total_path = "/www/server/total/total"

    # 启动监控服务
    def StartServer(self, get):
        if self.check_monitor():
            a = self.CheckServer(get)
            if a["status"] == True:
                return public.returnMsg(True, '服务已经在运行了无需再启动')
            os.system("nohup /usr/bin/python %s/plugin/msg_push/msg_push_main.py &" % self.setpath)
            a = self.CheckServer(get)
            if a["status"] == True:
                os.system("/usr/bin/echo '1' > %s/plugin/msg_push/open.txt" % self.setpath)
                return public.returnMsg(True, '服务启动成功')
            else:
                return public.returnMsg(False, '服务启动失败')
        else:
            return public.returnMsg(False, '请先打开 面板监控<br>开启方法: 菜单-->监控-->开启监控</br>')

    def StopServer(self, get):
        a = self.CheckServer(get)
        if a["status"] != True:
            return public.returnMsg(True, '服务没有启动')
        else:
            a = public.ExecShell("ps aux|grep msg_push|grep -v 'grep'|awk 'NR==1 {print $2}'")[0].strip("\n")
            os.system("kill -9 %s" % a)
            os.system("/usr/bin/echo '0' > %s/plugin/msg_push/open.txt" % self.setpath)
            return public.returnMsg(True, '服务停止成功')

    def CheckServer(self, get):
        a = public.ExecShell("ps aux|grep 'msg_push'|grep -v 'grep'|wc -l")[0].strip()
        if a == "0":
            return public.returnMsg(False, '服务未启动')
        else:
            return public.returnMsg(True, '服务已启动')
    # 新建消息推送
    def create_msg_even(self,get):

        if self.__check_msg_even(get.push_name):
            return public.returnMsg(False, '指定消息推送已存在')
        if not self.check_monitor():
            return public.returnMsg(False, '请先开启面板监控')
        if get.check_type != "report":
            if int(get.push_time) < 10:
                return public.returnMsg(False, '邮件发送间隔时间不能小于10分钟')
        getdata = get.__dict__
        data = {}
        for k in getdata.keys():
            if k == "args" or k == "data" or k == "s" or k == "action" or k == "name":
                continue
            if "value" in k:
                try:
                    n = int(getdata[k])
                    if n > 100 or n <= 0:
                        return public.returnMsg(False, '阈值不能小于等于0或大于100')
                except:
                    return public.returnMsg(False, '请输入整数')
            if "time" in k:
                try:

                    n = int(getdata[k])
                    if n <= 0:
                        return public.returnMsg(False, '不能输入负数或0')
                except:
                    return public.returnMsg(False, '请输入整数')
            if k=="mysql":
                if getdata[k] == "1":
                    if not os.path.exists("/www/server/panel/plugin/masterslave"):
                        return public.returnMsg(False, '没有安装【Mysql主从】插件，无法启用监控')
            if k=="report":
                if not os.path.exists("/www/server/panel/plugin/total"):
                    return public.returnMsg(False, '没有安装【网站监控报表】插件插件，无法启用报表发送')
            data[k] = getdata[k]
        if "url_list" in data.keys():
            site = {
                'url_list':data["url_list"],
                'key':data["key"],
                'site_name':data["site_name"],
                'adv':data["adv"]
            }
            data.pop("url_list")
            data.pop("key")
            data.pop("adv")
            data.pop("site_name")
            data["site"] = site
        conf_data = self.__read_config(self.__confPath)
        conf_data.append(data)
        self.__write_config(self.__confPath, conf_data)
        public.WriteLog('消息推送', ' 添加监控[' + data["push_name"] + ']')
        return public.returnMsg(True, '添加成功')

    # 检查事件是否存在
    def __check_msg_even(self,push_name):
        conf_data = self.__read_config(self.__confPath)
        for i in conf_data:
            if i["push_name"] == push_name:
                return i

    # 获取事件列表
    def get_msgpush_list(self, get):
        conf = self.__read_config(self.__confPath)
        for i in conf:
            if not i.has_key("push_time"):
                i["push_time"] = "10"
            try:
                if i["site"]:
                    i["url_list"] = i["site"]["url_list"]
                    i["key"] = i["site"]["key"]
                    i["adv"] = i["site"]["adv"]
                    i["site_name"] = i["site"]["site_name"]
                    i.pop("site")
            except:
                pass
        return conf



    # 修改事件监控阈值
    def modify_msgpush(self,get):
        data = self.get_msgpush_list(get)
        push_name = get.push_name
        get_data = get.__dict__
        keys = {"push_type":"推送类型",
                "cpu_alarm_value":"CPU阈值",
                "cpu_check_time":"CPU检查周期",
                "mem_alarm_value":"内存阈值",
                "mem_check_time":"内存检查周期",
                "net_alarm_value":"带宽预警阈值",
                "net_check_time":"带宽监测时间",
                "net_bandwidth":"最大带宽",
                "site_check_url":"检查URL",
                "site_check_word":"检查关键字",
                "disk_alarm_value":"监控磁盘阈值",
                "url_list":"监控域名",
                "adv":"精确站点监控",
                "key":"监控站点关键字",
                "site_name":"监控站点",
                "push_time":"推送间隔时间",
                "report":"报表发送时间",
                "report_type":"报表类型",
                "netcard":"网卡",
                "open":"检测开关"}
        alter_options = ""
        try:
            push_time = get.push_time
        except:
            get.push_time = 10
        if int(get.push_time) < 10:
            return public.returnMsg(False, '邮件发送间隔时间不能小于10分钟')
        for i in data:
            if push_name == i["push_name"]:
                if not i.has_key("push_time"):
                    i["push_time"] = "10"
                for k in keys.keys():
                    try:
                        if get_data[k]:
                            if "value" in k:
                                try:
                                    a = int(get_data[k])
                                    if a <= 0 or a > 100:
                                        return public.returnMsg(False, '阈值不能小于等于0或大于100')
                                except:
                                    return public.returnMsg(False, '请输入整数')
                            if "time" in k:
                                try:
                                    a = int(get_data[k])
                                    if a <= 0:
                                        return public.returnMsg(False, '不能输入负数或0')
                                except:
                                    return public.returnMsg(False, '请输入整数')
                            if str(i[k]) != get_data[k]:
                                ldata = ""
                                udata = ""
                                if "value" in k:
                                    ldata += i[k] + "%"
                                    udata += get_data[k] + "%"
                                elif "time" in k:
                                    ldata += i[k] + "分钟"
                                    udata += get_data[k] + "分钟"
                                elif "open" in k or "adv" in k:
                                    if get_data[k] == "1":
                                        udata += "开启"
                                        ldata += "关闭"
                                    else:
                                        udata += "关闭"
                                        ldata += "开启"
                                elif "bandwidth" in k:
                                    udata += get_data[k] + "Mbps"
                                    ldata += i[k] + "Mbps"
                                elif "url" in k:
                                    udata += get_data[k]
                                    ldata += i[k]
                                else:
                                    udata += get_data[k]
                                    ldata += i[k]
                                alter_options += '推送名称 "%s" 的%s "%s" 修改为 "%s"' % (push_name, keys[k], ldata, udata)
                                i[k] = get_data[k]
                    except:
                        pass
                if alter_options:
                    public.WriteLog('消息推送', ' 修改配置[' + alter_options + ']')
        for i in data:
            try:
                if i["url_list"]:
                    site = {
                        "url_list":i["url_list"],
                        "key":i["key"],
                        "adv":i["adv"],
                        "site_name":i["site_name"]
                    }
                    i.pop("url_list")
                    i.pop("key")
                    i.pop("adv")
                    i.pop("site_name")
                    i["site"] = site
            except:
                pass

        self.__write_config(self.__confPath, data)
        return public.returnMsg(True, '修改成功')

    #删除推送事件
    def remove_msgpush(self,get):
        data = self.__read_config(self.__confPath)
        push_name = get.push_name
        for i in range(len(data)):
            if data[i]["push_name"] == push_name:
                del data[i]
                self.__write_config(self.__confPath, data)
                public.WriteLog('消息推送', ' 删除配置[' + push_name + ']')
                return public.returnMsg(True, '删除成功')
    # 第一次打开提醒设置邮件
    def CheckMailFirst(self, get):
        if not public.readFile(self.__first_check):
            public.writeFile(self.__first_check,"1")
        a = public.readFile(self.__first_check)
        e = self.get_email_list(get)["emails"]
        if a == "1" and not e:
            b = a + "1"
            public.writeFile(self.__first_check,b)
            return a
        else:
            return 0

    # 获取邮箱列表
    def get_email_list(self, get):
        if not os.path.exists(self.__mail_list):
            public.writeFile(self.__mail_list, '[]')
        emails = public.readFile(self.__mail_list)
        data = {}
        data['emails'] = json.loads(emails)
        return data

    # 添加邮箱地址
    def add_email(self, get):
        emails = self.get_email_list(get)['emails']
        if len(emails) > 2: return public.returnMsg(False, '最多添加3个收件地址!')
        if get.email in emails: return public.returnMsg(False, '指定收件地址已存在!')
        # rep = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
        rep = "\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}"
        if not re.search(rep,get.email):
            return public.returnMsg(False, '请输入正确的邮箱格式')
        emails.append(get.email)
        public.WriteLog('消息推送', '添加收件地址[' + get.email + ']')
        self.__write_config(self.__mail_list,emails)
        return public.returnMsg(True, '添加成功')

    # 删除邮箱地址
    def remove_email(self, get):
        emails = self.get_email_list(get)['emails']
        emails.remove(get.email)
        public.WriteLog('消息推送', '删除收件地址[' + get.email + ']')
        self.__write_config(self.__mail_list,emails)
        return public.returnMsg(True, '删除成功')


    # 读配置
    def __read_config(self, path):
        if not os.path.exists(path) or not public.readFile(path):
                public.writeFile(path, '[]')
        upBody = public.readFile(path)
        return json.loads(upBody)

    # 写配置
    def __write_config(self ,path, data):
        return public.writeFile(path, json.dumps(data))

    # 外部读配置
    def read_config(self):
        return self.__read_config(self.__confPath)
    # 监控CPUIO
    def GetCpuIo(self,starttime):
        # 取指定时间段的CpuIo
        data = public.M('cpuio').dbfile('system').where("addtime>=? AND addtime<=?",(starttime, time.time())).field('id,pro,mem').order('id asc').select()
        return data

    # 检测硬盘使用
    def Check_hd_use(self):
            cmd_get_hd_use = '/bin/df'
            try:
                fp = os.popen(cmd_get_hd_use)
            except:
                ErrorInfo = r'get_hd_use_error'
                return ErrorInfo
            re_obj = re.compile(r'^/dev/.+\s+(?P<used>\d+)%\s+(?P<mount>.+)')
            hd_use = {}
            for line in fp:
                match = re_obj.search(line)
                if match:
                    hd_use[match.groupdict()['mount']] = match.groupdict()['used']
            fp.close()
            return hd_use
    # 返回{'/www/wwwroot/www_youbadbad_cn/files': '6', '/boot': '14', '/': '61'}

    def CheckInodeUse(self):
        cmd_get_hd_use = '/bin/df -i'
        try:
            fp = os.popen(cmd_get_hd_use)
        except:
            ErrorInfo = r'get_hd_use_error'
            return ErrorInfo
        re_obj = re.compile(r'^/dev/.+\s+(?P<used>\d+)%\s+(?P<mount>.+)')
        hd_use = {}
        for line in fp:
            match = re_obj.search(line)
            if match:
                hd_use[match.groupdict()['mount']] = match.groupdict()['used']
        fp.close()
        return hd_use

    # 检测网络用量
    def GetNetWorkIo(self, starttime):
        #取指定时间段的网络Io
        data =  public.M('network').dbfile('system').where("addtime>=? AND addtime<=?",(starttime,time.time())).field('id,up,down').order('id asc').select()
        return data
    # 发送邮件
    def __send_mail(self, url, data):
        return public.httpPost(url, data)

    # 检查站点健康
    def check_site_health(self,i):
        site_check_word = i["site_check_word"]
        site_check_url = i["site_check_url"]
        try:
            site_data = requests.get(site_check_url,timeout=5)
            site_data.encoding = 'utf-8'
            self.url_dict[site_check_url] = site_check_word in site_data.text
        except:
            self.url_dict[site_check_url] = False

    def get_local_site_list(self,get=None):
        site = {}
        site_list = public.M("sites").field("id,name").select()
        for i in site_list:
            domain_list = public.M("domain").where("pid=?", (i["id"],)).field("name").select()
            l = []
            for domain in domain_list:
                l.append(domain["name"])
            site[i["name"]] = l
        return site

    def check_local_site_health(self,url):
        url = "http://"+url
        try:
            a = requests.get(url, timeout=5)
            self.site_dict[url] = a.status_code
        except:
            self.site_dict[url] = "timeout"

    def ThreadingCheck(self,i):
        site_list = i["site"]
        if site_list["adv"] == "1":
            i["site_check_word"] = site_list["key"]
            u = site_list["url_list"]
            i["site_check_url"] = u
            t = threading.Thread(target=self.check_site_health, args=(i,))
            t.start()
        else:
            u = site_list["url_list"]
            t = threading.Thread(target=self.check_local_site_health, args=(u,))
            t.start()

    # 检查监控是否开启
    def check_monitor(self):
        monitor_file = 'data/control.conf'
        if os.path.exists(monitor_file):
            return True

    # URL回调
    def callback_url(self):
        # 构造post请求
        pass
    # 获取日志
    def get_logs(self, get):
        import page
        page = page.Page()
        count = public.M('logs').where('type=?', (u'消息推送',)).count()
        limit = 12
        info = {}
        info['count'] = count
        info['row'] = limit
        info['p'] = 1
        if hasattr(get, 'p'):
            info['p'] = int(get['p'])
        info['uri'] = get
        info['return_js'] = ''
        if hasattr(get, 'tojs'):
            info['return_js'] = get.tojs
        data = {}

        # 获取分页数据
        data['page'] = page.GetPage(info, '1,2,3,4,5,8')
        data['data'] = public.M('logs').where('type=?', (u'消息推送',)).order('id desc').limit(
            bytes(page.SHIFT) + ',' + bytes(page.ROW)).field('log,addtime').select()
        return data

    def CheckPort(self,ip,port):
        import socket
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(5)
        try:
            sk.connect((ip, int(port)))
            return True
        except:
            return False

    def GetNetCard(self,get):
        import psutil
        a = psutil.net_io_counters(pernic=True)
        l = []
        for i in a.keys():
            if i != "lo":
                l.append(i)
        return l

    def GetProcessCpuPercent(self,i):
        try:
            pp = psutil.Process(i)
            if pp.name() not in self.process_cpu.keys():
                self.process_cpu[pp.name()] = float(pp.cpu_percent(interval=0.1))
                return
            self.process_cpu[pp.name()]+=float(pp.cpu_percent(interval=0.1))
        except:
            pass
    # 取占用最大cpu的进程
    def ThreadingGetProcessCpuPercent(self):
        self.process_cpu = {}
        for i in psutil.pids():
            time.sleep(0.2)
            threading.Thread(target=self.GetProcessCpuPercent,args=(i,)).start()
        time.sleep(3)
        maxk = max(self.process_cpu,key=self.process_cpu.get)
        if maxk == "gunicorn":
            del(self.process_cpu[maxk])
        maxk = max(self.process_cpu, key=self.process_cpu.get)
        return [maxk,self.process_cpu[maxk]]

    # 取占用内存最高的进程
    def GetProcessMemPercent(self,i):
        try:
            pp = psutil.Process(i)
            if pp.name() not in self.process_mem.keys():
                self.process_mem[pp.name()] = float(pp.memory_info().rss / 1024 / 1024)
                return
            self.process_mem[pp.name()]+=float(pp.memory_info().rss / 1024 / 1024)
        except:
            pass

    def ThreadingGetProcessMemPercent(self):
        self.process_mem = {}
        for i in psutil.pids():
            time.sleep(0.2)
            threading.Thread(target=self.GetProcessMemPercent,args=(i,)).start()
        time.sleep(3)
        maxk = max(self.process_mem,key=self.process_mem.get)
        if maxk == "gunicorn":
            del(self.process_mem[maxk])
        maxk = max(self.process_mem, key=self.process_mem.get)
        return [maxk,self.process_mem[maxk]]

    def __get_file_json(self,filename,defaultv = {}):
        try:
            if not os.path.exists(filename): return defaultv;
            return json.loads(public.readFile(filename))
        except:
            os.remove(filename)
            return defaultv
    # 获取站点名称
    def GetNameOfSites(self):
        sites = []
        getsites = public.M('sites').field('name').select()
        for s in getsites:
            sites.append(s["name"])
        return sites

    def GetLogs(self,data,sites_data,get_type):
        # data 日志文件内容
        # sites_data 预设的dict
        # get_type 获取类型，时日月报表
        if get_type == "network":
            for n in data:
                sites_data[get_type] += data[n]
        else:
            for time in data:
                for c in data[time]:
                    if c not in sites_data[get_type]:
                        sites_data[get_type][c] = 0
                    sites_data[get_type][c] += int(data[time][c])
    def GetTime(self,time):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        hour = datetime.datetime.now().hour
        day = datetime.datetime.now().day
        lastHour = hour - 1
        yesterday = day - 1
        lastMonth = month - 1
        times = {"year": year, "month": month, "day": day, "hour": hour,"lastHour":lastHour,"yesterday":yesterday,"lastMonth":lastMonth}
        for i in times:
            if times[i] < 10:
                times[i] = "0"+str(times[i])
            else:
                times[i] = str(times[i])
        return times[time]

    # 获取监控报表
    def GetSiteReport(self,siteName,gettime):
        if gettime == "daily":
            date = datetime.datetime.now()+datetime.timedelta(days=-1)
            date = date.strftime("%Y-%m-%d")
        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        sites_data = {"client":{},"network":0,"request":{},"spider":{}}
        get_types = ["client","network","request","spider"]
        logpath = self.total_path+"/"+siteName
        if os.path.exists(logpath):
            for get_type in get_types:
                if gettime == "month":
                    logfiles = os.listdir(logpath+"/"+get_type)
                    if "total.json" in logfiles:
                        logfiles.remove("total.json")
                    for f in logfiles:
                        if str(self.GetTime("year"))+"-"+str(self.GetTime("lastMonth")) in f:
                            lg = "%s/%s/%s" % (logpath, get_type, f)
                            data = self.__get_file_json(lg)
                            self.GetLogs(data,sites_data,get_type)
                    continue
                lg = "%s/%s/%s.json" % (logpath,get_type,date)
                data = self.__get_file_json(lg)
                if gettime == "daily":
                    self.GetLogs(data,sites_data,get_type)
                else:
                    for time in data:
                        if time == gettime:
                            sites_data[get_type] = data[time]
        else:
            pass
        return sites_data

    def GetAllSiteReport(self,report_type,report,email_data,warningUrl):
        serverip = "\nServer IP: 【 %s 】 " % public.GetLocalIp()
        sites = self.GetNameOfSites()
        hourList = self.GetTimeStamp()
        sites_data = {}
        r_file = "%s/plugin/msg_push/rsc.txt" % self.setpath
        rsc = public.readFile(r_file)
        if not rsc:
            rsc = {"day":"","month":""}
            public.writeFile(r_file,json.dumps(rsc))
        rsc = json.loads(rsc)
        #将前端传入的时间小于10的加前面加0
        list = []
        if "," in report:
            report = report.split(",")
            for i in report:
                if int(i) < 10:
                    i = "0"+str(i)
                list.append(str(i))
            report = list
        else:
            try:
                if int(report) < 10:
                    report = "0"+str(report)
            except:
                pass
        now = time.time()
        for i in sites:
            if report_type == "hour":
                sites_data[i] = self.GetSiteReport(i, self.GetTime("lastHour"))
            else:
                sites_data[i] = self.GetSiteReport(i, report_type)
        print(self.hour)
        if report_type == "hour":
            for h in hourList:
                if h < now < h + 300:
                    if self.hour == 0:
                        email_data["title"] = "监控报表时报表"
                        email_data["body"] = serverip+self.FormatHtml(sites_data)
                        # print("监控报表时报表" + str(email_data))
                        even = ""
                        # if self.__send_mail(warningUrl, email_data) == "1":
                        #     public.WriteLog('消息推送', "时报表发送成功")
                        if self.__SendMail(email_data,even,warningUrl):
                            self.hour += 1
                            break
                else:
                    if  h + 300 < now < h + 500:
                        self.hour = 0
        elif report_type == "daily":
            if report == self.GetTime("hour"):
                if not rsc["day"]:
                    yesterday = "%s-%s-%s" % (self.GetTime("year"),self.GetTime("month"),self.GetTime("yesterday"))
                    email_data["title"] = "监控报表日报表 %s" % yesterday
                    email_data["body"] = serverip+self.FormatHtml(sites_data)
                    even = ""
                    if self.__SendMail(email_data,even,warningUrl):
                        rsc["day"] = "1"
                        public.writeFile(r_file, json.dumps(rsc))
                    # print("监控报表日报表"+str(email_data))
            else:
                if rsc["day"]:
                    rsc["day"] = ""
                    public.writeFile(r_file, json.dumps(rsc))
        else:
            if report[0] == self.GetTime("day") and self.GetTime("hour") == report[1]:
                if not rsc["month"]:
                    lastMonth =  "%s-%s" % (self.GetTime("year"),self.GetTime("lastMonth"))
                    email_data["title"] = "报表监控月报表 %s" % lastMonth
                    email_data["body"] = serverip+self.FormatHtml(sites_data)
                    even = ""
                    public.writeFile("/tmp/month.html",str(email_data["body"]))
                    # print("监控报表月报表" + str(email_data))
                    if self.__SendMail(email_data,even,warningUrl):
                        rsc["month"] = "1"
                        public.writeFile(r_file, json.dumps(rsc))
            else:
                if rsc["month"]:
                    rsc["month"] = ""
                    public.writeFile(r_file, json.dumps(rsc))


    def FormatHtml(self,sites_data):
        from prettytable import PrettyTable as pt
        # today = datetime.datetime.now().strftime("%Y-%m-%d")
        title = ["站点名", "PV", "UV", "IP", "200", "404", "500", "502", "503", "流量", "请求数", "蜘蛛"]
        table = pt(title)
        try:
            for sd in sites_data:
                data = []
                data.append(sd)
                status = ["pv","uv","ip","200","404","500","502","503"]
                for s in status:
                    if s in sites_data[sd]["request"].keys():
                        data.append(sites_data[sd]["request"][s])
                    else:
                        data.append(0)
                data.append(sites_data[sd]["network"])
                rql = ["GET","PUT","POST","DELETE"]
                rq_times = 0
                for r in rql:
                    if r in sites_data[sd]["request"].keys():
                        rq_times += int(sites_data[sd]["request"][r])
                data.append(rq_times)
                spiders = 0
                for s in sites_data[sd]["spider"]:
                    spiders += int(sites_data[sd]["spider"][s])
                data.append(spiders)
                table.add_row(data)
        except Exception as e:
            print(e)
        table.reversesort = True
        text = table.get_html_string(format=True)
        html = '<html>\n<head>\n<meta charset="utf-8">\n%s\n</head>\n</html>' % text
        html = html.replace("cols","all")
        return html


    # 获取24小时时间戳
    def GetTimeStamp(self):
        tsl = []
        for i in range(24):
            d = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % i
            timelist = time.strptime(d, "%Y-%m-%d %H:%M:%S")
            tsl.append(int(time.mktime(timelist)))
        return tsl
    # 判断监控报表是否安装
    def CheckTotal(self,get):
        path = "/www/server/panel/plugin/total/total_main.py"
        if not os.path.exists(path):
            return public.returnMsg(False, '请先安装监控报表')
        else:
            return public.returnMsg(True, '已经安装监控报表')

    # 发送邮件
    def __SendMail(self,email_data,even,warningUrl):
        serverip = "\nServer IP: 【 %s 】 " % public.GetLocalIp()
        if "title" not in email_data.keys() or "body" not in email_data.keys():
            email_data["title"] = serverip + even
            email_data["body"] = serverip +even
        email_data = base64.b64encode(json.dumps(email_data))
        data = {"access_key": self.GetAccessKey(), "data": email_data,
                "token": self.SetToken(email_data)}
        res = self.__send_mail(warningUrl, data)
        # print(res)
        if res == "1":
            if even:
                public.WriteLog('消息推送', "告警邮件发送成功")
            else:
                public.WriteLog('消息推送', "报表发送成功")
            return True
        # else:
        #     public.WriteLog('消息推送', "邮件发送失败 %s" % res)
    # 循环监控代码
    def CheckCPU(self,cache,i,email_data,warningUrl):
        # 检查cpu负载
        starttime = time.time() - int(i["cpu_check_time"]) * 60
        cpu_data = self.GetCpuIo(starttime)
        cpusum = 0
        for cpuio in cpu_data:
            cpusum += int(cpuio["pro"])
        cpu_avg = cpusum / len(cpu_data)
        if int(i["cpu_alarm_value"]) <= cpu_avg:
            evenmd5 = "cpumsg" + public.Md5(str(cpu_avg))
            now = time.time()
            t = now - float(cache["cpumsg"][1])
            push_time = int(i["push_time"])*60
            if cache["cpumsg"][0] != evenmd5 and t >= push_time:
                mxp = self.ThreadingGetProcessCpuPercent()
                cache["cpumsg"][1] = now
                cache["cpumsg"][0] = evenmd5
                even = "CPU已经使用[  %.2f%s  ]超过设定阈值，其中【%s】进程占用cpu最高，占用率为 %.2f%s" % (cpu_avg, "%", mxp[0],float(mxp[1])/int(self.cpunum),"%")
                public.WriteLog('消息推送', even)
                # 判断告警方式发送消息
                self.__SendMail(email_data,even,warningUrl)
                # email_data["title"] = even
                # email_data["body"] = even
                # email_data = base64.b64encode(json.dumps(email_data))
                # data = {"access_key": self.GetAccessKey(), "data": email_data, "token": self.SetToken(email_data)}
                # res = self.__send_mail(warningUrl, data)
                # if res == "1":
                #     public.WriteLog('消息推送', "cpu 告警邮件发送成功")
                self.cpu_error_code += 1
                # if self.__send_mail(warningUrl, email_data) == "1":
                #     public.WriteLog('消息推送', "cpu 告警邮件发送成功")
        else:
            if self.cpu_error_code != 0:
                self.cpu_error_code = 0
                cache["cpumsg"][0] = ""
                even = "cpu 告警状态已经恢复正常"
                public.WriteLog('消息推送', even)
                self.__SendMail(email_data,even,warningUrl)
                # if self.__send_mail(warningUrl, email_data) == "1":
                #     public.WriteLog('消息推送', "cpu 恢复邮件发送成功")

    def CheckDisk(self,cache,i,email_data,warningUrl):
        hd_data = self.Check_hd_use()
        inode_data = self.CheckInodeUse()
        for keys in hd_data:
            use = int(hd_data[keys])
            inode_use = int(inode_data[keys])
            c_use = int(i["disk_alarm_value"])
            if use >= c_use or inode_use >= c_use:
                evenmd5 = "diskmsg" + public.Md5(str(use))
                now = time.time()
                t = now - float(cache["diskmsg"][1])
                push_time = int(i["push_time"]) * 60
                if cache["diskmsg"][0] != evenmd5 and t >= push_time:
                    disk_data = '  %s  目录已经使用 %s%s 空间，inode 已经使用 %s%s' % (keys, use, "%",inode_use,"%")
                    cache["diskmsg"][0] = evenmd5
                    cache["diskmsg"][1] = now
                    even = "磁盘已经使用[  %s  ]超过设定阈值" % disk_data
                    public.WriteLog('消息推送', even)
                    self.__SendMail(email_data, even, warningUrl)
                    self.disk_error_code += 1
                    self.ed[keys] = self.disk_error_code
                    # 判断告警方式发送消息
            else:
                try:
                    if self.ed[keys] != 0:
                        self.ed[keys] = 0
                        cache["diskmsg"][0] = ""
                        even = "磁盘告警状态已经恢复正常"
                        self.__SendMail(email_data, even, warningUrl)
                        public.WriteLog('消息推送', even)
                except:
                    self.ed[keys] = 0

    def CheckNet(self, cache, i, email_data, warningUrl):
        import psutil
        ct = int(i["net_check_time"])
        nb = int(i["net_bandwidth"])
        nv = int(i["net_alarm_value"])
        push_time = int(i["push_time"])
        cache_t = float(cache["netmsg"][1])
        if "netcard" not in i.keys():
            i["netcard"] = "lo"
        net_tmp = psutil.net_io_counters(pernic=True)

        r_tmp = net_tmp[i["netcard"]].bytes_recv
        t_tmp = net_tmp[i["netcard"]].bytes_sent

        if len(self.r_tmp_list) < 2:
            self.r_tmp_list.append(r_tmp)
        else:
            self.r_tmp_list.pop(0)
            self.r_tmp_list.append(r_tmp)
        if len(self.t_tmp_list) < 2:
            self.t_tmp_list.append(t_tmp)
        else:
            self.t_tmp_list.pop(0)
            self.t_tmp_list.append(t_tmp)

        r = int(self.r_tmp_list[-1]) - int(self.r_tmp_list[-2])
        t = int(self.t_tmp_list[-1]) - int(self.t_tmp_list[-2])
        if len(self.r_list) > ct:
            self.r_list.pop(0)
        if len(self.t_list) > ct:
            self.t_list.pop(0)
        self.r_list.append(r)
        self.t_list.append(t)
        rsum = 0
        tsum = 0

        for i in self.r_list:
            rsum += i
        for i in self.t_list:
            tsum += i
        rsum = rsum/1024/ct
        tsum = tsum/1024/ct
        net_bandwidth = nb*1024*nv/ 100
        if rsum >= net_bandwidth and tsum >= net_bandwidth:
            d = "上行带宽 %.2fKB 下行带宽 %.2fKB" % (tsum, rsum)
            even = "带宽已经使用[ %s ]超过设定阈值" % d
            evenmd5 = "netmsg" + public.Md5(even)
            now = time.time()
            t = now - cache_t
            push_time = push_time*60
            if cache["netmsg"][0] != evenmd5 and t >=push_time:
                cache["netmsg"][0] = evenmd5
                cache["netmsg"][1] = now
                public.WriteLog('消息推送', even)
                self.__SendMail(email_data, even, warningUrl)
                self.net_error_code += 1
        else:
            if self.net_error_code != 0:
                self.net_error_code = 0
                cache["netmsg"][0] = ""
                even = "带宽告警状态已经恢复正常"
                self.__SendMail(email_data, even, warningUrl)
                public.WriteLog('消息推送', "带宽告警状态已经恢复正常")

    def CheckMem(self,cache,i,email_data,warningUrl):
        starttime = time.time() - int(i["mem_check_time"]) * 60
        mem_data = self.GetCpuIo(starttime)
        memsum = 0
        for mem in mem_data:
            memsum += int(mem["mem"])
        mem_avg = memsum / len(mem_data)
        if int(i["mem_alarm_value"]) <= mem_avg:
            evenmd5 = "memmsg" + public.Md5(str(mem_avg))
            now = time.time()
            t = now - float(cache["memmsg"][1])
            push_time = int(i["push_time"]) * 60
            if cache["memmsg"][0] != evenmd5 and t >= push_time:
                mxp = self.ThreadingGetProcessMemPercent()
                even = "内存已经使用[  %d%s  ]超过设定阈值，其中【%s】进程占用内存最高，占用率为 %sMB" % (mem_avg, "%", mxp[0],mxp[1])
                cache["memmsg"][0] = evenmd5
                cache["memmsg"][1] = now
                public.WriteLog('消息推送', even)
                self.__SendMail(email_data, even, warningUrl)
                self.mem_error_code += 1
                # 判断告警方式发送消息
        else:
            if self.mem_error_code != 0:
                self.mem_error_code = 0
                cache["memmsg"][0] = ""
                even = "内存告警状态已经恢复正常"
                self.__SendMail(email_data, even, warningUrl)
                public.WriteLog('消息推送', even)

    def CheckUrl(self,cache,i,email_data,warningUrl):
        site_url = i["site_check_url"]
        self.check_site_health(i)
        for u in self.url_dict:
            if not self.url_dict[u]:
                even = "URL [  %s  ] 监控到访问异常" % site_url
                evenmd5 = "sitemsg" + public.Md5(even)
                now = time.time()
                t = now - float(cache["memmsg"][1])
                push_time = int(i["push_time"]) * 60
                if cache["sitemsg"][0] != evenmd5 and t >= push_time:
                    cache["sitemsg"][0] = evenmd5
                    cache["sitemsg"][1] = now
                    public.WriteLog('消息推送', even)
                    self.__SendMail(email_data, even, warningUrl)
                    self.url_error_code += 1
            else:
                if self.url_error_code != 0:
                    self.url_error_code = 0
                    cache["sitemsg"][0] = ""
                    even = "URL告警状态已经恢复正常 [ %s ]" % site_url
                    public.WriteLog('消息推送', even)
                    self.__SendMail(email_data, even, warningUrl)

    def CheckLocalSite(self,cache,i,email_data,warningUrl):
        self.ThreadingCheck(i)
        l = []
        l.append(i["site"]["url_list"])
        if i["site"]["adv"] == "1":
            while len(self.url_dict) !=len(l):
                time.sleep(0.5)
        else:
            while len(self.site_dict) != len(l):
                time.sleep(0.5)

        if self.site_dict:
            a = self.site_dict
        else:
            a = self.url_dict
        for s in a.keys():
            if a[s] != 200 or not a[s]:
                even = "站点 [  %s  ] 监控到访问异常" % s
                evenmd5 = "localsitemsg" + public.Md5(even)
                now = time.time()
                t = now - float(cache["memmsg"][1])
                push_time = int(i["push_time"]) * 60
                if cache["localsitemsg"][0] != evenmd5 and t >= push_time:
                    cache["localsitemsg"][0] = evenmd5
                    cache["localsitemsg"][1] = now
                    public.WriteLog('消息推送', even)
                    self.__SendMail(email_data, even, warningUrl)
                    self.site_error_code += 1
            else:
                if self.site_error_code != 0:
                    self.site_error_code = 0
                    cache["localsitemsg"][0] = ""
                    even = "站点告警状态已经恢复正常 [ %s ]" % s
                    public.WriteLog('消息推送', even)
                    self.__SendMail(email_data, even, warningUrl)

    def CheckMysql(self,cache,email_data,warningUrl,i):
        import panelMysql as pm
        f = "%s/plugin/masterslave/data.json" % self.setpath
        conf = public.readFile(f)
        if os.path.exists(f) and conf != "":
            conf = json.loads(conf)
            try:
                now = time.time()
                t = now - float(cache["memmsg"][1])
                push_time = int(i["push_time"]) * 60
                if "master_ip" in conf.keys():
                    slavestatus = pm.panelMysql().query("show slave status")[0]
                    Slave_IO_Running = slavestatus[10]
                    Slave_SQL_Running = slavestatus[11]
                    if Slave_IO_Running != "Yes" or Slave_SQL_Running != "Yes":
                        even = "mysql主从异常"
                        evenmd5 = "mysqlmsg" + public.Md5(even)
                        if cache["mysqlmsg"][0] != evenmd5 and t >= push_time:
                            cache["mysqlmsg"][0] = evenmd5
                            cache["mysqlmsg"][1] = now
                            self.__SendMail(email_data, even, warningUrl)
                            self.mysql_error_code += 1
                            public.WriteLog('消息推送', "Mysql主从异常")
                    else:
                        if self.mysql_error_code != 0:
                            self.mysql_error_code = 0
                            cache["mysqlmsg"][0] = ""
                            even = "Mysql主从异常恢复"
                            public.WriteLog('消息推送', even)
                            self.__SendMail(email_data, even, warningUrl)
                else:
                    if not self.CheckPort(conf["slave_ip"], conf["slave_port"]):
                        even = '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % conf["slave_ip"]
                        evenmd5 = "mysqlmsg" + public.Md5(even)
                        if cache["mysqlmsg"][0] != evenmd5 and t >= push_time:
                            cache["mysqlmsg"][0] = evenmd5
                            cache["mysqlmsg"][1] = now
                            self.mysql_error_code += 1
                            public.WriteLog('消息推送', even)
                            self.__SendMail(email_data, even, warningUrl)
                            return
                    slavestatus = public.ExecShell(
                        "mysql -h%s -P%s --connect_timeout=3 -u%s -p%s -e 'show slave status\G'" % (
                            conf["slave_ip"], conf["slave_port"], "user" + conf["slave_user"],
                            "pass" + conf["slave_pass"]))[0]
                    Slave_IO_Running = "Slave_IO_Running:\s+(\w+)"
                    Slave_SQL_Running = "Slave_SQL_Running:\s+(\w+)"
                    Slave_IO_Running = re.search(Slave_IO_Running, slavestatus).group(1)
                    Slave_SQL_Running = re.search(Slave_SQL_Running, slavestatus).group(1)
                    if Slave_IO_Running != "Yes" or Slave_SQL_Running != "Yes":
                        even = "mysql主从异常"
                        evenmd5 = "mysqlmsg" + public.Md5(even)
                        if cache["mysqlmsg"][0] != evenmd5 and t >= push_time:
                            cache["mysqlmsg"][0] = evenmd5
                            cache["mysqlmsg"][1] = now
                            self.__SendMail(email_data, even, warningUrl)
                        public.WriteLog('消息推送', "Mysql主从异常！！")
                    else:
                        if self.mysql_error_code != 0:
                            self.mysql_error_code = 0
                            cache["mysqlmsg"][0] = ""
                            even = "Mysql主从异常恢复"
                            public.WriteLog('消息推送', even)
                            self.__SendMail(email_data, even, warningUrl)
            except:
                public.WriteLog('消息推送', "error: " + public.get_error_info())
        else:
            if self.mysql_error_code < 1:
                self.mysql_error_code += 1
                public.WriteLog('消息推送', "主从没有配置")
    def SetToken(self,email_data):
        ufile = "/www/server/panel/data/userInfo.json"
        uconf = public.readFile(ufile)
        if uconf:
            uconf = json.loads(uconf)
            sk = uconf["secret_key"]
        else:
            return False
        token = public.Md5(sk+email_data)
        return token
    def GetAccessKey(self):
        ufile = "/www/server/panel/data/userInfo.json"
        uconf = public.readFile(ufile)
        if uconf:
            uconf = json.loads(uconf)
            ak = uconf["access_key"]
        else:
            return False
        return ak


    # 检查开始
    def checkM(self):
        if self.check_monitor():
            myip = ""
            cache = {"cpumsg":["",0],"diskmsg":["",0],"netmsg":["",0],"memmsg":["",0],"sitemsg":["",0],"mysqlmsg":["",0],"localsitemsg":["",0]}
            warningUrl = "http://www.bt.cn/api/index/send_mail_msg"
            while True:
                mail_list = self.get_email_list(None)["emails"]
                mail_list = ",".join(mail_list)
                email_data = {"email": mail_list}
                conf_data = self.__read_config(self.__confPath)
                self.cpunum = psutil.cpu_count()
                for i in conf_data:
                    if int(i["open"]) == 1:
                        try:
                            if "push_time" not in i.keys():
                                i["push_time"] = "10"
                            if "cpu_alarm_value" in i.keys() and i["cpu_alarm_value"] != "":
                                self.CheckCPU(cache,i,email_data,warningUrl)
                            # 检查磁盘空间
                            if "disk_alarm_value" in i.keys() and i["disk_alarm_value"] != "":
                                self.CheckDisk(cache,i,email_data,warningUrl)
                            # 检测带宽
                            if "net_alarm_value" in i.keys() and i["net_alarm_value"] != "":
                                self.CheckNet(cache,i,email_data,warningUrl)
                            # 检测内存
                            if "mem_alarm_value" in i.keys() and i["mem_alarm_value"] != "":
                                self.CheckMem(cache,i,email_data,warningUrl)
                            # 检测URL健康
                            if "site_check_url" in i.keys() and i["site_check_url"]:
                                self.url_dict = {}
                                self.CheckUrl(cache,i,email_data,warningUrl)
                            # 检测站点
                            if "site" in i.keys() and i["site"]["url_list"]:
                                self.site_dict = {}
                                self.CheckLocalSite(cache, i, email_data, warningUrl)
                            # 检查mysql主从健康
                            if "mysql" in i.keys() and i["mysql"] != "":
                                self.CheckMysql(cache,email_data,warningUrl,i)
                            # 小时报表发送
                            if "report_type" in i.keys():
                                self.GetAllSiteReport(i["report_type"],i["report"],email_data,warningUrl)
                        except Exception as e:
                            print(e)
                time.sleep(60)
        else:
            return public.returnMsg(False, '请先打开 面板监控，开启方法菜单-->监控-->开启监控')


if __name__ == '__main__':
    msg_push = msg_push_main()
    msg_push.checkM()

# class get:
#     pass
# get.disk_alarm_value="80"
# get.push_type="disk"
# get.open="1"
# get.push_time="101"
# get.push_name="磁盘"
#
# m = msg_push_main()
# print(m.modify_msgpush(get))


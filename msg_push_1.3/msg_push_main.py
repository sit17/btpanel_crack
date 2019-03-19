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
import json, os, time, public, re, requests
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
        push_name = get.push_name
        push_type = get.push_type
        check_type = get.check_type
        cpu_alarm_value = get.cpu_alarm_value
        cpu_check_time = get.cpu_check_time
        disk_alarm_value = get.disk_alarm_value
        mem_alarm_value = get.mem_alarm_value
        mem_check_time = get.mem_check_time
        net_alarm_value = get.net_alarm_value
        net_check_time = get.net_check_time
        net_bandwidth = get.net_bandwidth
        site_check_url = get.site_check_url
        site_check_word = get.site_check_word
        open = get.open
        mysql = get.mysql
        url_list = get.url_list
        adv = get.adv
        key = get.key
        site_name = get.site_name
        push_time = get.push_time
        if int(push_time) < 10:
            return public.returnMsg(False, '邮件发送间隔时间不能小于10分钟')
        check_int = [[cpu_alarm_value,disk_alarm_value,mem_alarm_value,net_alarm_value],[cpu_check_time,mem_check_time,net_check_time,net_bandwidth,push_time]]
        for i in range(len(check_int)):
            if i == 0:
                try:
                    for j in check_int[i]:
                        if j:
                            n = int(j)
                            if n > 100 or n <= 0:
                                return public.returnMsg(False, '阈值不能小于等于0或大于100')
                except:
                    return public.returnMsg(False, '请输入整数')
            else:
                try:
                    for j in check_int[i]:
                        if j:
                            n = int(j)
                            if n <= 0:
                                return public.returnMsg(False, '不能输入负数或0')
                except:
                    return public.returnMsg(False, '请输入整数')


        if mysql == "1":
            if check_type == "mysql":
                if not os.path.exists("/www/server/panel/plugin/masterslave"):
                    return public.returnMsg(False, '没有安装Mysql主从插件，无法启用监控')
            else:
                mysql = ""

        site = {
            'url_list':url_list,
            'key':key,
            'site_name':site_name,
            'adv':adv
        }
        conf_data = self.__read_config(self.__confPath)
        conf_data.append({
                                'push_name': push_name,
                                'push_type': push_type,
                                'cpu_alarm_value': cpu_alarm_value,
                                'cpu_check_time': cpu_check_time,
                                'disk_alarm_value': disk_alarm_value,
                                'mem_alarm_value': mem_alarm_value,
                                'mem_check_time': mem_check_time,
                                'net_alarm_value': net_alarm_value,
                                'net_check_time': net_check_time,
                                'net_bandwidth': net_bandwidth,
                                'time': int(time.time()),
                                'site_check_url': site_check_url,
                                'site_check_word': site_check_word,
                                'open': open,
                                'mysql': mysql,
                                'site': site,
                                'check_type': check_type
        })
        self.__write_config(self.__confPath, conf_data)
        public.WriteLog('消息推送', ' 添加监控[' + push_name + ']')
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
                "open":"检测开关"}
        alter_options = ""
        try:
            push_time = get.push_time
        except:
            get.push_time = 10
        if int(get.push_time) < 10:
            return public.returnMsg(False, '邮件发送间隔时间不能小于10分钟')
        for i in data:
            if i["check_type"] != "mysql":
                i["mysql"] = ""
            if push_name == i["push_name"]:
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
                            # public.writeFile("/tmp/jose.txt", "%s %s\n" % (i[keys[n]],n),"a+")

                            if i[k] != get_data[k]:
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
        if not os.path.exists(path):
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

    # 检测网络用量
    def GetNetWorkIo(self, starttime):
        #取指定时间段的网络Io
        data =  public.M('network').dbfile('system').where("addtime>=? AND addtime<=?",(starttime,time.time())).field('id,up,down').order('id asc').select()
        return data
    # 发送邮件
    def __send_mail(self, url, data):
        if data["email"] == "":
            return False
        return public.httpPost(url,data)

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
        import threading
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
            even = "CPU已经使用[  %.2f  ]超过设定阈值" % cpu_avg
            evenmd5 = "cpumsg" + public.Md5(even)
            now = time.time()
            t = now - float(cache["cpumsg"][1])
            push_time = int(i["push_time"])*60
            if cache["cpumsg"][0] != evenmd5 and t >= push_time:
                cache["cpumsg"][1] = now
                cache["cpumsg"][0] = evenmd5
                public.WriteLog('消息推送', even)
                # 判断告警方式发送消息
                email_data["type"] = "cpu_w"
                email_data["v1"] = " %.2f%s " % (cpu_avg, "%")
                self.cpu_error_code += 1
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "cpu 告警邮件发送成功")
        else:
            if self.cpu_error_code != 0:
                self.cpu_error_code = 0
                cache["cpumsg"][0] = ""
                email_data["type"] = "cpu_s"
                public.WriteLog('消息推送', "cpu 告警状态已经恢复正常")
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "cpu 恢复邮件发送成功")

    def CheckDisk(self,cache,i,email_data,warningUrl,ed):
        hd_data = self.Check_hd_use()
        for keys in hd_data:
            use = int(self.Check_hd_use()[keys])
            c_use = int(i["disk_alarm_value"])
            if use >= c_use:
                disk_data = '  %s  目录已经使用 %.2f%s ' % (keys, float(self.Check_hd_use()[keys]), "%")
                evenmd5 = "diskmsg" + public.Md5(disk_data)
                now = time.time()
                t = now - float(cache["diskmsg"][1])
                push_time = int(i["push_time"]) * 60
                print(use)
                if cache["diskmsg"][0] != evenmd5 and t >= push_time:
                    cache["diskmsg"][0] = evenmd5
                    cache["diskmsg"][1] = now
                    public.WriteLog('消息推送', "磁盘已经使用[  %s  ]超过设定阈值" % disk_data)
                    email_data["type"] = "disk_w"
                    email_data["v1"] = disk_data
                    if self.__send_mail(warningUrl, email_data) == "1":
                        public.WriteLog('消息推送', "磁盘 告警邮件发送成功")
                    self.disk_error_code += 1
                    ed[keys] = self.disk_error_code
                    # 判断告警方式发送消息
            else:
                try:
                    if ed[keys] != 0:
                        ed[keys] = 0
                        cache["diskmsg"][0] = ""
                        email_data["type"] = "disk_s"
                        if self.__send_mail(warningUrl, email_data) == "1":
                            public.WriteLog('消息推送', "磁盘 恢复邮件发送成功")
                        public.WriteLog('消息推送', "磁盘告警状态已经恢复正常")
                except:
                    ed[keys] = 0
    # def CheckNet(self,cache,i,email_data,warningUrl):
    #     starttime = time.time() - int(i["net_check_time"]) * 60
    #     net_data = self.GetNetWorkIo(starttime)
    #     upsum = 0
    #     downsum = 0
    #     for netio in net_data:
    #         upsum += int(netio["up"])
    #         downsum += int(netio["down"])
    #     net_alarm = int(i["net_bandwidth"]) * int(i["net_alarm_value"]) / 100
    #     upavg = upsum / 1024 / len(net_data)
    #     downavg = downsum / 1024 / len(net_data)
    #     if net_alarm <= upavg or net_alarm <= downavg:
    #         d = "上行带宽 %.2fKB 下行带宽 %.2fKB" % (upavg * 1024, downavg * 1024)
    #         even = "带宽已经使用[ %s ]超过设定阈值" % d
    #         evenmd5 = "netmsg" + public.Md5(even)
    #         now = time.time()
    #         t = now - cache["netmsg"][1]
    #         push_time = int(i["push_time"]) * 60
    #         if cache["netmsg"][0] != evenmd5 and t >= push_time:
    #             cache["netmsg"][0] = evenmd5
    #             cache["netmsg"][1] = now
    #             email_data["type"] = "network_w"
    #             email_data["v1"] = d
    #             public.WriteLog('消息推送', even)
    #             self.net_error_code += 1
    #             if self.__send_mail(warningUrl, email_data) == "1":
    #                 public.WriteLog('消息推送', "带宽告警邮件发送成功")
    #             # 判断告警方式发送消息
    #     else:
    #         if self.net_error_code != 0:
    #             self.net_error_code = 0
    #             cache["netmsg"][0] = ""
    #             email_data["type"] = "network_s"
    #             if self.__send_mail(warningUrl, email_data) == "1":
    #                 public.WriteLog('消息推送', "带宽 恢复邮件发送成功")
    #             public.WriteLog('消息推送', "带宽告警状态已经恢复正常")
    def CheckNet(self, cache, i, email_data, warningUrl):
        import psutil
        ct = int(i["net_check_time"])
        nb = int(i["net_bandwidth"])
        nv = int(i["net_alarm_value"])
        push_time = int(i["push_time"])
        cache_t = float(cache["netmsg"][1])
        if "netcard" not in i.keys():
            i["netcard"] = "lo"
        # net_tmp = public.ExecShell("grep '%s' /proc/net/dev|awk '{print $2,$10}'" % i["netcard"])
        net_tmp = psutil.net_io_counters(pernic=True)

        r_tmp = net_tmp[i["netcard"]].bytes_recv
        t_tmp = net_tmp[i["netcard"]].bytes_sent
        # r_list = []
        # t_list = []
        # r_tmp_list = []
        # t_tmp_list = []
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
        print(rsum,tsum)
        net_bandwidth = nb*1024*nv/ 100
        if rsum >= net_bandwidth and tsum >= net_bandwidth:
            d = "上行带宽 %.2fKB 下行带宽 %.2fKB" % (tsum, rsum)
            even = "带宽已经使用[ %s ]超过设定阈值" % d
            evenmd5 = "netmsg" + public.Md5(even)
            now = time.time()
            print(push_time, cache_t)
            t = now - cache_t
            push_time = push_time*60
            print(t,push_time,evenmd5)
            if cache["netmsg"][0] != evenmd5 and t >=push_time:
                cache["netmsg"][0] = evenmd5
                cache["netmsg"][1] = now
                email_data["type"] = "network_w"
                email_data["v1"] = d
                public.WriteLog('消息推送', even)
                self.net_error_code += 1
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "带宽告警邮件发送成功")
                # 判断告警方式发送消息
        else:
            if self.net_error_code != 0:
                self.net_error_code = 0
                cache["netmsg"][0] = ""
                email_data["type"] = "network_s"
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "带宽 恢复邮件发送成功")
                public.WriteLog('消息推送', "带宽告警状态已经恢复正常")


    def CheckMem(self,cache,i,email_data,warningUrl):
        starttime = time.time() - int(i["mem_check_time"]) * 60
        mem_data = self.GetCpuIo(starttime)
        memsum = 0
        for mem in mem_data:
            memsum += int(mem["mem"])
        mem_avg = memsum / len(mem_data)
        if int(i["mem_alarm_value"]) <= mem_avg:
            even = "内存已经使用[  %d%s  ]超过设定阈值" % (mem_avg, "%")
            evenmd5 = "memmsg" + public.Md5(even)
            now = time.time()
            t = now - float(cache["memmsg"][1])
            push_time = int(i["push_time"]) * 60
            if cache["memmsg"][0] != evenmd5 and t >= push_time:
                cache["memmsg"][0] = evenmd5
                cache["memmsg"][1] = now
                email_data["type"] = "mem_w"
                email_data["v1"] = str(mem_avg) + "%"
                public.WriteLog('消息推送', even)
                self.mem_error_code += 1
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "内存 告警邮件发送成功")
                # 判断告警方式发送消息
        else:
            if self.mem_error_code != 0:
                self.mem_error_code = 0
                cache["memmsg"][0] = ""
                email_data["type"] = "mem_s"
                if self.__send_mail(warningUrl, email_data) == "1":
                    public.WriteLog('消息推送', "内存 恢复邮件发送成功")
                public.WriteLog('消息推送', "内存告警状态已经恢复正常")

    def CheckUrl(self,cache,i,email_data,warningUrl):
        site_url = i["site_check_url"]
        self.check_site_health(i)
        for i in self.url_dict.keys():
            if self.url_dict[i] == False:
                even = "URL[  %s  ]监控异常" % site_url
                evenmd5 = "sitemsg" + public.Md5(even)
                now = time.time()
                t = now - float(cache["memmsg"][1])
                push_time = int(i["push_time"]) * 60
                if cache["sitemsg"][0] != evenmd5 and t >= push_time:
                    cache["sitemsg"][0] = evenmd5
                    cache["sitemsg"][1] = now
                    email_data["type"] = "site_w"
                    email_data["v1"] = site_url
                    public.WriteLog('消息推送', even)
                    self.url_error_code += 1
                    # 判断告警方式发送消息
                    if self.__send_mail(warningUrl, email_data) == "1":
                        public.WriteLog('消息推送', "URL 告警邮件发送成功")
            else:
                if self.url_error_code != 0:
                    self.url_error_code = 0
                    cache["sitemsg"][0] = ""
                    public.WriteLog('消息推送', "URL告警状态已经恢复正常 [ %s ]" % site_url)
                    email_data["type"] = "site_s"
                    if self.__send_mail(warningUrl, email_data) == "1":
                        public.WriteLog('消息推送', "URL 恢复邮件发送成功")

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
                even = "站点[  %s  ]监控异常" % s
                evenmd5 = "localsitemsg" + public.Md5(even)
                now = time.time()
                t = now - float(cache["memmsg"][1])
                push_time = int(i["push_time"]) * 60
                if cache["localsitemsg"][0] != evenmd5 and t >= push_time:
                    cache["localsitemsg"][0] = evenmd5
                    cache["localsitemsg"][1] = now
                    email_data["type"] = "site_w"
                    email_data["v1"] = s
                    public.WriteLog('消息推送', even)
                    self.site_error_code += 1
                    # 判断告警方式发送消息
                    if self.__send_mail(warningUrl, email_data) == "1":
                        public.WriteLog('消息推送', "站点 告警邮件发送成功")
            else:
                if self.site_error_code != 0:
                    self.site_error_code = 0
                    cache["localsitemsg"][0] = ""
                    public.WriteLog('消息推送', "站点告警状态已经恢复正常 [ %s ]" % s)
                    email_data["type"] = "site_s"
                    if self.__send_mail(warningUrl, email_data) == "1":
                        public.WriteLog('消息推送', "站点 恢复邮件发送成功")

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
                            email_data["type"] = "db_w"
                            self.mysql_error_code += 1
                            public.WriteLog('消息推送', "Mysql主从异常")
                            if self.__send_mail(warningUrl, email_data) == "1":
                                public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
                    else:
                        if self.mysql_error_code != 0:
                            self.mysql_error_code = 0
                            cache["mysqlmsg"][0] = ""
                            public.WriteLog('消息推送', "Mysql主从异常恢复")
                            email_data["type"] = "db_s"
                            if self.__send_mail(warningUrl, email_data) == "1":
                                public.WriteLog('消息推送', "Mysql主从 恢复邮件发送成功")
                else:
                    if not self.CheckPort(conf["slave_ip"], conf["slave_port"]):
                        even = '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % conf["slave_ip"]
                        evenmd5 = "mysqlmsg" + public.Md5(even)
                        if cache["mysqlmsg"][0] != evenmd5 and t >= push_time:
                            cache["mysqlmsg"][0] = evenmd5
                            cache["mysqlmsg"][1] = now
                            self.mysql_error_code += 1
                            public.WriteLog('消息推送', even)
                            email_data["type"] = "db_w"
                            email_data["v2"] = conf["slave_ip"]
                            if self.__send_mail(warningUrl, email_data) == "1":
                                public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
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
                            email_data["type"] = "db_w"
                        public.WriteLog('消息推送', "Mysql主从异常！！")
                        if self.__send_mail(warningUrl, email_data) == "1":
                            public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
                    else:
                        if self.mysql_error_code != 0:
                            self.mysql_error_code = 0
                            cache["mysqlmsg"][0] = ""
                            public.WriteLog('消息推送', "Mysql主从异常恢复")
                            email_data["type"] = "db_s"
                            if self.__send_mail(warningUrl, email_data) == "1":
                                public.WriteLog('消息推送', "Mysql主从 恢复邮件发送成功")


            except:
                public.WriteLog('消息推送', "error: " + public.get_error_info())

        else:
            if self.mysql_error_code < 1:
                self.mysql_error_code += 1
                public.WriteLog('消息推送', "主从没有配置")

    # 检查开始
    def checkM(self):
        if self.check_monitor():
            ed = {}
            cache = {"cpumsg":["",0],"diskmsg":["",0],"netmsg":["",0],"memmsg":["",0],"sitemsg":["",0],"mysqlmsg":["",0],"localsitemsg":["",0]}
            warningUrl = "http://www.bt.cn/api/index/sendMailMessage"
            while True:
                mail_list = self.get_email_list(None)["emails"]
                mail_list = ",".join(mail_list)
                email_data = {"email": mail_list}
                conf_data = self.__read_config(self.__confPath)
                # check_time = 100
                for i in conf_data:
                    if int(i["open"]) == 1:
                        try:
                            if "push_time" not in i.keys():
                                i["push_time"] = "10"
                            if i["cpu_alarm_value"] != "":
                                self.CheckCPU(cache,i,email_data,warningUrl)
                            # 检查磁盘空间
                            if i["disk_alarm_value"] != "":
                                self.CheckDisk(cache,i,email_data,warningUrl,ed)
                            # 检测带宽
                            if i["net_alarm_value"] != "":
                                self.CheckNet(cache,i,email_data,warningUrl)
                            # 检测内存
                            if i["mem_alarm_value"] != "":
                                self.CheckMem(cache,i,email_data,warningUrl)
                            # 检测URL健康
                            if i["site_check_url"]:
                                self.url_dict = {}
                                self.CheckUrl(cache,i,email_data,warningUrl)
                            # 检测站点
                            if i["site"]["url_list"]:
                                self.site_dict = {}
                                self.CheckLocalSite(cache, i, email_data, warningUrl)
                            # 检查mysql主从健康
                            if i["mysql"] != "":
                                self.CheckMysql(cache,email_data,warningUrl)
                        except:
                            pass
                time.sleep(10)
        else:
            return public.returnMsg(False, '请先打开 面板监控，开启方法菜单-->监控-->开启监控')


if __name__ == '__main__':
    msg_push = msg_push_main()
    msg_push.checkM()



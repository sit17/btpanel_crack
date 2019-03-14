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

    # 启动监控服务
    def StartServer(self, get):
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
        check_int = [[cpu_alarm_value,disk_alarm_value,mem_alarm_value,net_alarm_value],[cpu_check_time,mem_check_time,net_check_time,net_bandwidth]]
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
        return self.__read_config(self.__confPath)

    # 修改事件监控阈值
    def modify_msgpush(self,get):
        push_name = get.push_name
        data = self.__read_config(self.__confPath)
        # keys = ["push_type","cpu_alarm_value","cpu_check_time","mem_alarm_value","mem_check_time","net_alarm_value","net_check_time","net_bandwidth","site_check_url","site_check_word","disk_alarm_value","open"]
        # ps = ["推送类型","CPU阈值","CPU检查周期","内存阈值","内存检查周期","网络阈值","网络检查周期","最大带宽","检查URL","检查关键字","监控磁盘阈值","检测开关"]
        get_data = get.__dict__
        #
        # alter_options = ""
        # for i in data:
        #     if i["check_type"] != "mysql":
        #         i["mysql"] = ""
        #     if push_name == i["push_name"]:
        #         n = 0
        #         for k in keys:
        #             if get_data[k]:
        #                 if "value" in k:
        #                     try:
        #                         a = int(get_data[k])
        #                         if a <= 0 or a > 100:
        #                             return public.returnMsg(False, '阈值不能小于等于0或大于100')
        #                     except:
        #                         return public.returnMsg(False, '请输入整数')
        #                 if "time" in k:
        #                     try:
        #                         a = int(get_data[k])
        #                         if a <= 0:
        #                             return public.returnMsg(False, '不能输入负数或0')
        #                     except:
        #                         return public.returnMsg(False, '请输入整数')
        #                 # public.writeFile("/tmp/jose.txt", "%s %s\n" % (i[keys[n]],n),"a+")
        #                 if i[k] != get_data[k]:
        #                     alter_options += '推送名称 "%s" 的%s "%s" 修改为 "%s"' % (push_name, ps[n], i[k], get_data[k])
        #                     i[k] = get_data[k]
        #                     n+=1
        #                 else:
        #                     n+=1
        #
        #
        #
        #         if alter_options:
        #             public.WriteLog('消息推送', ' 修改配置[' + alter_options + ']')
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
                "open":"检测开关"}
        alter_options = ""
        for i in data:
            if i["check_type"] != "mysql":
                i["mysql"] = ""
            if push_name == i["push_name"]:
                for k in keys.keys():
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
                            elif "open" in k:
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

                if alter_options:
                    public.WriteLog('消息推送', ' 修改配置[' + alter_options + ']')

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
        rep = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
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
        # conf_data = self.__read_config(self.__confPath)
        # for i in conf_data:
        site_check_word = i["site_check_word"]
        site_check_url = i["site_check_url"]
        site_data = requests.get(site_check_url)
        site_data.encoding = 'utf-8'
        if site_check_word in site_data.text:
            return "200"

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


    # 检查开始
    def checkM(self):
        if self.check_monitor():
            disk_error_code = 0
            cpu_error_code = 0
            net_error_code = 0
            mem_error_code = 0
            url_error_code = 0
            mysql_error_code = 0
            ed = {}
            settime = time.time()
            cache = {"cpumsg":"","diskmsg":"","netmsg":"","memmsg":"","stiemsg":"","mysqlmsg":""}
            warningUrl = "http://www.bt.cn/api/index/sendMailMessage"

            while True:
                mail_list = self.get_email_list(None)["emails"]
                mail_list = ",".join(mail_list)
                data = {"email": mail_list}
                conf_data = self.__read_config(self.__confPath)
                # check_time = 100
                for i in conf_data:
                    if int(i["open"]) == 1:
                        try:
                            # 检查cpu负载
                            if i["cpu_alarm_value"] != "":
                                starttime = time.time() - int(i["cpu_check_time"]) * 60
                                cpu_data = self.GetCpuIo(starttime)
                                cpusum = 0
                                for cpuio in cpu_data:
                                    cpusum += int(cpuio["pro"])
                                cpu_avg = cpusum / len(cpu_data)
                                if int(i["cpu_alarm_value"]) <= cpu_avg:
                                    even = "CPU已经使用[  %.2f  ]超过设定阈值" % cpu_avg
                                    evenmd5 = "cpumsg" + public.Md5(even)
                                    if cache["cpumsg"] != evenmd5:
                                    # if cpu_error_code < check_time:
                                        cache["cpumsg"] = evenmd5
                                        public.WriteLog('消息推送', even)
                                        # 判断告警方式发送消息
                                        data["type"] = "cpu_w"
                                        data["v1"] = " %.2f%s " % (cpu_avg,"%")
                                        if self.__send_mail(warningUrl,data) == "1":
                                            public.WriteLog('消息推送', "cpu 告警邮件发送成功")
                                        cpu_error_code += 1

                                else:
                                    if cpu_error_code != 0:
                                        cpu_error_code = 0
                                        cache["cpumsg"] = ""
                                        data["type"] = "cpu_s"
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "cpu 恢复邮件发送成功")
                            # 检查磁盘空间
                            if i["disk_alarm_value"] != "":
                                hd_data = self.Check_hd_use()
                                for keys in hd_data:
                                    use = int(self.Check_hd_use()[keys])
                                    c_use = int(i["disk_alarm_value"])
                                    if use >= c_use:
                                        disk_data = '  %s  目录已经使用 %.2f%s ' % (keys, float(self.Check_hd_use()[keys]), "%")
                                        evenmd5 = "diskmsg" + public.Md5(disk_data)
                                        if cache["diskmsg"] != evenmd5:
                                            # if cpu_error_code < check_time:
                                            cache["diskmsg"] = evenmd5
                                        # if disk_error_code < check_time:
                                            public.WriteLog('消息推送', "磁盘已经使用[  %s  ]超过设定阈值" % disk_data)
                                            data["type"] = "disk_w"
                                            data["v1"] = disk_data
                                            if self.__send_mail(warningUrl, data) == "1":
                                                public.WriteLog('消息推送', "磁盘 告警邮件发送成功")
                                            disk_error_code += 1
                                            ed[keys] = disk_error_code
                                            # 判断告警方式发送消息
                                    else:
                                        try:
                                            if ed[keys] != 0:
                                                ed[keys] = 0
                                                cache["diskmsg"] = ""
                                                data["type"] = "disk_s"
                                                if self.__send_mail(warningUrl, data) == "1":
                                                    public.WriteLog('消息推送', "磁盘 恢复邮件发送成功")
                                                public.WriteLog('消息推送', "磁盘告警状态已经恢复正常")
                                        except:
                                            ed[keys] = 0
                            # 检测带宽
                            if i["net_alarm_value"] != "":
                                starttime = time.time() - int(i["net_check_time"]) * 60
                                net_data = self.GetNetWorkIo(starttime)
                                upsum = 0
                                downsum = 0
                                for netio in net_data:
                                    upsum += int(netio["up"])
                                    downsum += int(netio["down"])
                                net_alarm = int(i["net_bandwidth"]) * int(i["net_alarm_value"]) / 100
                                upavg = upsum / 1024 / len(net_data)
                                downavg = downsum / 1024 / len(net_data)
                                if net_alarm <= upavg or net_alarm <= downavg:
                                    d = "上行带宽 %.2fKB 下行带宽 %.2fKB" % (upavg*1024,downavg*1024)
                                    even = "带宽已经使用[ %s ]超过设定阈值" % d
                                    # if net_error_code < check_time:
                                    evenmd5 = "netmsg" + public.Md5(even)
                                    if cache["netmsg"] != evenmd5:
                                        # if cpu_error_code < check_time:
                                        cache["netmsg"] =  evenmd5
                                        data["type"] = "network_w"
                                        data["v1"] = d
                                        public.WriteLog('消息推送', even)
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "带宽告警邮件发送成功")
                                        # 判断告警方式发送消息
                                        net_error_code+=1
                                else:
                                    if net_error_code != 0:
                                        net_error_code = 0
                                        cache["netmsg"] = ""
                                        data["type"] = "network_s"
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "带宽 恢复邮件发送成功")
                                        public.WriteLog('消息推送', "带宽告警状态已经恢复正常")
                            # 检测内存
                            if i["mem_alarm_value"] != "":

                                starttime = time.time() - int(i["mem_check_time"]) * 60
                                mem_data = self.GetCpuIo(starttime)
                                memsum = 0
                                for mem in mem_data:
                                    memsum += int(mem["mem"])
                                mem_avg = memsum / len(mem_data)
                                if int(i["mem_alarm_value"]) <= mem_avg:
                                    even = "内存已经使用[  %d%s  ]超过设定阈值" % (mem_avg,"%")
                                    # if mem_error_code < check_time:
                                    evenmd5 = "memmsg" + public.Md5(even)
                                    if cache["memmsg"] != evenmd5:
                                        # if cpu_error_code < check_time:
                                        cache["memmsg"] = evenmd5
                                        data["type"] = "mem_w"
                                        data["v1"] = str(mem_avg)+"%"
                                        public.WriteLog('消息推送', even)
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "内存 告警邮件发送成功")
                                        # 判断告警方式发送消息
                                        mem_error_code+=1
                                else:
                                    if mem_error_code != 0:
                                        mem_error_code = 0
                                        cache["memmsg"] = ""
                                        data["type"] = "mem_s"
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "内存 恢复邮件发送成功")
                                        public.WriteLog('消息推送', "内存告警状态已经恢复正常")

                            # 检测站点健康

                            if i["site_check_url"]:
                                site_url = i["site_check_url"]
                                if self.check_site_health(i) != "200":
                                    even = "站点[  %s  ]监控异常" % site_url
                                    # if url_error_code < check_time:
                                    evenmd5 = "sitemsg" + public.Md5(even)
                                    if cache["sitemsg"] != evenmd5:
                                        # if cpu_error_code < check_time:
                                        cache["stiemsg"] = evenmd5
                                        data["type"] = "site_w"
                                        data["v1"] = site_url
                                        public.WriteLog('消息推送', even)
                                        # 判断告警方式发送消息
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "站点 告警邮件发送成功")
                                        url_error_code+=1
                                else:
                                    if url_error_code != 0:
                                        url_error_code = 0
                                        cache["stiemsg"] = ""
                                        public.WriteLog('消息推送', "站点告警状态已经恢复正常 [ %s ]" % site_url)
                                        data["type"] = "site_s"
                                        if self.__send_mail(warningUrl, data) == "1":
                                            public.WriteLog('消息推送', "站点 恢复邮件发送成功")

                            # 检查mysql主从健康
                            if i["mysql"] != "":
                                import panelMysql as pm
                                f = "%s/plugin/masterslave/data.json" % self.setpath
                                conf = public.readFile(f)
                                if os.path.exists(f) and conf != "":
                                    conf = json.loads(conf)
                                    try:
                                        if "master_ip" in conf.keys():
                                            slavestatus = pm.panelMysql().query("show slave status")[0]
                                            Slave_IO_Running = slavestatus[10]
                                            Slave_SQL_Running = slavestatus[11]
                                            if Slave_IO_Running != "Yes" or Slave_SQL_Running != "Yes":
                                                even = "mysql主从异常"
                                                # if mysql_error_code < check_time:
                                                evenmd5 = "mysqlmsg" + public.Md5(even)
                                                if cache["mysqlmsg"] != evenmd5:
                                                    # if cpu_error_code < check_time:
                                                    cache["mysqlmsg"] = evenmd5
                                                    data["type"] = "db_w"
                                                    mysql_error_code += 1
                                                    public.WriteLog('消息推送', "Mysql主从异常")
                                                    if self.__send_mail(warningUrl, data) == "1":
                                                        public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
                                            else:
                                                if mysql_error_code != 0:
                                                    mysql_error_code = 0
                                                    cache["mysqlmsg"] = ""
                                                    public.WriteLog('消息推送', "Mysql主从异常恢复")
                                                    data["type"] = "db_s"
                                                    if self.__send_mail(warningUrl, data) == "1":
                                                        public.WriteLog('消息推送', "Mysql主从 恢复邮件发送成功")
                                        else:
                                            if not self.CheckPort(conf["slave_ip"], conf["slave_port"]):
                                                even = '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % conf["slave_ip"]
                                                evenmd5 = "mysqlmsg" + public.Md5(even)
                                                if cache["mysqlmsg"] != evenmd5:
                                                    # if cpu_error_code < check_time:
                                                    cache["mysqlmsg"] = evenmd5
                                                    mysql_error_code += 1
                                                    public.WriteLog('消息推送', even)
                                                    data["type"] = "db_w"
                                                    data["v2"] = conf["slave_ip"]
                                                    if self.__send_mail(warningUrl, data) == "1":
                                                        public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
                                                    continue
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
                                                if cache["mysqlmsg"] != evenmd5:
                                                    cache["mysqlmsg"] = evenmd5
                                                data["type"] = "db_w"
                                                public.WriteLog('消息推送', "Mysql主从异常！！")
                                                if self.__send_mail(warningUrl, data) == "1":
                                                    public.WriteLog('消息推送', "Mysql主从 告警邮件发送成功")
                                            else:
                                                if mysql_error_code != 0:
                                                    mysql_error_code = 0
                                                    cache["mysqlmsg"] = ""
                                                    public.WriteLog('消息推送', "Mysql主从异常恢复")
                                                    data["type"] = "db_s"
                                                    if self.__send_mail(warningUrl, data) == "1":
                                                        public.WriteLog('消息推送', "Mysql主从 恢复邮件发送成功")


                                    except:
                                        public.WriteLog('消息推送', "error: " + public.get_error_info())

                                else:
                                    if mysql_error_code < 1:
                                        mysql_error_code +=1
                                        public.WriteLog('消息推送', "主从没有配置")


                        except:
                            pass
                time.sleep(60)


if __name__ == '__main__':
    msg_push = msg_push_main()
    msg_push.checkM()


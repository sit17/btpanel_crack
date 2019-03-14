#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2019 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 邹浩文 <627622230@qq.com>
# +-------------------------------------------------------------------

#--------------------------------
# Mysql主从复制
#--------------------------------
import sys
sys.path.append("class/")
import os,public,re,base64,time,json,threading,psutil,socket
os.chdir("/www/server/panel")
import panelMysql as pm

class masterslave_main:
    __mfile = "/etc/my.cnf"
    setpath = "/www/server/panel"
    logfile = "/www/server/panel/plugin/masterslave/setslave.log"
    totalspeedfile = "/www/server/panel/plugin/masterslave/speed.log"
    def GetMasterInfo(self,get):
        master_version = pm.panelMysql().query("select version()")[0][0].split("-")[0]
        master_id = re.search("server-id\s+=\s+(\d+)", public.readFile("/etc/my.cnf")).group(1)
        masterinfo = {
            "slave_user": self.GetRandomString(9),
            "slave_pass": self.GetRandomString(9),
            "btmysql": self.GetRandomString(9),
            "master_port": self.GetMysqlPort(),
            "master_version": str(master_version),
            "master_dbs": self.GetDbs(get),
            "master_id": master_id
        }
        print(masterinfo)
        return masterinfo

    def GetMysqlPort(self):
        try:
            port = pm.panelMysql().query("show global variables like 'port'")[0][1]
        except:
            return False
        if not port:
            return False
        else:
            return int(port)

    def GetDbs(self,get):
        # 判断mysql是否启动
        if not self.GetMysqlPort():
            print('请确定数据库已经开启')
            return public.returnMsg(False, '请确定数据库是否已经开启')
        master_version = pm.panelMysql().query("select version()")[0][0].split("-")[0]
        if "5.1." in master_version:
            return public.returnMsg(False, '本插件不支持5.1版本MYSQL，请安装5.5或以上版本')
        ms = pm.panelMysql().query("show databases")
        dbs = []
        for i in ms:
            if i[0] != "information_schema" and i[0] != "performance_schema" and i[0] != "sys":
                dbs.append(i[0])
        print(dbs)
        return dbs

    def GetLocalIP(self):
        #获取本机ip
        ip = []
        result = psutil.net_if_addrs()
        for k, v in result.items():
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    ip.append((item[1]))
        return ip

    def CheckPort(self,ip,port):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(5)
        try:
            sk.connect((ip, int(port)))
            return True
        except:
            return False

    def SetMaster(self,get):
        if not self.GetPort(get):
            print(self.GetPort(get))
            return public.returnMsg(False, '请确定数据库是否已经开启')
        iprep = "(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})"
        if re.search(iprep, get.slaveip):
            slave_ip = re.search(iprep, get.slaveip).group()
        else:
            print('请输入正确的IP地址')
            return public.returnMsg(False, '请输入正确的IP地址')
        ip = self.GetLocalIP()
        for i in ip:
            if i == slave_ip:
                return public.returnMsg(False, '不能输入本机的IP')
        try:
            slave_port = int(get.slave_port)
            if slave_port >= 65535 or slave_port < 1:
                return public.returnMsg(False, '请输入正确的端口号')
        except:
            return public.returnMsg(False, '请输入正确的端口号')

        if not self.CheckPort(slave_ip,slave_port):
            return public.returnMsg(False, '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % slave_port)
        mconf = public.readFile(self.__mfile)
        masterinfo = self.GetMasterInfo(get)
        masterinfo["replicate_dbs"] = json.loads(get.replicate_dbs)
        dbmsg = []
        if masterinfo["replicate_dbs"][0] == "alldatabases":
            for i in self.GetDbs(get):
                if i != "mysql":
                    d = public.M('databases').where('name=?', ('%s' % i,)).find()
                    dbmsg.append(d)
        else:
            for i in masterinfo["replicate_dbs"]:
                d = public.M('databases').where('name=?', (i,)).find()
                dbmsg.append(d)
        masterinfo["replicate_dbs_info"] = dbmsg
        masterinfo["slave_ip"] = slave_ip
        masterinfo["slave_port"] = slave_port
        addconf = """
log-slave-updates=true
enforce-gtid-consistency=true
gtid-mode=on
        """
        if masterinfo["replicate_dbs"][0] == "alldatabases":
            masterinfo["slave_ips"] = public.M('config').where('id=?', (1,)).getField('mysql_root')
        print(masterinfo["master_version"])
        if "5.5" not in masterinfo["master_version"] and not re.match("10",masterinfo["master_version"]):
            print(masterinfo["master_version"])
            if not re.search("gtid-mode=on", mconf):
                mconf = re.sub("\[mysqld\]","[mysqld]"+ addconf,mconf)
                public.writeFile(self.__mfile,mconf)
                self.WriteLog("重启mysql")
                pid_old = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                self.WriteLog("旧PID %s" % pid_old)
                pid_new = pid_old
                public.writeFile("/tmp/mysqlpid", "")
                for i in range(10):
                    if i == 1:
                        os.system("/etc/init.d/mysqld restart &")
                        time.sleep(10)
                        pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                        self.WriteLog("新PID %s" % pid_new)
                    if pid_old == pid_new:
                        time.sleep(10)
                        pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                    else:
                        public.writeFile("/tmp/mysqlpid", "ok")
                        break
        if re.match("8",masterinfo["master_version"]):
            create_btmysql_sql = "create user btmysql@'%s' identified by '%s'" % (
            masterinfo["slave_ip"], masterinfo["btmysql"])
            grant_btmysql_sql = "grant all on *.* to btmysql@'%s'" % (masterinfo["slave_ip"])
            create_slave_sql = "create user %s@'%s' identified by '%s'" % (
            masterinfo["slave_user"], masterinfo["slave_ip"], masterinfo["slave_pass"])
            grant_slave_sql = "grant replication slave on *.* to %s@'%s'" % (
            masterinfo["slave_user"], masterinfo["slave_ip"])
        else:
            grant_btmysql_sql = ""
            grant_slave_sql = ""
            create_btmysql_sql = "grant all on *.* to btmysql@'%s' identified by '%s'" % (masterinfo["slave_ip"],masterinfo["btmysql"])
            create_slave_sql = "grant replication slave on *.* to %s@'%s' identified by '%s'" % (masterinfo["slave_user"],masterinfo["slave_ip"], masterinfo["slave_pass"])
        flush_sql = "flush privileges"
        pm.panelMysql().execute("delete from mysql.user where host='%s'" % slave_ip)
        for i in [create_btmysql_sql,create_slave_sql,grant_btmysql_sql,grant_slave_sql,flush_sql]:
            pm.panelMysql().execute(i)

        keys = base64.b64encode(json.dumps(masterinfo))
        print(keys)
        public.writeFile("%s/plugin/masterslave/data.json" % self.setpath, json.dumps(masterinfo))
        return keys

    def GetRandomString(self,length):
        from random import Random
        strings = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        chrlen = len(chars) - 1
        random = Random()
        for i in range(length):
            strings += chars[random.randint(0, chrlen)]
        return strings

    def __ExceSql(self,*args, **kwargs):
        try:
            if kwargs:
                ip = kwargs["masterinfo"]["master_ip"]
                port = kwargs["masterinfo"]["master_port"]
                user = "btmysql"
                passwd = kwargs["masterinfo"]["btmysql"]
            else:
                ip = args[0]
                port = args[1]
                user = args[2]
                passwd = args[3]
            sql = args[-1]
            result = public.ExecShell("/usr/bin/mysql -h%s -P%s --connect_timeout=3 -u%s -p%s  -e '%s'" % (ip, port, user, passwd, sql))
        except:
            result = False
        return result

    def WriteLog(self, msg):
        localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if not os.path.exists(self.logfile):
                os.system("touch %s" % self.logfile)
        public.writeFile(self.logfile,localtime+"\n"+msg+"\n","a+")

    def SetTotalSpeed(self,msg):
        if not os.path.exists(self.totalspeedfile):
                os.system("touch %s" % self.totalspeedfile)
        public.writeFile(self.totalspeedfile,json.dumps(msg))
    def GetTotalSpeed(self,get):
        if not os.path.exists(self.totalspeedfile):
            os.system("touch %s" % self.totalspeedfile)
            public.writeFile(self.totalspeedfile,json.dumps({"total":"1"}))
        s = public.readFile(self.totalspeedfile)
        return json.loads(s)

####从库操作
    # 取进度
    def GetSpeed(self,get):
        return public.getSpeed()
    # 设置进度
    def SetSpeed(self):
        data = public.getSpeed()
        bakpath = "/www/backup/database/masterslave.sql"
        if data["title"] == "导入数据库":
            self.SetTotalSpeed({"total": "80"})
            conffile = "%s/plugin/masterslave/data.json" % self.setpath
            masterinfo = json.loads(public.readFile(conffile))
            public.writeSpeed(data["title"],1,data["total"])
            while True:
                data = public.getSpeed()
                time.sleep(1)
                if public.ExecShell("ps aux|grep 'mysql -uroot -p'|wc -l")[0].split("\n")[0] == "2":
                    public.writeSpeed(data["title"], data["total"], data["total"])
                    break
                if data["used"] < data["total"]:
                    if masterinfo["replicate_dbs"][0] == "alldatabases":
                        used = float(pm.panelMysql().query("select concat(round(sum(data_length/1024/1024),2),'MB') as data from information_schema.tables")[0][0].split("M")[0])
                    else:
                        used = 0
                        try:
                            for i in masterinfo["replicate_dbs"]:
                                used += float(pm.panelMysql().query(
                                    "select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables where table_schema='%s'" % i)[
                                                      0][0].split("M")[0])
                        except:
                            used = data["total"]

                    public.writeSpeed(data["title"],int(used),data["total"])
                else:
                    public.writeSpeed(data["title"], data["total"], data["total"])
                    break
        if data["title"] == "备份数据库":
            self.SetTotalSpeed({"total":"30"})
            while True:
                data = public.getSpeed()
                time.sleep(1)
                if public.ExecShell("ps aux|grep 'mysqldump -h'|wc -l")[0].split("\n")[0] == "2":
                    public.writeSpeed(data["title"], data["total"], data["total"])
                    break
                if data["used"] < data["total"]:
                    # used = int(public.ExecShell("du -sm |awk '{print $1}'" % bakpath)[0].split("M")[0])
                    used = int(public.ExecShell("du -sm %s|awk '{print $1}'" % bakpath)[0].split("\n")[0])
                    if used > data["total"]:
                        used = data["total"]
                    public.writeSpeed(data["title"],int(used),data["total"])
                else:
                    public.writeSpeed(data["title"], data["total"], data["total"])
        if data["title"] == "重启数据库":
            self.SetTotalSpeed({"total": "99"})
            n = 0
            while True:
                data = public.getSpeed()
                time.sleep(1)
                if n == 100:
                    break
                if public.readFile("/tmp/mysqlpid"):
                    public.writeSpeed(data["title"], data["total"], data["total"])
                    self.SetTotalSpeed({"total": "100"})
                    os.system("rm -f /tmp/mysqlpid")
                    break
                n+=1
    #放行Mysql端口
    def GetPort(self,get):
        try:
            import firewalls
            port = self.GetMysqlPort()

            if port:
                get.port = str(port)
            else:
                return False
            get.ps = 'MySQL'
            firewalls.firewalls().AddAcceptPort(get)
            return port
        except:
            return False

    def BackUpMasterDbs(self,get):
        import MySQLdb
        bakpath = "/www/backup/database"
        # 判断输入url是否为ip
        iprep = "(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})"
        if re.search(iprep, get.master_ip):
            master_ip = re.search(iprep, get.master_ip).group()
        else:
            print('请输入正确的IP地址')
            return public.returnMsg(False, '请输入正确的IP地址')
        ip = self.GetLocalIP()
        for i in ip:
            if i == master_ip:
                return public.returnMsg(False, '不能输入本机的IP')
        # 解码
        masterinfo = json.loads(base64.b64decode(get.keys))
        masterinfo["master_ip"] = master_ip
        slave_version = pm.panelMysql().query("select version()")[0][0].split("-")[0]
        masterinfo["slave_version"] = slave_version
        # 写入data.json供设置速度使用
        self.WriteLog(json.dumps(masterinfo))
        public.writeFile("%s/plugin/masterslave/data.json" % self.setpath, json.dumps(masterinfo))
        if not self.CheckPort(master_ip, masterinfo["master_port"]):
            return public.returnMsg(False, '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % masterinfo["slave_port"])
        if slave_version == masterinfo["master_version"]:
            #开始锁表
            try:
                db = MySQLdb.connect(host=masterinfo["master_ip"],port=masterinfo["master_port"], user="btmysql", passwd=masterinfo["btmysql"],
                                     charset="utf8")
                cur = db.cursor()
            except:
                return public.returnMsg(False, '无法连接主服务器，请确定主服务器 IP端口是否正确，安全组是否已经放行Mysql端口')
            print("主库开始锁表")
            self.WriteLog("主库开始锁表")
            cur.execute("flush tables with read lock;")

            # baktime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            print("Set Master to readonly mode")
            # 开始备份
            backsqlpath = "%s/masterslave.sql" % (bakpath)
            backsh = "nohup mysqldump -h%s -P%s -u%s -p%s %s%s 1> %s 2>/dev/null&"
            if masterinfo["replicate_dbs"][0] == "alldatabases":
                print("Starting backup of databases alldatabases")
                self.WriteLog("开始备份数据库")
                # 统计数据库大小
                cur.execute("select concat(round(sum(data_length/1024/1024),2),'MB') as data from information_schema.tables")
                total_db = int(float(cur.fetchall()[0][0].split("M")[0]))
                print(total_db)
                if total_db == 0:
                    total_db = 2
                public.writeSpeed("备份数据库",1,total_db)
                # 开始备份数据库
                try:
                    self.WriteLog("备份数据库 %s" % "alldatabases")
                    error = public.ExecShell(backsh % (masterinfo["master_ip"], masterinfo["master_port"], "btmysql", masterinfo["btmysql"],"--all-databases","",backsqlpath))[1]
                    if "error" in error:
                        return public.returnMsg(False, '数据库备份失败 %s\n错误信息：%s\n ,请检测主库是否有问题' % ("alldatabases", error))
                except:
                    self.WriteLog("备份失败 %s" % "alldatabases")
                    return public.returnMsg(False, '数据库备份失败 %s' % "alldatabases")
                threading.Thread(target=self.SetSpeed()).start()
            else:
                total_db = 1
                replicate_dbs = ""
                cur.execute("use information_schema")
                for d in masterinfo["replicate_dbs"]:
                    replicate_dbs += " %s " % d
                # 统计数据库大小
                    cur.execute("select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables where table_schema='%s'" % d)
                    a = cur.fetchall()[0][0]
                    if a:
                        total_db += float(a.split("M")[0])
                        print(total_db)
                public.writeSpeed("备份数据库", 1, int(total_db))
                print("Starting backup of databases %s" % replicate_dbs)
                # 开始备份数据库
                try:
                    self.WriteLog("备份数据库 %s" % replicate_dbs)
                    error = public.ExecShell(backsh % (
                        masterinfo["master_ip"], masterinfo["master_port"], "btmysql", masterinfo["btmysql"], "--databases",
                        replicate_dbs, backsqlpath))[1]
                    if "error" in error:
                        return public.returnMsg(False, '数据库备份失败 %s\n错误信息：%s\n ,请检测主库是否有问题' % ("replicate_dbs", error))
                except:
                    self.WriteLog("备份失败 %s" % replicate_dbs)
                    return public.returnMsg(False, '数据库备份失败 %s' % replicate_dbs)
                threading.Thread(target=self.SetSpeed()).start()
                self.WriteLog("备份成功")

            masterloginfo = self.__ExceSql("show master status",masterinfo=masterinfo)[0].split("\n")[1].split("\t")
            logfile = masterloginfo[0]
            logpos = masterloginfo[1]
            try:
                gtid = self.__ExceSql('SELECT BINLOG_GTID_POS("%s", %s)' % (logfile,logpos),masterinfo=masterinfo)[0].split("\n")[1]
            except:
                gtid = ""
            print("主库解锁表")
            self.WriteLog("主库解锁表")
            cur.execute("unlock tables;")
            db.close()
            public.writeFile("%s/log.txt" % bakpath,str([logfile,logpos]))
            masterinfo["logfile"] = logfile
            masterinfo["logpos"] = logpos
            masterinfo["gtid"] = gtid
            masterinfo["backsqlpath"] = backsqlpath
            public.writeFile("%s/plugin/masterslave/data.json" % self.setpath, json.dumps(masterinfo))
            public.writeFile("/tmp/mysql.log", masterinfo, "a+")
            return masterinfo
        else:
            self.WriteLog("mysql版本不一致")
            return public.returnMsg(False, 'mysql版本不一致')


    def SetSlave(self,get):
        if not self.GetPort(get):
            return public.returnMsg(False, '请确定数据库是否已经开启')
        sconf = public.readFile(self.__mfile)
        # 备份需要同步的数据库
        masterinfo = self.BackUpMasterDbs(get)
        try:
            bkstatus = masterinfo["msg"]
        except:
            bkstatus = False
        if bkstatus:
            return bkstatus
        __dbpass = public.M('config').where('id=?', (1,)).getField('mysql_root')

        slave_version = masterinfo["slave_version"]
        create_replicate_sql = ""
        # Mysql5.5版本
        if "5.5" in slave_version:
            create_replicate_sql += "CHANGE MASTER TO MASTER_HOST='%s',MASTER_PORT=%s,MASTER_USER='%s',MASTER_PASSWORD='%s',MASTER_LOG_FILE='%s',MASTER_LOG_POS=%s" % (
                masterinfo["master_ip"], masterinfo["master_port"], masterinfo["slave_user"],
                masterinfo["slave_pass"],
                masterinfo["logfile"], masterinfo["logpos"])

        # Mysql5.6+版本
        addconf = """
log-slave-updates=true
enforce-gtid-consistency=true
gtid-mode=on"""
        if "5.5" not in slave_version and not re.match("10", slave_version):
            if not re.search("gtid-mode=on",sconf):
                sconf = re.sub("\[mysqld\]", "[mysqld]" + addconf, sconf)
            create_replicate_sql += "CHANGE MASTER TO MASTER_HOST='%s',MASTER_PORT=%s,MASTER_USER='%s',MASTER_PASSWORD='%s',MASTER_AUTO_POSITION = 1" % (
                masterinfo["master_ip"], masterinfo["master_port"], masterinfo["slave_user"],
                masterinfo["slave_pass"])

        # 构造要同步的数据库配置
        replicate_dbs = ""
        if masterinfo["replicate_dbs"][0] != "alldatabases":
            for d in masterinfo["replicate_dbs"]:
                replicate_dbs += "\nreplicate-wild-do-table = %s.%s" % (d, "%")
        else:
            sconf = re.sub("replicate-wild-do-table\s+=\s+[\w\%\.\_\-]+","",sconf)
        print(replicate_dbs)
        serverid = int(masterinfo["master_id"])+1
        if not re.search("replicate-wild-do-table",sconf):
            sconf = re.sub("server-id\s+=\s+\d+", "server-id = %s%s" % (serverid,replicate_dbs), sconf)
        public.writeFile(self.__mfile, sconf)

        # 导入主库数据库
        try:
            pid_old = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
            self.WriteLog("旧PID %s" % pid_old)
            pid_new = pid_old
            public.writeFile("/tmp/mysqlpid", "")
            for i in range(10):
                if i == 1:
                    os.system("/etc/init.d/mysqld restart &")
                    time.sleep(10)
                    pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                    self.WriteLog("新PID %s" % pid_new)
                if pid_old == pid_new:
                    time.sleep(10)
                    pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                else:
                    public.writeFile("/tmp/mysqlpid", "ok")
                    break
            pm.panelMysql().execute("stop slave")
            pm.panelMysql().execute("reset master")
            pm.panelMysql().execute("reset slave all")
            self.WriteLog("开始导入数据库")
            speed = public.getSpeed()
            public.writeSpeed("导入数据库", 1, speed["total"])
            error = public.ExecShell("nohup /usr/bin/mysql -uroot -p%s < %s &" % (__dbpass, masterinfo["backsqlpath"]))
            self.WriteLog(str(error))
            # for i in error:
            #     if "error" in str.lower(str(i)):
            #         return public.ReturnMsg(False, "导入失败")
        except Exception as e:
            self.WriteLog("导入数据库失败  %s" % e)
            return public.ReturnMsg(False, "导入失败")
        threading.Thread(target=self.SetSpeed()).start()
        self.WriteLog("导入数据库完成")

        self.WriteLog("删除备份的数据库文件")
        os.system("rm -f %s" % masterinfo["backsqlpath"])
        os.system("rm -f /tmp/mysqlpid")
        self.WriteLog("重启mysql")
        pid_old = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
        self.WriteLog("旧PID %s" % pid_old)
        pid_new = ""
        public.writeFile("/tmp/mysqlpid", "")

        for i in range(10):
            if i == 1:
                os.system("/etc/init.d/mysqld restart &")
                time.sleep(10)
                pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
                self.WriteLog("新PID %s" % pid_new)
            if pid_old == pid_new:
                time.sleep(10)
                pid_new = public.ExecShell("ps aux|grep 'mysql.sock'|awk 'NR==1 {print $2}'")[0].split("\n")[0]
            else:
                public.writeFile("/tmp/mysqlpid","ok")
                break
        public.writeSpeed("重启数据库", int(1), int(2))
        threading.Thread(target=self.SetSpeed()).start()
        self.WriteLog("mysql重启完成")

        # 写入同步的数据库到面板数据库
        for i in masterinfo["replicate_dbs_info"]:
            public.M('databases').add(("name,username,password,accept,ps"), (i[2], i[3], i[4], i[5], i[6]))
        # 完整复制将主root密码写入到从的面板
        if masterinfo["replicate_dbs"][0] ==  "alldatabases":
            self.WriteLog("因为是完整同步，修改从库面板密码为主库")
            public.M('config').where('id=?', (1,)).setField('mysql_root', masterinfo["slave_ips"])
            result = str(pm.panelMysql().query("select version()")[0])
            self.WriteLog(result)
            if result == "1045":
                public.M('config').where('id=?', (1,)).setField('mysql_root', __dbpass)
        # Mairadb10.*版本
        if re.match("10",slave_version):
            set_slave_pos_sql = "SET GLOBAL gtid_slave_pos='%s'" % masterinfo["gtid"]
            # 需要在数据重启后配置
            pm.panelMysql().query(set_slave_pos_sql)
            create_replicate_sql += "CHANGE MASTER TO MASTER_HOST='%s',MASTER_PORT=%s,MASTER_USER='%s',MASTER_PASSWORD='%s',master_use_gtid=slave_pos" % (
                masterinfo["master_ip"], masterinfo["master_port"], masterinfo["slave_user"], masterinfo["slave_pass"])
        self.WriteLog("停止从服务")
        pm.panelMysql().query("stop slave")
        self.WriteLog("修改从服务器的主服务器信息")
        pm.panelMysql().query(create_replicate_sql)
        self.WriteLog("启动从服务")
        pm.panelMysql().query("start slave")

        time.sleep(2)
        self.WriteLog("获取从状态")
        slavestatus = pm.panelMysql().query("show slave status")[0]
        self.WriteLog(str(slavestatus))

        self.WriteLog("创建Slave监控用户")
        create_status_user = "create user %s@%s identified by '%s'" % ("user"+masterinfo["slave_user"], masterinfo["master_ip"], "pass"+masterinfo["slave_pass"])
        grant_status_user = "grant super,select,delete on *.* to %s@'%s'" % ("user"+masterinfo["slave_user"], masterinfo["master_ip"])
        pm.panelMysql().execute(create_status_user)
        pm.panelMysql().execute(grant_status_user)

        n = 0
        for i in slavestatus:
            if i == "Yes":
                n += 1
        if n == 2:
            print("设置成功")
            self.WriteLog("删除btmysql用户")
            self.__ExceSql('delete from mysql.user where user="btmysql"', masterinfo=masterinfo)
            if masterinfo["replicate_dbs"][0] != "alldatabases":
                self.WriteLog("删除从btmysql用户")
                pm.panelMysql().execute("delete from mysql.user where user='btmysql'")
            self.WriteLog("设置成功")
            os.system("rm -f %s" % self.totalspeedfile)
            return public.returnMsg(True, '设置成功')
        else:
            self.WriteLog("设置失败")
            os.system("rm -f %s" % self.totalspeedfile)
            return public.returnMsg(True, '设置失败')

    def RemoveReplicate(self,get):
        f = "%s/plugin/masterslave/data.json" % self.setpath
        conf = public.readFile(f)
        if os.path.exists(f) and conf != "":
            conf = json.loads(conf)
            try:
                master_ip = conf["master_ip"]
            except:
                master_ip = ""
            if master_ip:
                pm.panelMysql().execute("stop slave")
                pm.panelMysql().execute("reset slave all")
                pm.panelMysql().execute("reset master")
            os.system("rm -f %s/plugin/masterslave/data.json" % self.setpath)
            self.WriteLog("删除成功")
            return public.returnMsg(True, "删除成功")

    # 获取主从状态
    def GetReplicateStatus(self,get):
        f = "%s/plugin/masterslave/data.json" % self.setpath
        conf = public.readFile(f)
        if os.path.exists(f) and conf != "":
            conf = json.loads(conf)
            try:
                if "master_ip" in conf.keys():
                    slavestatus = pm.panelMysql().query("show slave status")[0]
                    Slave_IO_Running = slavestatus[10]
                    Slave_SQL_Running = slavestatus[11]
                    master_ip = conf["master_ip"]
                    slave_ip = "local"
                else:
                    if not self.CheckPort(conf["slave_ip"], conf["slave_port"]):
                        return public.returnMsg(False, '无法访问从服务器<br>请确认安全组是否已经放行<br>Mysql端口：%s' % conf["slave_ip"])
                    slavestatus = public.ExecShell(
                        "mysql -h%s -P%s --connect_timeout=3 -u%s -p%s -e 'show slave status\G'" % (conf["slave_ip"],conf["slave_port"],"user"+conf["slave_user"],"pass"+conf["slave_pass"]))[0]
                    if not slavestatus:
                        return public.returnMsg(True, "获取成功")
                    Slave_IO_Running = "Slave_IO_Running:\s+(\w+)"
                    Slave_SQL_Running = "Slave_SQL_Running:\s+(\w+)"
                    Slave_IO_Running = re.search(Slave_IO_Running, slavestatus).group(1)
                    Slave_SQL_Running = re.search(Slave_SQL_Running, slavestatus).group(1)
                    master_ip = "local"
                    slave_ip = conf["slave_ip"]
            except:
                return public.returnMsg(True, "获取成功")

        else:
            return public.returnMsg(True, "获取成功")
        status = {
            "Slave_IO_Running": Slave_IO_Running,
            "Slave_SQL_Running": Slave_SQL_Running,
            "master_ip": master_ip,
            "slave_ip": slave_ip,
            "slavestatus": slavestatus,
            "replicate_dbs": conf["replicate_dbs"]
        }
        return public.returnMsg(True, status)

    def CheckTables(self):
        __dbpass = public.M('config').where('id=?', (1,)).getField('mysql_root')
        file = "%s/plugin/masterslave/data.json" % self.setpath
        conf = json.loads(public.readFile(file))
        host = "localhost"
        user = "root"
        passwd = __dbpass
        a = public.ExecShell("/www/server/mysql/bin/mysqlcheck -h%s aaa_com -u%s -p%s" % (host, user, passwd))[
            0].split("OK")
        host = conf["slave_ip"]
        user = "user"+conf["slave_user"]
        passwd = "pass"+conf["slave_pass"]
        b = public.ExecShell("/www/server/mysql/bin/mysqlcheck -h%s aaa_com -u%s -p%s" % (host, user, passwd))[
            0].split("OK")
        errortable = []
        for l in [a, b]:
            for i in l:
                if "error" in i:
                    errortable.append(i)
        print(errortable)
        if errortable:
            return public.returnMsg(False, "以下表 %s 已损坏，请修复后再重新做同步" % errortable)

    # 检测主从错误
    def GetReplicateError(self,get):
        f = "%s/plugin/masterslave/data.json" % self.setpath
        conf = json.loads(public.readFile(f))
        status = self.GetReplicateStatus(get)["msg"]
        if status["master_ip"] == "local":
            status = status
            if status["Slave_IO_Running"] != "Yes" or status["Slave_SQL_Running"] != "Yes":
                errortable = self.CheckTables()
                if errortable:
                    return errortable
                if self.CheckPort(conf["slave_ip"], conf["slave_port"]):
                    last_io_errno = re.search("Last_IO_Errno:\s+(\d+)", status["slavestatus"]).group(1)
                    if last_io_errno == "1236":
                        errormsg = re.search("Last_IO_Error:\s+(.+)", status["slavestatus"]).group(1)
                        if "Could not find first log file name in binary log index file" in errormsg:
                            print('<br><a style="color:red;">主服务器二进制文件丢失，请重做主从，以免丢失数据</a>')
                            return public.returnMsg(False, "主服务器异常重启导致主库有数据回滚，若有数据丢失请到从库查找，若要重做主从请先备份好主库和从库以免丢失数据")
                        if "Slave has more GTIDs than the master has" in errormsg:
                            print("主服务器二进制文件丢失，请重做主从，以免丢失数据")
                            return public.returnMsg(False, "主服务器异常重启导致主库有数据回滚，若有数据丢失请到从库查找，若要重做主从请先备份好主库和从库以免丢失数据")
                        if "Error: connecting slave requested to start from GTID" in errormsg:
                            return public.returnMsg(False, "主服务器异常重启导致主库有数据回滚，若有数据丢失请到从库查找，若要重做主从请先备份好主库和从库以免丢失数据")
                        return public.returnMsg(True, "读取二进制日志时报错，主要出现在服务器有异常重启的情况，是否尝试修复")
                    # 主键冲突处理
                    last_sql_errno = re.search("Last_SQL_Errno:\s+(\d+)", status["slavestatus"]).group(1)
                    if last_sql_errno == "1062":
                        # return {"fix": 1, "content": "从库已经存在插入的数据，修复会先删除从库冲突的数据，在插入主库数据，是否尝试修复"}
                        return public.returnMsg(True, "从库已经存在插入的数据，修复会先删除从库冲突的数据，在插入主库数据，是否尝试修复"+'<br><a style="color:red;">！！！如果需要修复请先备份好从库以免使数据丢失！！！</a>')

                else:
                    return public.returnMsg(False, "无法连接到从服务器")
            else:
                print("同步正常无需修复")
                return public.returnMsg(False, "同步正常无需修复")
        else:
            return public.returnMsg(False, "请到主服务器执行")
        # if get.fix == "1":
        #     pass
    # 修复主从
    def FixReplicate(self,get):
        file = "%s/plugin/masterslave/data.json" % self.setpath
        conf = json.loads(public.readFile(file))
        status = self.GetReplicateStatus(get)
        if status:
            status = status["msg"]
            if status["Slave_IO_Running"] != "Yes" or status["Slave_SQL_Running"] != "Yes":
                mversion = pm.panelMysql().query("select version()")[0][0].split("-")[0]
                Last_IO_Errno = re.search("Last_IO_Errno:\s+(\d+)", status["slavestatus"]).group(1)
                if Last_IO_Errno == "1236":
                    if "5.5" in mversion:
                        errormsg = re.search("Last_IO_Error:\s+(.+)",status["slavestatus"]).group(1)
                        rep = "(mysql-bin\.\d+)\'\s\w{2}\s(\d+)"
                        errormsg = re.search(rep, errormsg)
                        errmysqlbin = errormsg.group(1)
                        errlogpos = errormsg.group(2)
                        os.system(
                            "/www/server/mysql/bin/mysqlbinlog /www/server/data/%s|grep 'end_log_pos' > /www/server/data/btfix.log" % errmysqlbin)
                        mpos = public.ExecShell("tail -n 1 /www/server/data/btfix.log|awk '{print $7}'")[0].split("\n")[0]
                        print(mpos)
                        if int(mpos) < int(errlogpos):
                            change_sql='stop slave;change master to  MASTER_LOG_FILE="%s",MASTER_LOG_POS=%s;start slave' % (errmysqlbin,mpos)
                            print(change_sql)
                            print(self.__ExceSql(conf["slave_ip"], conf["slave_port"], "user" + conf["slave_user"],
                                           "pass" + conf["slave_pass"], change_sql))
                            status = self.GetReplicateStatus(get)
                            status = status["msg"]
                            if status["Slave_IO_Running"] == "Yes" and status["Slave_SQL_Running"] == "Yes":
                                os.system("rm -f /www/server/data/btfix.log")
                                print("修复成功")
                                return public.returnMsg(True, "修复成功")
                            else:
                                print("修复失败")
                                return public.returnMsg(True, "修复失败")

                # 主键冲突处理
                last_sql_errno = re.search("Last_SQL_Errno:\s+(\d+)", status["slavestatus"]).group(1)
                if last_sql_errno == "1062":
                    while True:
                        errormsg = re.search("Last_SQL_Error:\s+(.*)", status["slavestatus"]).group(1)
                        primary = "entry\s'(\w+)'"
                        defdb = "database:\s'(\w*)'"
                        db_tb = "insert\s+into\s+([\w\_\-\.]+)\s+\("
                        primary = re.search(primary, errormsg).group(1)
                        try:
                            defdb = re.search(defdb, errormsg).group(1)
                        except:
                            defdb = ""
                        db_tb = re.search(db_tb, errormsg).group(1)
                        print(primary, defdb, db_tb)
                        if not defdb:
                            sql = "desc %s" % db_tb
                            result = pm.panelMysql().query(sql)
                            for i in result:
                                if "PRI" in i:
                                    prikey = i[0]
                            sql = 'delete from %s where %s=%s;stop slave;start slave;' % (db_tb, prikey, primary)
                            print(sql)
                            a = self.__ExceSql(conf["slave_ip"], conf["slave_port"], "user" + conf["slave_user"],
                                           "pass" + conf["slave_pass"], sql)
                            print(a)
                            status = self.GetReplicateStatus(get)["msg"]
                            print(status)
                            last_sql_errno = re.search("Last_SQL_Errno:\s+(\d+)", status["slavestatus"]).group(1)
                            if last_sql_errno != "1062":
                                return public.returnMsg(True, "修复成功")
                else:
                    return public.returnMsg(False, "无法修复")


            else:
                print("同步正常无需修复")
                return public.returnMsg(True, "同步正常无需修复")
        else:
            return public.returnMsg(False, "获取主从状态失败")

    # 同步异常提醒
    def MonitorMysql(self,get):
        if self.GetReplicateStatus(get):
            pass
        else:
            pass

#
# class get:
#     pass
# get.slaveip = "192.168.1.199"
# get.master_ip = "192.168.1.198"
# get.slave_port = "3306"
# get.replicate_dbs = ["jose"]
# get.replicate_dbs = "[\"alldatabases\"]"
# get.keys = "eyJtYXN0ZXJfZGJzIjogWyJhYWFfY29tIiwgImJiYl9jb20iLCAibWF5aWRheGlhbmciLCAibXlzcWwiXSwgInNsYXZlX3Bhc3MiOiAiWE5KYUJoQkRRIiwgInNsYXZlX3VzZXIiOiAiOXRnRjlEMHFZIiwgIm1hc3Rlcl92ZXJzaW9uIjogIjUuNS41NyIsICJzbGF2ZV9pcCI6ICIxOTIuMTY4LjEuMTk5IiwgIm1hc3Rlcl9wb3J0IjogIjMzMDYiLCAic2xhdmVfcG9ydCI6IDMzMDYsICJidG15c3FsIjogIldHNnhJeWk0eiIsICJyZXBsaWNhdGVfZGJzIjogWyJhbGxkYXRhYmFzZXMiXSwgInNsYXZlX2lwcyI6ICIxODA3MzRkNTA1MjNiYWYzIn0="
# a = masterslave_main()
# a.SetMaster(get)
# a.GetMasterInfo(get)
# # a.BackUpMasterDbs(get)
# # a.SetSlave(get)
# a.GetReplicateStatus(get)
# a.FixReplicate(get)
# a.GetReplicateError(get)
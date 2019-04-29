#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
install_tmp='/tmp/bt_install.pl'
public_file=/www/server/panel/install/public.sh

if [ ! -f $public_file ];then
	wget -O $public_file http://download.bt.cn/install/public.sh -T 5;
fi

. $public_file
download_Url=$NODE_URL
pluginPath=/www/server/panel/plugin/msg_push

Install_MsgPush()
{
    id=`ps aux|grep "/www/server/panel/plugin/msg_push"|grep -v "grep"|awk '{print $2}'`
    if [ "$id" ];then
	    kill -9 $id
	fi
    rm -f $pluginPath/msg_push_main.py
	mkdir -p $pluginPath
	/usr/bin/pip install requests prettytable
	echo '正在安装脚本文件...' > $install_tmp
	wget -O $pluginPath/msg_push_main.py $download_Url/install/plugin/msg_push/msg_push_main.py -T 5
	wget -O $pluginPath/index.html $download_Url/install/plugin/msg_push/index.html -T 5
	wget -O $pluginPath/info.json $download_Url/install/plugin/msg_push/info.json -T 5
	wget -O $pluginPath/icon.png $download_Url/install/plugin/msg_push/icon.png -T 5
	if [ ! -f "$pluginPath/config.json" ];then
	    wget -O $pluginPath/config.json $download_Url/install/plugin/msg_push/config.json -T 5
	fi
	wget -O $pluginPath/install.sh $download_Url/install/plugin/msg_push/install.sh -T 5
	\cp -a -r /www/server/panel/plugin/msg_push/icon.png /www/server/panel/static/img/soft_ico/ico-msg_push.png
	sed -i '/* * * * * \/bin\/sh \/www\/server\/panel\/plugin\/msg_push\/daemon.sh/d' /var/spool/cron/root
	nohup /usr/bin/python /www/server/panel/plugin/msg_push/msg_push_main.py &
	/usr/bin/echo '1' > /www/server/panel/plugin/msg_push/open.txt

	echo '安装完成' > $install_tmp
}

Uninstall_MsgPush()
{
	rm -rf $pluginPath
	id=`ps aux|grep msg_push|grep -v "grep"|awk '{print $2}'`
	kill -9 $id
	/usr/bin/systemctl restart crond
}

if [ "${1}" == 'install' ];then
	Install_MsgPush
elif  [ "${1}" == 'update' ];then
	Install_MsgPush
elif [ "${1}" == 'uninstall' ];then
	Uninstall_MsgPush
fi

#!/bin/sh
basedir="/www/server/panel/plugin/msg_push"
if [ -f "$basedir/open.txt" ];then
    open=`/usr/bin/cat $basedir/open.txt`
else
    echo '0' > $basedir/open.txt
    open=`/usr/bin/cat $basedir/open.txt`
fi
if [ "$open" -eq "1" ];then
    r=`ps aux|grep msg_push|grep -v "grep"|wc -l`
    if [ "$r" -lt "3" ];then
        nohup /usr/bin/python $basedir/msg_push_main.py &
    fi
fi
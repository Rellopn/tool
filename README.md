# redis install cluster sentinel tool in centOs<br>
**need python 2.7+**<br/>
enter 'python redisInstall.py -h'<br/>
you will see
    &nbsp;&nbsp;&nbsp;&nbsp;-h print help message.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;-n set the amount of cluster salve. <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;-i (waring:must set -n with -i)start redis cluster by args, ip and port include cmd args.e.g: `python redisInstall.py -i 192.168.1.1:7001,192.168.1.1:7002,192.168.1.1:7003 -n 1`<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;-o only install redis.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;-c start cluster redis instance by args's .node number must >= 6.e.g:`python redisInstall.py -c 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003`<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;-s start single redis instance by args's .e.g:`python redisInstall.py -s 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003`<br/>

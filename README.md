
# Redis的安装脚本--有集群功能
-------------
需要：pythin2.7
## 运行方法：
脚本放在`root`目录下，键入`python redisInstall.py -o`
### 参数说明：
- `-o` 仅安装redis。
- `-s` 运行redis。安装并运行redis的命令可以写成：`python redisInstall.py -o -s`。
- `-c` 配置redis集群文件。如:`python redisInstall.py -c 192.168.1.11:8000,192.168.1.11:8001,192.168.1.11:8002,192.168.1.11:8003,192.168.1.11:8004,192.168.1.11:8005`,即配置端口在其中的redis文件。
- `-i` 开启配置的redis集群实例。**注意，必须带有参数`-n`**。如:`python redisInstall.py -c 192.168.1.11:8000,192.168.1.11:8001,192.168.1.11:8002,192.168.1.11:8003,192.168.1.11:8004,192.168.1.11:8005 -n 1`,即运行端口在其中的redis文件。并切给每个redis实例一个从属的实例。如图所示：
<img src='https://github.com/Rellopn/tool/blob/master/img1.png' height='200px' weight='200px'/>
- `-m` 开启redis哨兵。

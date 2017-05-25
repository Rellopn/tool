# coding=utf-8
import os
import requests
import re
import sys, getopt

# python 脚本的工作目录
workPath = os.getcwd()
# singleConfig 的通用配置
singleConfigStr = '''
protected-mode no
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
cluster-enabled no

slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
'''
# clusterConfig 的通用设置
clusterConfigStr = '''
protected-mode no
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
cluster-enabled yes

slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
'''


# 帮助信息
def usage():
    usage = '''
    -h help print help message.
    -n set the amount of cluster salve. 
    -i (waring:must set -n with -i)start redis cluster by args, ip and port include cmd args.e.g: python redisInstall.py -i 192.168.1.1:7001,192.168.1.1:7002,192.168.1.1:7003
    -o only install redis.
    -c start cluster redis instance by args's number.node number must >= 6.e.g:python redisInstall.py -c 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003
    -s start single redis instance by args's number.e.g:python redisInstall.py -s 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003
    '''
    return usage


# 获取命令行参数 -i -h，形如：python redisInstall.py -i 192.168.1.1:7001,192.168.1.1:7002,192.168.1.1:7003
# 参数处理逻辑 ：
# 1.如果有-h参数，打印帮助信息，退出程序。
# 2.如果有-i参数，其它参数都可以有。
# 3.如果有-o参数，则其它参数都可以有。
# 4.如果有-s参数，其它都可以有。
# 5 .如果有-t参数，其它都可以有。
def getCmdArgs():
    argsDic = {}
    opts, args = getopt.getopt(sys.argv[1:], "hos:c:i:m:n:")
    # "h:i:"指明本程序只接受-h -i的参数
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以只取sys.argv[1:]部分，过滤掉脚本名

    for op, value in opts:
        if op == "-i":
            print "-i values is:" + value  # 此处的value就是-i的值
            argsDic["i"] = value
        if op == "-h":
            print usage()
            sys.exit(0)
        if op == "-o":
            argsDic["o"] = value
        if op == "-c":
            argsDic["c"] = value
        if op == "-s":
            argsDic["s"] = value
        if op == "-m":
            argsDic['m'] = value
        if op== "-n":
            argsDicDic["n"]=value
    return argsDic


# 检查指定目录下是否存在包含名称的文件夹或者文件.存在返回False,不存在返回True
def checkDirExist(checkName, dir):
    dirExist = os.listdir(dir)
    for i in dirExist:
        if (checkName in i):
            return False
    return True


# http://download.redis.io/releases/redis-3.2.8.tar.gz
# 安装redis
def installRedis():
    os.system(
        "yum install gcc gcc-c++ kernel-devel automake autoconf libtool make wget tcl vim ruby rubygems unzip git -y")
    # 安装到工作目录下
    if (checkDirExist("redis_source", workPath)):
        os.system("mkdir redis_source")
    os.chdir("redis_source")
    os.system("wget http://download.redis.io/releases/redis-3.2.8.tar.gz")
    os.system("tar -zxvf redis-3.2.8.tar.gz")
    os.chdir("redis-3.2.8")
    os.system("make")
    os.chdir("src")
    os.system("make install PREFIX=/usr/local/redis")
    # 把启动的配置文件和集群文件复制到启动目录下
    os.system("cp /root/redis_source/redis-3.2.8/src/redis-trib.rb /usr/local/redis/bin")
    os.system("cp /root/redis_source/redis-3.2.8/redis.conf /usr/local/redis/bin/")
    print ("redis3.2.8 has installed")


# 启动redis
def runRedis():
    os.chdir("/usr/local/redis/bin/")
    os.system("./redis-server redis.conf")
    print ("redis3.2.8 is runing")


class redisCluster():
    configList = []

    # 获得ip和port的list[list[ip,port]].
    def getIpAndPorts(self):
        # 要返回的list
        ipAndPorts = {}
        # 找命令行参数i，如果没有就结束运行并提示
        argDic = getCmdArgs()
        print "argDic:" + str(argDic)
        argI = argDic.get("i", "not found")
        argC = argDic.get("c", "not found")
        argS = argDic.get("s", "not found")
        print "argI:" + argI
        print "argC:" + argC
        if (argI == "not found" and argC == "not found" and argS == "not found"):
            raise Exception("not found args -i or -c or -s")
        # 解析-i参数,必须大于三个，因为集群最小配置就是三个
        if (argI != "not found"):
            listI = []
            splitList = argI.split(",")
            if (len(splitList) < 6 and argI != "not found"):
                raise Exception("must be greater than or equal to 6")
            for i in range(len(splitList)):
                ipAndPortI = splitList[i].split(":")
                listI.append(ipAndPortI)
            ipAndPorts["i"] = listI
        if (argC != "not found"):
            listC = []
            splitList = argC.split(",")
            for i in range(len(splitList)):
                ipAndPortC = splitList[i].split(":")
                listC.append(ipAndPortC)
                ipAndPorts["c"] = listC
        if (argS != "not found"):
            listS = []
            splitList = argS.split(",")
            for i in range(len(splitList)):
                ipAndPortS = splitList[i].split(":")
                listS.append(ipAndPortS)
                ipAndPorts["s"] = listS
        # 获取ip和port

        print ipAndPorts
        return ipAndPorts

    # 本地redis
    def generateSingleConfig(self):
        nativeDir = os.listdir(workPath)
        ipAndPortsS = self.getIpAndPorts()
        ipAndPorts = ipAndPortsS["s"]
        if "redisNativeConfig" not in nativeDir:
            os.system("mkdir redisNativeConfig")
        os.chdir(workPath + "/redisNativeConfig")
        for i in range(len(ipAndPorts)):
            port = ipAndPorts[i][1]
            str1 = '''port %s
        logfile "''' + workPath + '''/redisNativeConfig/%s.log"
                    ''' % (port, port)
            configStr1 = str1 + singleConfigStr
            # 要生成的文件名
            configName = "redis" + port + ".config"
            # 检查下有没有重名的文件，如果重名，就停止执行。
            redisNativeConfigPwd = os.listdir(workPath + "/redisNativeConfig")
            # 判断是否已经有configName文件，如果没有就继续，如果有了就认为已经安装了
            if configName in redisNativeConfigPwd:
                raise Exception("configName has exist,process will exit!")
            f = open(configName, "w")
            f.write(configStr1)
            f.close()

    # 生成clusterConfig文件
    def generateClusterConfig(self):
        # 获得ip和ports，在这里只取port生成配置文件
        ipAndPortsC = self.getIpAndPorts()
        ipAndPorts = ipAndPortsC["c"]
        # 创建log日志的文件
        if checkDirExist("redis-cluster", workPath):
            os.system("mkdir redis-cluster")
        os.chdir("redis-cluster")
        for i in range(len(ipAndPorts)):
            port = ipAndPorts[i][1]
            str1 = '''port %s
logfile "/root/redis-cluster/%s/%s.log"
cluster-config-file /root/redis-cluster/%s/nodes-%s.conf
            ''' % (port, port, port, port, port)
            configStr1 = str1 + clusterConfigStr
            # 要生成的文件名
            configName = "redis" + port + "-cluster.config"
            # 检查下有没有重名的文件，如果重名，就停止执行。
            rootPwd = os.listdir(workPath)
            # 判断是否已经有configName文件，如果没有就继续，如果有了就认为已经安装了

            for i in rootPwd:
                if (i == configName):
                    raise Exception("configName has exist,process will exit!")
                f = open(configName, "w")
                f.write(configStr1)
                f.close()
            os.system("mkdir " + port)

    # 启动实例。singleOrCluster=1为集群实例启动，singleOrCluster=2为本地实例启动
    def copyAndRun(self, singleOrCluster):
        redisConfDir=workPath+"/redis-cluster"
    	os.chdir(redisConfDir)
        runConfigList = []
        # 计数，计redis启动的实例的数量
        n = 0
        if (singleOrCluster == 1):
            # 把文件名称 做成列表，挨个比较包不包含config字符串。每找到一个configNumber数量加1，表示要启动的redis实例数量。
            listDir = os.listdir(redisConfDir)
            for i in listDir:
                if (i.find("config") != -1):
                    runConfigList.append(redisConfDir+"/"+i)
            for i in runConfigList:
                n += 1
                #os.system("cp -f " + i + " /usr/local/redis/bin/")
                os.chdir("/usr/local/redis/bin")
                os.system("./redis-server " + str(i))
                print("redis instance number：" + str(n) + ".Config file is :" + str(i))
        if (singleOrCluster == 2):
            os.chdir(workPath + "/redisNativeConfig")
            listDir = os.listdir(workPath + "/redisNativeConfig")
            for i in listDir:
                if (i.find("config") != -1):
                    runConfigList.append(i)
            print (runConfigList)
            for i in runConfigList:
                n += 1
                os.system("cp -f " + i + " /usr/local/redis/bin/")
                os.chdir("/usr/local/redis/bin")
                os.system("./redis-server " + str(i))
                print("redis instance number：" + str(n) + ".Config file is :" + str(i))

    # 获得外网ip地址
    def GetOuterIP(self):
        url = "http://www.ip138.com/ip2city.asp"
        r = requests.get(url)
        ip = re.search("\d+\.\d+\.\d+\.\d+", r.text).group(0)
        return ip

    # 执行redis的创建集群命令创建集群
    def exeRedisCluster(self):
        argDic = getCmdArgs()
        salveArg = argDic.get("n", "not found")
        # 如果没有参数，抛出错误
        if salveArg == "not found" or sentinelArg == "":
            raise Exception("not found arg -m")
        # 解决缺少redis和ruby的接口
        # os.system("gem install redis")
        # os.system("y")
        # 开始集群喽
        os.chdir("/usr/local/redis/bin/")
        ipAndPortsI = self.getIpAndPorts()
        ipAndPorts = ipAndPortsI["i"]
        # ...
        redisClusterIpAndPorts = ""
        for i in range(len(ipAndPorts)):
            redisClusterIpAndPorts += ipAndPorts[i][0] + ":" + ipAndPorts[i][1] + " "
        os.system(" ./redis-trib.rb  create --replicas "+salveArg+ " "+ redisClusterIpAndPorts)


def runSentinel():
    argDic = getCmdArgs()
    sentinelArg = argDic.get("m", "not found")
    # 如果没有参数，抛出错误
    if sentinelArg == "not found" or sentinelArg == "":
        raise Exception("not found arg -m")

    splitList = sentinelArg.split(",")
    # 取出要监听的端口port
    if len(splitList[1]) > 5:
        raise Exception("must have monitor port")
    port = splitList[1]
    isinstanceNum = splitList[0]
    del splitList[0]
    del splitList[0]

    sentinelconf = ''
    time = 0
    for i in range(len(splitList)):
        stringTime = str(time)
        ipAndPortS = splitList[i].split(":")
        sentinelconf += '''
sentinel monitor mymaster''' + stringTime + " " + ipAndPortS[0] + " " + ipAndPortS[1] + " " + str(
            (len(splitList) / 2 + 1)) + '''
sentinel down-after-milliseconds mymaster''' + stringTime + ''' 30000
sentinel parallel-syncs mymaster''' + stringTime + ''' 1
sentinel failover-timeout mymaster''' + stringTime + ''' 20000
        '''
        time = time + 1
    sentinelconf = 'port ' + port + sentinelconf
    file = open('sentinel.conf', 'w')
    file.write(sentinelconf)
    file.close()
    os.chdir("./usr/local/redis/bin/")
    for i in isinstanceNum:
        os.system('./redis-sentinel sentinel.conf')
        # os.system('./usr/local/redis/bin/redis-sentinel sentinel.conf')
    os.chdir(workPath)


def run():
    # 获得运行参数字典
    runArgs = getCmdArgs()
    o = runArgs.has_key("o")
    i = runArgs.has_key("i")
    c = runArgs.has_key("c")
    s = runArgs.has_key("s")
    m = runArgs.has_key("m")
    b = redisCluster()
    # 如果有参数o，安装redis
    if (o):
        installRedis()
        # 如果有参数t，启动redis
        if (c):
            b.generateClusterConfig()
            b.copyAndRun(1)
            if (i):
                # 如果有i，启动集群
                b.exeRedisCluster()
        elif (s):
            # 上层判断如果是s，为本机实例启动
            b.generateSingleConfig()
            b.copyAndRun(2)
            if (i):
                # 如果有i，启动集群
                b.exeRedisCluster()
    elif (c):
        # 上层判断如果是c，为集群实例启动
        b.generateClusterConfig()
        print "dierbukaisjinx" 
        b.copyAndRun(1)
        print "dierbuzhixingwanbi,kaisdisanbu" 
        if (i):
            # 如果有i，启动集群
            b.exeRedisCluster()
    elif (s):
        # 上层判断如果是s，为本机实例启动
        b.generateSingleConfig()
        b.copyAndRun(2)
        if (i):
            # 如果有i，启动集群
            b.exeRedisCluster()
    elif (i):
        # 如果有i，启动集群
        b.exeRedisCluster()

    elif (m):
        runSentinel()


if __name__ == '__main__':
    run()

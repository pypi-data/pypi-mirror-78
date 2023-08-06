# 智能助理服务端 
## 开发测试
初始化配置:  
```shell script
python bin/init_app.py
```
交互测试:  
```shell script
python tests/input.py
```

## 应用部署
通过流水线docker容器部署在业务网paas平台
为确保dockerfile文件正常，能正常部署，修改后，需要先在本地执行部署
### 本地部署
build images  
```shell script
docker build -t assistant/server:2.0.2
```
以ocpuser用户运行  
```shell script
docker run -i -t -p 8080:8080 -u ocpuser -d assistant/server:2.0.2 /bin/bash
docker exec -it xxx /bin/bash
```
开发环境需要修改环境变量后重启
修改global_config.ini中env为st
supervisorctl shutdown
supervisord -c /etc/supervisord.conf

## 对接服务
###  AIPower平台微服务应用  
计算量较大的服务均部署在AIPower平台，包括：
- 银行与非银行文本分类模型
- 相似度查找模型
- 不同语料相似度计算模型
- 记账分类模型
- 写诗模型
- 对对联模型
- 藏字联模型
### 本体引擎
### 搜索引擎
### 社区引擎

## 网络开通
### 互联网访问
1. 天气API域名: tianqiapi.com
2. 股票API域名: xueqiu.com
### DMZ区
1. 汇率查询: xds.cmbchina.com, hosts 10.0.41.35
            fx.cmbchina.com
2. 搜索引擎: suggest.cmbchina.com hosts, 10.0.102.227:9093


### 数据库访问
1. tools中update需要访问远程银行数据库拉取语料，因此需要开通
相关端口:  
10.8.7.63:1433

## 语料管理
1. 开发环境通过开发配置页面配置语料```TODO```
2. 生产环境通过远程银行管理页面管理语料

## 配置平台
配置平台可进行功能/活动相关配置，可在“一事通”->“专业系统”，搜索添加“手机银行智能助理配置管理系统”

## 后台进程
### 本地缓存数据更新
应用数据更新方式有2种： 
1. 从配置平台/或其它数据源[定时拉取](assistant/bin/update.py)相关配置数据，缓存在本地，web进程定时检测到本地版本变更后重新加载数据
2. 实时访问ES获取最新语料/词槽数据
### 应用监控
通过后台[监控程序](assistant/bin/app_monitor.py)监控应用状态，将告警信息
### 日志推送到ES
每隔3s批量[更新日志](assistant/bin/update.py)到ES中

# 辅助应用
辅助应用需要依赖assistant相关包，但独立部署在其它机器，包括：
## 告警
应用在[tools/alert](assistant/tools/alert)目录，单台机器定时拉取es告警数据，通过招呼订阅号推送告警信息
部署机器: 大数据跳板机12.0.2.82  
运行方式:   
```shell script
nohup python tools/alert/alert.py > alert.log &
```

## ES数据更新  
应用在[tools/update_es](assistant/tools/update_es.py)，单台机器定时采集并更新ES(双集群)数据  
运行方式:
```shell script
nohup python tools/update_es.py > update_es.log &
```


### 动态数据:
- 语料
- 理财/基金/私人基金

### 本地词槽数据:
- 垃圾分类
- 货币名称
- 商户
- 记账分类
- 同义词/常用词/时间词/地名


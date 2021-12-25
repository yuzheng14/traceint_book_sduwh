# tracient-book-sduwh

山东大学（威海）我去图书馆抢座脚本

**请认真阅读许可证**

## 许可证（请以LICENSE文件为准，此处仅提供阅读）

                        禁止盈利许可证
                        2021/12/1 v1.0
    
    在本许可证保护下，所有包含本项目代码（包括部分代码）的项目，不允许盈利，
    可免费自己使用或提供他人使用，但不允许盈利或收取费用。
    
    请在国家法律许可的范围内使用本项目代码，如您使用本代码，则默认您已知晓是
    否在法律允许范围之内，项目作者不承担任何因超出法律范围使用本项目代码带来
    的法律纠纷。

## 使用方法

目前本项目代码可以实现明日预约、实时/定时捡漏、退座

目前代码重构以及更改通用性中，随时可能更改使用方法

main分支为稳定可用分支

### python版本

开发时所用版本为`3.8.2`

点击下载安装包：[3.8.2官网安装包](https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe)

> 官网下载链接下载慢可将链接复制到迅雷创建下载任务

经测试`3.10.1`会导致找不到适合的`ddddocr`依赖

### 包

```shell
pip install -r requirements.txt
```

### 明日预约

1. 抓包得到图书馆post请求header的cookie
2. 调用`com.yuzheng14.traceint.traceint`中的`seat_reserve`函数，参数详见docstring
3. 冲杯咖啡等待即可

### 实时捡漏

1. 抓包得到图书馆post请求header的cookie
2. 调用`com.yuzheng14.traceint.traceint`中的`seat_pickup`函数，参数详见docstring
3. 冲杯咖啡等待即可

### 退座

1. 抓包得到图书馆post请求header的cookie
2. 调用`com.yuzheng14.traceint.traceint`中的`seat_cancel`函数，参数详见docstring
3. 冲杯咖啡等待即可

### 签到

1. 抓包得到图书馆post请求header的cookie
2. 调用`com.yuzheng14.traceint.traceint`中的`credit_sign`函数，参数详见docstring
3. 冲杯咖啡等待即可

## uml设计

### 用例图
![](https://www.plantuml.com/plantuml/png/XPFVRX915CRlzodsKYymqKj2ID-4J9TJsB2mE3DRDCQ46lz0KwZMAiIOg4sjfab5ZPQciJoDCyk-XRCpi-nEDXcv8E7CRyuvtyStMuGYJADku5JZuwzyjAowYBWH0UpqaTT1BN0zH80ySbpnkPNCVlBP9PzyudyERwSawICCwYo-MB7HTrNrMprzOJXarrzaSU3JTXEZWJhWyocVVKvEdiRNP_AOXjqGut3WFDvCzdjU43NXhXxEHgVyxGMVBzZBC_v-p6vUYmwY-z-RYUpGHhlG882en8M6T7DnRNKUJnTy_oHR18Ftq0kWiHs67Rtb-S5wiUU9tpvi-lCt8uchScCN1NupKpfcgsVyu0NxzaxOaSn-iUFJvFcHaebyMjnNIOptB_bmJm9z31Y4mUco5D6856aXYeqd-Gx2fRB6p2ejDbUWlkEFQf27-jHh8mKKzEUw-VGecN-GnViHH53s_bxc_TMLo4TXaN27Gg-m03jyjVwz7C0s2RqEqFLYoNyyaMHMCq0COY0fOheYLd3I-BcLPZZeLUewOKOfqszKPUYCIfuu9prpAzXljUaTtTAjkhKQF10gclMw1WBOIS-p_WRXg5kojs0sONEhjPesIr06P4J7mXc9j61fj8nZ9zlq_nDBg6nc0yf1jUCwRlQfCdnsGYRHZfHVWMbB_kVe6pfT9bPqtRMIXgisi6IPbTQEMHcvd0RoHsSoqh4Coj-RwOcp9N8STOD_)

##  scrum敏捷开发

### 迭代

#### 功能完善1

- [X] 退座代码
- [X] 保存每日爬取验证码图片

#### 验证码问题

- [X] 比较ddddocr与mugle_ocr准确率

#### 重构

- [X] 设计用例图
- [x] 重构代码
- [x] 注释
- [x] 根据代码扫描结果修改代码
- [ ] 画时序图

#### 功能完善2

- [ ] 签到代码嵌入闲时捡漏与明日预约
- [ ] 签到代码
- [x] 查看排队状态
- [ ] 预约代码加入排队延迟继续预定

#### 封装

- [ ] tkintr封装
- [ ] 后端
- [ ] 前端
- [ ] docker打包

**都看到这里了不给个star嘛？**

## 微信OAuth认证尝试

请求获取oauth url与实际请求oauth url对比

请求得到

```
https://open.weixin.qq.com/connect/oauth2/authorize
?appid=wx2996d437cd442527
&redirect_uri=https://wechat.v2.traceint.com/index.php/url/auth.html
?r=https://wechat.v2.traceint.com/index.php/reserve/index.html
?f=wechat
&n=617f6d050f140
&response_type=code
&scope=snsapi_userinfo
&state=1
&connect_redirect=1
#wechat_redirect
```

实际请求

```
https://open.weixin.qq.com/connect/oauth2/authorize
?appid=wx2996d437cd442527
&redirect_uri=https://wechat.v2.traceint.com/index.php/url/auth.html
?r=https://wechat.v2.traceint.com/index.php/reserve/index.html
?f=wechat
&n=617f6d050f14
&response_type=code
&scope=snsapi_userinfo
&state=1
&connect_redirect=1
&uin=MjAwNTcxNTA3OA%3D%3D
&key=c39cf953308ace2d1d5dfaab91543e6b5ca955eb40d997fa3aaf8652bad19b0f1e77c908c52f7be9c83b12e7452079ce795fcc8f44bd6dcb272646c0575754771afd4b8299ca67b14d64fc9fdbf547fc01016c67d4aae21fa7b0be744806aa4faa84ec3d8f1c77bfa41c6dcd108a6d5a2524b5e1378c8a1c45f772c5c35d3e3c
&version=63040026
&pass_ticket=yxHHNjeZdF9nA6MWULlbzgEPps4czteK399zvDw0%2BOQMh6m95nCR19kubhSzaoCn
```

其中新加`uin`、`key`、 `version`、 `pass_ticket`四个参数，`uin`和`version`相对固定，`key`和`pass_ticket`为随时生成。

带有`wechatSESS_ID`和`SERVERID`发送请求则返回该cookie
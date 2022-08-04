# Certbotool

基于certbot包装的dns适配层工具，可以进行多账号多dns解析平台的配置（例如：你可以维护多个dnspod账号和aliyun账号的域名进行certbot的dns认证）。

相比直接使用certbot：
* 工具更加集成，命令参数更加简便。
* 适用于维护泛域名证书
* 可以单机下维护来自多种dns解析平台、多个账号的域名。

## RPM仓库

本项目使用rpmbuild构建安装包，不需要复杂的环境配置，开箱即用。

配置仓库可直接下载配置好的repo文件到/etc/yum.repos.d

```
wget https://rpm.mntmdev.com/repo/mntmdev.repo -O /etc/yum.repos.d/mntmdev.repo
```

安装项目的所有组件

```
yum install certbotool* -y
```

## certbotool

dns选项：DNS认证接口，由certbot调用，用户不应手动显式调用该接口。

```
certbotool dns [-h] [-c CONFIG] [-d]
```

cert选项：新增域名时使用下述命令，只需提供配置名称和新增的域名。

```
certbotool cert [-h] [-c CONFIG] [-d DOMAIN]
```

## certbotool-plugins

该包提供主流的DNS解析插件，现已支持的类型有：
* DNSPOD(腾讯云解析)
* Aliyun(阿里云解析)

安装后，在/etc/certbotool/conf.d目录下会自带.json.template的模板文件，用户需要根据每个插件认证参数的具体要求填写json配置。

certbotool-dnspod:

APIKEY的配置 https://console.dnspod.cn/account/token/token

鉴权方式说明 https://docs.dnspod.cn/api/api-public-request/

```
{
    "script":"certbotool-dnspod",
    "params":{
        "key":"API_ID,API_TOKEN"
    }
}
```

certbotool-aliyun:

创建用户、AccessKey、授权 https://ram.console.aliyun.com/users

```
{
    "script": "certbotool-aliyun",
    "params": {
        "key_id": "阿里云api的KEY_ID",
        "key_secret": "阿里云api的KEY_SECRET"
    }
}
```

## certbotool-crond

该包提供定时自动续期的daemon服务，参数配置文件为/etc/certbotool/daemon.json

```
{
    "log_directory":"日志存放目录",
    "post_renew": "所有域名续期后执行的脚本(比如重启nginx)"
}
```

daemon服务管理脚本如下

```
systemctl enable certbotool-crond # 设置自动启动
systemctl start certbotool-crond # 启动服务
```
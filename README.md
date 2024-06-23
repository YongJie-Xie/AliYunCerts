# 阿里云全站加速 SSL 证书自动部署工具

本工具配合 `acme.sh` 实现了将免费证书自动上传到阿里云全站加速的功能，解决了阿里云免费证书额度不足的问题。

---

## 运行要求

1. 拥有包含 `AliyunYundunCertFullAccess` 和 `AliyunDCDNFullAccess` 权限的访问凭据
2. 拥有 Python 3 运行环境
3. 拥有能够正常申请 SSL 证书的 `acme.sh` 环境

### 准备运行环境

操作系统使用 Debian / Ubuntu 均可，因其默认集成 Python 3 环境较为方便。

```shell
apt install -y git python3-venv
git clone https://github.com/YongJie-Xie/AliYunCerts.git /opt/aliyun-certs
python3 -m venv /opt/aliyun-certs/venv
/opt/aliyun-certs/venv/bin/python -m pip install -r /opt/aliyun-certs/requirements.txt
```

### 配置参数

编辑 `/opt/aliyun-certs/main.py` 文件（如需从环境变量读取参数，可自行修改代码）

1. 将 `access_key_id` 和 `access_key_secret` 替换为有效的访问凭据
2. 在 `domains` 中填充需要自动部署证书的全站加速域名
3. 将 `acme_domain` 修改为 需要申请证书的域名 或 命令 `acme.sh --list` 输出结果中 `Main_Domain` 列的值

## 集成到 acme.sh 中

### 方法一：（未申请证书）

```shell
acme.sh --issue --dns dns_ali -d example.com --renew-hook "/opt/aliyun-certs/venv/bin/python /opt/aliyun-certs/main.py"
```

### 方法二：（已申请证书）

编辑 `acme.sh` 工作目录下对应域名的配置文件，如：`/root/.acme.sh/example.com_ecc/example.com.conf`

修改其中的 `Le_RenewHook` 配置项为如下值

```ini
Le_RenewHook='__ACME_BASE64__START_L29wdC9hbGl5dW4tY2VydHMvdmVudi9iaW4vcHl0aG9uIC9vcHQvYWxpeXVuLWNlcnRzL21haW4ucHk=__ACME_BASE64__END_'
```

> 注：中间部分是 `/opt/aliyun-certs/venv/bin/python /opt/aliyun-certs/main.py` 的 Base64 编码形式

## 测试

执行测试会上传已经申请的免费证书到阿里云数字证书管理服务中，并修改对应全站加速域名中配置的 HTTPS 证书。

```shell
/opt/aliyun-certs/venv/bin/python /opt/aliyun-certs/main.py
```

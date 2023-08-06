# opsadmin


## 初始化数据库

```sql
CREATE DATABASE `opsadmin` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
create user 'opsadmin'@'%' identified by 'opsadmin';
GRANT all privileges on opsadmin.* to 'opsadmin'@'%';
flush privileges;
```

## 环境变量
本地开发环境如果不是使用的容器,还应加入以下环境变量

```sh
# bash
export CONSUL_HTTP_SSL='true'
export CONSUL_HTTP_ADDR='127.0.0.1:8500'
export CONSUL_HTTP_TOKEN='711923e3-a7a7-2ccb-1f9c-ca98fdb327fe'
export CONSUL_NAMESPACE='dev'
# powershell
$env:CONSUL_HTTP_SSL='true'
$env:CONSUL_HTTP_ADDR='127.0.0.1:8500'
$env:CONSUL_HTTP_TOKEN='711923e3-a7a7-2ccb-1f9c-ca98fdb327fe'
$env:CONSUL_NAMESPACE='dev'
```

## 容器部署

### Build镜像
```bash
tar zcf cicd/docker/opsadmin.tar.gz \
    --exclude=.git \
    --exclude=venv \
    --exclude=logs \
    --exclude=temp \
    --exclude=cicd \
    --exclude=README.md \
    ./
cd cicd/docker
docker build -t opsadmin .
```


## Django
以下内容待总结
### 配置
环境变量
DB查询
项目自身的conf model查询
### simpleui

### 简单的API
#### url
#### views

### 修改APP显示顺序

### 修改Model显示顺序

### Model类
#### 检查联合字段唯一性
#### 字段颜色

### ModelAdmin类
#### 搜索和指定字段搜索
#### save_model

#### 权限
get_readonly_fields
has_add_permission
has_delete_permission
has_change_permission
### Model操作数据库

### 


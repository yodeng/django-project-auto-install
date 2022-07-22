## djano项目自动化安装部署并编译

`django`开发的项目，封装成`python`包，通过`pip`一键安装部署，同时使用`cython`对源码进行编译处理。

#### 1. 安装

```shell
git clone https://github.com/yodeng/django-project-auto-install.git
pip3 install -r ./django-project-auto-install/requirements.txt
pip3 install ./django-project-auto-install
```

+ 安装后，各`app`独自为`python`模块包，路径为 `site.getsitepackages()[0]`

+ 原`manager.py`文件需要改成`main()`模块导入，而不是直接运行，可通过安装生成的命令`console_scripts`替代。
+ 本项目为示例，自己项目对应进行代码调整即可，需注意应用名是否和已存在的模块名冲突。



#### 2. 使用

```shell
$ kpipe --help

Type 'kpipe help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```


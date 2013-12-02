# 得图云 Python SDK<a style="font-size:16px" href="https://github.com/suiqirui1987/detuyun-python-sdk/archive/master.zip">[下载]</a>


得图云存储 Python SDK，基于<a href="http://www.detuyun.com/docs/page1.html" target="_blank">得图云存储 HTTP REST API 接口</a> 开发。该SDK不再兼容 1.x 的版本，相比旧版本，新版接口设计和实现更加 Pythonic ，且代码风格完全符合 <a href="https://pypi.python.org/pypi/pep8" target="_blank">pep8</a> 规范。


- [应用接入](#install)
	- [获取Access Key 和 Secret Key](#acc-appkey)
- [使用说明](#detuyun-api)
	- [1 初始化DetuYun](#detuyun-init)
	- [2 上传文件](#detuyun-upload)
	- [3 下载文件](#detuyun-down)
	- [4 创建目录](#detuyun-createdir)
	- [5 删除目录或者文件](#detuyun-deletedir)
	- [6 获取目录文件列表](#detuyun-getdir)
	- [7 获取文件信息](#detuyun-getfile)
	- [8 获取空间使用状况](#detuyun-getused)
- [异常处理](#detuyun-exception)


<a name="install"></a>
## 应用接入

<a name="acc-appkey"></a>

### 1. 获取Access Key 和 Secret Key

要接入得图云存储，您需要拥有一对有效的 Access Key 和 Secret Key 用来进行签名认证。可以通过如下步骤获得：

1. <a href="http://www.detuyun.com/user/accesskey" target="_blank">登录得图云开发者自助平台，查看 Access Key 和 Secret Key 。</a>

<a name=detuyun-api></a>
## 使用说明
<a name="detuyun-init"></a>
### 1.初始化 DetuYun


	import deutuyun
	
	dt = detuyun.DetuYun('bucket', 'username', 'password', timeout=30)


其中，参数 `bucket` 为空间名称，`username` 和 `password` 分别为授权操作员帐号和密码，必选。

参数 `timeout` 为 HTTP 请求超时时间，默认 60 秒，可选。

根据网络状况，得图云存储 API 默认设置接入点为：ED_HOST=s.detuyun.com，并自动接入。

<a name="detuyun-upload"></a>
### 2.上传文件

#### 直接传递文件内容的形式上传


	res = dt.put(rootpath + 'ascii.txt', ascii(), checksum=True)


其中，方法 `dt.put` 默认已开启相应目录的自动创建。

#### 数据流方式上传，可降低内存占用


	headers = {"x-gmkerl-rotate": "180"}
	with open('unix.png', 'rb') as f:
		res = dt.put(rootpath + 'xinu.png', f, checksum=False,
			headers=headers)


其中，参数 `checksum` 和 `headers` 可选，前者默认 False，表示不进行 MD5 校验; 后者可根据需求设置自定义 HTTP Header，例如作图参数 x-gmkerl-*, 具体请参考 <a href="http://www.detuyun.com/docs/page2.html" target="_blank">标准 API 上传文件</a> 。

上传成功，如果当前空间是图片空间，那么 `res` 返回的是一个包含图片长、宽、帧数和类型信息的 Python Dict 对象 (文件空间，返回一个空的 Dict)：


	{ 'width': '1280', 'height': '800', 'frames': '1','type': 'PNG'}


上传失败，则抛出相应异常。

<a name=detuyun-down></a>
###3. 下载文件

#### 直接读取文件内容

	res = dt.get(rootpath + 'ascii.txt')


下载成功，返回文件内容; 失败则抛出相应异常。

#### 使用数据流模式下载，节省内存占用


	with open('xinu.png', 'wb') as f:
		dt.get(rootpath + 'xinu.png', f)


下载成功，返回 Python `None` 对象; 失败则抛出相应异常。

<a name=detuyun-createdir></a>
###4. 创建目录


	dt.mkdir(rootpath + 'temp')


创建成功，返回 Python `None` 对象; 失败则抛出相应异常。

<a name=detuyun-deletedir></a>
###5. 删除目录或文件


	dt.delete(rootpath + 'xinu.png')
	if not ispicbucket:
	dt.delete(rootpath + 'ascii.txt')	
	dt.delete(rootpath + 'temp')
	dt.delete(rootpath)


删除成功，返回 Python `None` 对象; 失败则抛出相应异常。注意删除目录时，必须保证目录为空。

<a name=detuyun-getdir></a>
###6. 获取目录文件列表


	res = dt.getlist(rootpath)

	print "oked\n"
        if res:
            space = 12
            types = ["name", "type", "size", "time","filetype"]
            print '|'.join([t.center(space) for t in types])
            print '-'*(space*len(types)+len(types)-1)
            for item in res:
                print '|'.join([' ' + item[t].ljust(space-1) for t in types])


获取目录文件以及子目录列表。需要获取根目录列表是，使用 `res = dt.getlist(rootpath)` ，或直接用方法不传递参数。获取失败，则抛出相应的异常。

<a name=detuyun-getfile></a>
### 7.获取文件信息


	res = dt.getinfo(rootpath + 'xinu.png')


获取文件信息时通过Tab键分隔获取相应内容，返回结果为一个数组。

<a name=detuyun-getused></a>
### 8.获取空间使用情况


	res = dt.usage()


获取成功，始终返回该空间当前使用的总容量，单位 Bytes; 失败则抛出相应异常。

<a name=detuyun-exception></a>
### 异常处理

	
    except detuyun.DetuYunServiceException as se:
        print "failed\n"
        print "Except an DetuYunServiceException ..."
        print "HTTP Status Code: " + str(se.status)
        print "Error Message:    " + se.msg + "\n"
        if se.err:
            print se.err
    except detuyun.DetuYunClientException as ce:
        print "failed\n"
        print "Except an DetuYunClientException ..."
        print "Error Message: " + ce.msg + "\n"


其中， `DetuYunServiceException` 主要是得图云存储端返回的错误信息，具体错误代码请参考<a href="http://www.detuyun.com/docs/page6.html" target="_blank">标准 API 错误代码表</a>; 而 `DetuYunClientException` 则主要是一些客户端环境的异常，例如客户端网络超时等。

### 其他说明

具体请参考 `demo/try.py` 的代码，建议可在修改以下代码后直接运行该脚本，观察其输出情况，以便对整个 Python SDK 接口有个大致的了解：


# ------------------ CONFIG ---------------------
BUCKETNAME = 'bucketname'

USERNAME = 'username'

PASSWORD = 'password'
# -----------------------------------------------


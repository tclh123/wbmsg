#wbmsg API Manual - ver1.0

类型 | URL | 描述
------------ | ------------- | ------------
请求授权 | /login  | 登陆微博
读取接口 | / 或 /list  | 获取个人私信列表
读取接口 | /chat  | 获取个人与某用户的所有私信
写入接口 | /new 或 /send  | 发送私信
写入接口 | /del  | 删除个人与用户的所有私信

*以下微博均指新浪微博（weibo.com）*

##1、登陆微博
* 详细：接受用户名、密码，返回用户ID（uid）、token
* URL：/login
* 支持格式：JSON
* HTTP请求方式：POST
* 请求参数：

	参数名 | 必选 | 类型及范围 | 说明
------------ | ------------- | ------------ | ------------
username | true  | string | 微博的用户名（不是昵称）
password | true  | string | 微博的密码

* 返回结果示例：
			
		{
	    	"token": "3_58a34beb091a6343faa0dbcf56a21b9b654000",
	    	"uid": "1659177000"
		}
	*注：出错则返回的值都是null*
			
* 返回字段说明：

	返回值字段 | 字段类型 | 字段说明
------------ | ------------- | ------------
token | string | 登陆令牌
uid | string | 微博用户uid

##2、获取私信列表
* 详细：接受uid、token，返回个人私信列表
* URL：/ 或 /list
* 支持格式：JSON
* HTTP请求方式：GET
* 请求参数：

	参数名 | 必选 | 类型及范围 | 说明
------------ | ------------- | ------------ | ------------
uid | true  | string | 个人微博的uid（如，1903362107）
token | true  | string | 进行login后获得的令牌（token）

* 返回结果示例：
			
		[
		    {
		        "content": "。。。结果现在连勋章界面都看不到了",
		        "uid": "1659177872",
		        "touid": "2690970993"
		    },
		    {
		        "content": "秘密",
		        "uid": "1659177872",
		        "touid": "2660227393"
		    },
		    {
		        "content": "。。。。。",
		        "uid": "1659177872",
		        "touid": "1576800122"
		    },
		    {
		        "content": "嗯,拜拜",
		        "uid": "1659177872",
		        "touid": "2035855614"
		    },
		    {
		        "content": "嗯~",
		        "uid": "1659177872",
		        "touid": "1741694220"
		    },
		    {
		        "content": "╮(╯▽╰)╭无知小学妹么",
		        "uid": "1659177872",
		        "touid": "2341143242"
		    }
		]
			
* 返回字段说明：

	返回值字段 | 字段类型 | 字段说明
------------ | ------------- | ------------
content | string | 私信内容
uid | string | 微博用户uid
touid | string | 对方的uid

##3、获取私信对话
* 详细：接受uid、token、touid，返回个人与某用户的所有私信（对话）
* URL：/chat
* 支持格式：JSON
* HTTP请求方式：GET
* 请求参数：

	参数名 | 必选 | 类型及范围 | 说明
------------ | ------------- | ------------ | ------------
uid | true  | string | 个人微博的uid（如，1903362107）
token | true  | string | 进行login后获得的令牌（token）
touid | true | string | 对方的uid

* 返回结果：

		[
		    {
		        "content": "。。。结果现在连勋章界面都看不到了",
		        "is_receive": 1,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:35"
		    },
		    {
		        "content": "......无聊么",
		        "is_receive": 0,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:35"
		    },
		    {
		        "content": "为了勋章。。。",
		        "is_receive": 1,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:34"
		    },
		    {
		        "content": "谁叫你升的..",
		        "is_receive": 0,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:34"
		    },
		    {
		        "content": "...",
		        "is_receive": 0,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:34"
		    },
		    {
		        "content": "新版微博用不来。。。",
		        "is_receive": 1,
		        "uid": "1659177872",
		        "touid": "2690970993",
		        "time": "11月26日 23:33"
		    }
		]
		
* 字段说明：

	返回值字段 | 字段类型 | 字段说明
------------ | ------------- | ------------
content | string | 私信内容
is_receive | int | 是否是接收到的私信
uid | string | 微博用户uid
touid | string | 对方uid
time | string | 私信发送或接收的时间

##4、发送私信
* 详细：接受uid、token、text、touid，进行私信的发送
* URL：/new 或 /send
* 支持格式：JSON
* HTTP请求方式：POST
* 请求参数：

	参数名 | 必选 | 类型及范围 | 说明
------------ | ------------- | ------------ | ------------
uid | true  | string | 个人微博的uid（如，1903362107）
token | true  | string | 进行login后获得的令牌（token）
text | true | string，长度小于等于200汉字 | 私信内容
touid | true | string | 对方的uid

* 返回结果：

		{
		    "response": "发送成功"
		}

* 字段说明：

	返回值字段 | 字段类型 | 字段说明
------------ | ------------- | ------------
response | string | 服务器返回结果

##5、删除私信
* 详细：接受uid、token、touid，删除个人与某用户的所有私信
* URL：/del
* 支持格式：JSON
* HTTP请求方式：POST
* 请求参数：

	参数名 | 必选 | 类型及范围 | 说明
------------ | ------------- | ------------ | ------------
uid | true  | string | 个人微博的uid（如，1903362107）
token | true  | string | 进行login后获得的令牌（token）
touid | true | string | 对方的uid

* 返回结果：

		{
		    "response": "删除成功"
		}

* 字段说明：

	返回值字段 | 字段类型 | 字段说明
------------ | ------------- | ------------
response | string | 服务器返回结果
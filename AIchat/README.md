# 腾讯聊天接口的简单使用

### 1.腾讯AI聊天接口简介
基础闲聊接口提供基于文本的基础聊天能力，可以让您的应用快速拥有具备上下文语义理解的机器聊天功能。<br>
### 2.参数说明
参数名称|是否是必选|数据类型|数据约束|示例数据|描述
-------|-------|-------|-------|-------|------
app_id|是|int|正整数|1000001|应用标识（AppId）
time_stamp|是|int|正整数|1493468759|请求时间戳（秒级）
nonce_str|是|string|非空且长度上限32字节|非空且长度上限32字节|随机字符串
sign|是|string|非空且长度固定32字节|B250148B284956EC5218D4B0503E7F8A|签名信息，详见接口鉴权
session|是|string|UTF-8编码，非空且长度上限32字节|10000|会话标识（应用内唯一）
question|是|string|UTF-8编码，非空且长度上限300字节|你的名字|用户输入的聊天内容
### 3.响应参数
参数名称|是否必选|数据类型|描述
-------|-------|-------|-----
ret|是|int|返回码； 0表示成功，非0表示出错
msg|是|string|返回信息；ret非0时表示出错时错误原因
data|是|object|返回数据；ret为0时有意义
session|是|string|UTF-8编码，非空且长度上限32字节
answer|是|string|UTF-8编码，非空
### 4.签名算法
**调用腾讯API必须使用签名机制，否则校检不通过。**<br>
##### 计算步骤：
1. 将<key, value>请求参数对按key进行字典升序排序，得到有序的参数对列表N
2. 将列表N中的参数对按URL键值对的格式拼接成字符串，得到字符串T（如：key1=value1&key2=value2），URL键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8，而不是小写%e8
3. 将应用密钥以app_key为键名，组成URL键值拼接到字符串T末尾，得到字符串S（如：key1=value1&key2=value2&app_key=密钥)
4. 对字符串S进行MD5运算，将得到的MD5值所有字符转换成大写，得到接口请求签名
<br>
**腾讯相关文档链接：**
* https://ai.qq.com/doc/nlpchat.shtml
* https://ai.qq.com/doc/auth.shtml

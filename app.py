from flask import Flask, request
from WXBizMsgCrypt import WXBizMsgCrypt
import wx_util
import time


# 自行修改一下参数
sToken = "KV7DxCtuOsS8GrDXXXXX"  # 企业微信后台填写的token
sEncodingAESKey = "DnUujNA863ts5DRkPhFEXzhASbcpGhIS0GukxbXXXXX"   # 企业微信后台，应用详情页，开启“消息加解密”时显示
sCorpID = "ww4ad764c3c14XXXXX"  # 企业ID
wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wx_interface():
    # 响应url回调验证
    if 'GET' == request.method:
        return wx_interface_get()
    # 响应消息事件
    elif 'POST' == request.method:
        return wx_interface_post()
    else:
        pass


# 响应url回调验证
def wx_interface_get():
    sVerifyMsgSig = request.args.get("msg_signature")
    sVerifyTimeStamp = request.args.get("timestamp")
    sVerifyNonce = request.args.get("nonce")
    sVerifyEchostr = request.args.get("echostr")
    ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchostr)
    if (ret != 0):
        print('')
        return "无法处理该请求，确定是企业微信服务器发来的请求吗？"
    return sEchoStr


# 响应消息事件
def wx_interface_post():
    request_str = str(request.data, 'utf-8')
    sReqMsgSig = request.args.get("msg_signature")
    sReqTimeStamp = request.args.get("timestamp")
    sReqNonce = request.args.get("nonce")
    ret, request_str_Encrypt = wxcpt.DecryptMsg(request_str, sReqMsgSig, sReqTimeStamp, sReqNonce)
    read_dict = wx_util.xmlTodict(request_str_Encrypt)
    if (ret != 0):
        return "无法处理该请求，确定是企业微信服务器发来的请求吗？"
    print("接收报文：" + str(request_str_Encrypt))
    print(read_dict)

    TimeStamp = str(int(time.time()))
    return_str = getReturnStr(read_dict, TimeStamp)
    ret, sEncryptMsg = wxcpt.EncryptMsg(return_str, TimeStamp, TimeStamp)
    return sEncryptMsg


# 判断消息类型
def getReturnStr(read_dict, TimeStamp):
    # 文本消息
    if 'text' == read_dict['xml']['MsgType']:
        # 提取消息内容
        textContent = read_dict['xml']['Content']
        # textContent = "你好"
        print(textContent)
        return text(read_dict, TimeStamp, textContent)

    # 图片消息
    elif 'image' == read_dict['xml']['MsgType']:
        textContent = "该类型消息暂时未开发！！！"
        print(textContent)
        return text(read_dict, TimeStamp, textContent)

    # 语音消息
    elif 'voice' == read_dict['xml']['MsgType']:
        textContent = "该类型消息暂时未开发！！！"
        print(textContent)
        return text(read_dict, TimeStamp, textContent)

    # 视频消息
    elif 'video' == read_dict['xml']['MsgType']:
        textContent = "该类型消息暂时未开发！！！"
        print(textContent)
        return text(read_dict, TimeStamp, textContent)

    # 位置消息
    elif 'location' == read_dict['xml']['MsgType']:
        textContent = "该类型消息暂时未开发！！！"
        print(textContent)
        return text(read_dict, TimeStamp, textContent)

    # 事件函数
    elif 'event' == read_dict['xml']['MsgType']:
         # textContent = "该类型消息暂时未开发！！！"
         textContent = read_dict['xml']['EventKey']
         print(textContent)
         return text(read_dict, TimeStamp, textContent)


# 发送文本信息
def text(read_dict, TimeStamp, textContent):
    str = '''
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName> 
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
    </xml>
    ''' % (read_dict['xml']['FromUserName'],
           read_dict['xml']['ToUserName'],
           TimeStamp,
           textContent)
    return str


def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

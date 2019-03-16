# -*- coding:utf-8 -*-

import web
import hashlib
import receive
import reply


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            # 和公众平台官网-->基本配置中信息填写相同
            token = "douban_kgqa"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return "I don't Know"
        except Exception as err:
            print('ERROR: ' + str(err))
            return err

    def POST(self):
        try:
            webData = web.data()
            # 后台打印日志
            print('Handle Post webdata is ', webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    content = "彩虹屁屁"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print('暂且不处理')
            return reply.Msg().send()
        except Exception as err:
            print('ERROR: ' + str(err))
            return err


urls = (
    '/douban_kgqa', 'Handle'
)

if __name__ == '__main__':
    douban_kgqa_web = web.application(urls, globals())
    douban_kgqa_web.run()

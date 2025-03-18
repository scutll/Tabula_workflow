import time
import random
import asyncio
'''
request_list: 从前端接收到的请求，即将执行
request_to_send 将要发送到前端的请求
pending_requests 发送后等待确认的请求
'''
request_list=[]
request_to_send=[]
request_response={}
pending_requests={}


#将要发送的信息添加上requestId后加入到发送队列
def add_to_send_list(data):
    data['requestId']=Get_requestId()
    request_to_send.append(data)
    return data['requestId']


'''
get an unique requestId
时间戳+三位随机数+py2ht
'''
def Get_requestId():
    suffix='py2ht'
    times=int(time.time())
    rand=random.randint(100,999)
    return str(times)+str(rand)+suffix


async def wait_for_response(requestId):
    while True:
        #判断request_response是否有requestId键
        if requestId in request_response:
            data=request_response[requestId]
            del request_response[requestId]
            return data
       
        await asyncio.sleep(0.1)

'''
向客户端发送信息，并获取返回值
data: 发送的数据
'''
async def sendMsg(data):
    requestId=add_to_send_list(data)
    response=await wait_for_response(requestId)
    return response
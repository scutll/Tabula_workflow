import websockets
import asyncio
import json
import time


'''
request_list: 从前端接收到的请求，即将执行
request_to_send 将要发送到前端的请求
pending_requests 发送后等待确认的请求
'''
request_list=[]
request_to_send=[]
pending_requests={}

#将要发送的信息添加上requestId后加入到发送队列
def add_to_send_list(data):
    data['requestId']=Get_requestId()
    request_to_send.append(data)

   

'''
接收前端消息
confirm: 删除对应pending
其他: 将请求放入执行列表并发送确认消息
'''
async def recv(data,websocket):

    print('data: ',data)

    #前端确认收到消息，后端删除对应pending队列
    if data['type'].lower()=='confirm':
        print('confirm msg received')
        requestId=data['requestId']
        if requestId in pending_requests:
            pending_requests[requestId]['time_out'].cancel() #取消超时任务
            print('deleting pening list:')
            del pending_requests[requestId]


    elif data["type"] !='confirm': #somthing else
        #后端接收消息并发送确认请求
        print('msg received! sending confirm:')
        confirm={
            "type":"confirm",
            "data":None,
            "requestId":data['requestId']
        }
        await websocket.send(json.dumps(confirm))
        print('adding to request_list')
        request_list.insert(0,data)
        print(request_list)


'''
get an unique requestId
时间戳+py2ht
'''
def Get_requestId():
    return str(int(time.time()*1000))+'py2ht'


'''
向前端发送消息
发送前添加入待确认(pending_reuqests)列表并在超时或被取消(confirmed)后删除，若未得到确认则添加到发送列表重新发送
'''
async def send(request,websocket):
    print('sending request')
    requestId=request["requestId"]
    await websocket.send(json.dumps(request))

    #wait for confirm
    timeout_task=asyncio.create_task(asyncio.sleep(1))
    pending_requests[requestId]={
        'data':request,
        'time_out':timeout_task
    }
    try:
        await timeout_task
        print("time out!")
        request_to_send.insert(0,pending_requests[requestId]['data'])
    except asyncio.CancelledError: #请求得到确认，超时任务被取消
        print('confirmed!')
    finally:
        if requestId in pending_requests:
            del pending_requests[requestId]




    

async def handle(websocket):

    async def recv_request():
        async for text in websocket:
            print('msg received:')
            text=text.strip("'")
            try:
                data=json.loads(text)
                print(data)
            except json.JSONDecodeError as e:
                print(e)
            asyncio.create_task(recv(data,websocket))

    async def send_request():
        while True:
            if request_to_send:
                request=request_to_send.pop(0)
                await send(request,websocket)
            await asyncio.sleep(0.1)

    await asyncio.gather(recv_request(),send_request())






async def main():
    print("server running")
    async with websockets.serve(handle,'0.0.0.0',5200):
        await asyncio.Future()

if __name__=='__main__':
    data={
        "type":"greet",
        "data":"hello",
    }
    add_to_send_list(data)
    asyncio.run(main())


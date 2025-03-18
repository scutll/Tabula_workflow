import websockets
import asyncio
import json
from globals.request import *
from workflow.workflow import workflow
from workflow.workflows import *

Workflows_ = Workflows()
'''
信息样式，confirm类信息的data为null

'{"type":"confirm", "data":null,"requestId":"1145141919810hxd"}'
'''



'''
接收前端消息
confirm: 删除对应pending
其他: 将请求放入执行列表并发送确认消息
'''


'''
confrim: 向客户端确认收到消息
'''
async def confirm(websocket, data, requestId):
    confirm={
            "type":"confirm",
            "data":data,
            "requestId":requestId
        }
    await websocket.send(json.dumps(confirm))


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
            request_response[requestId]=data

    elif data['type'] == 'test':
        print('test msg received')
        await confirm(websocket,{},data['requestId'])        
        
        response=await sendMsg({"type":"getBlockID",
        "data":{}
        })
        print("id:" +response['data']['id'])

        response=await sendMsg({
        "type":"insertBefore",
        "data":{"text":"haola"},
        "blockType":"paragraph",
        "id":response['data']['id']
        })
        print("insert sucessfully ",response)

    elif data["type"]=="getNodes":
        print('sending nodes info')
        with open("get_nodes_init.json","r",encoding="utf-8") as file:
            nodes = json.load(file)
        await confirm(websocket,nodes,data['requestId'])


    elif data["type"]=="submitWorkflow":
        data_ = data["data"]
        workflow_ = workflow.deserialization(data_)
        success = Workflows_.add_workflow(workflow_)
        if success:
            await confirm(websocket,{"status":1},data['requestId'])
        else:
            await confirm(websocket,{"status":0,"err_msg":"" },data['requestId'])



    elif data["type"]=="getWorkflows":
        workflows = dict()
        for workflow_ in Workflows_.workflows.values():
            workflows[workflow_.id] = workflow_.serialization()
        await confirm(websocket,workflows,data['requestId']) 


    elif data["type"]=="callWorkflow":
        workflow_id , params = data["id"] , data["params"]
        workflow_ = Workflows_.get_workflow(workflow_id)
        for start in workflow_.start_:
            workflow_.set_value(start.inputs[0],params)
        await confirm(websocket,"workflow running:",data['requestId'])
        workflow_.run()

        
    else: #somthing else
        #后端接收消息并发送确认请求
        print('msg received! sending confirm:')
        await confirm(websocket,{},data['requestId'])        
        print('adding to request_list')
        request_list.insert(0,data)
        print(request_list)





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
        # print(pending_requests)
        if requestId in pending_requests:
            del pending_requests[requestId]
        # print(pending_requests)




    

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

    await asyncio.gather(
        recv_request(),
        send_request())






async def main():
    print("server running")
    async with websockets.serve(handle,'0.0.0.0',5200):
        await asyncio.Future()

if __name__=='__main__':

    
    # data={
    #     "type":"insertAfter",
    #     "data":{"test":"haola"},
    #     "blockType":"paragraph"
    # }
    # add_to_send_list(data)
    # data={
    #     "type":"test",
    #     "data":"hello",
    # }
    # add_to_send_list(data)
    asyncio.run(main())
    
   


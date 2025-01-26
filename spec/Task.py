from spec.Block import Blockspec,Blockspec_List
import uuid
'''
as a execution unit of Workflow,task consist of several blocks and have connections to other tasks
a Task has:
    task_id
    state
    type
    block_list
    parents/children
'''


class Tasktype:
    '''
    types of a task:
        multichoice: to make decision with blocks
        send: to send something to html
        call_api: call api with params
        call_llm: call a large language model with params
    '''
    NORMAL='normal'
    MULTICHOICE='multichoice'
    SEND='send'
    CALL_API='call_api'
    CALL_LLM='call_llm'

class Taskstate:

    '''
    states of a task:waiting ready running finished canceled 
    '''
    WAITITNG='waiting'
    READY=1
    RUNNING=2
    FINISHED=4
    CANCELED=8

    '''
    masks:
    '''
    NOTFINISHED=READY | RUNNING | CANCELED



class taskspec:
    def __init__(self,type,state=Taskstate.WAITITNG):
        '''
        parents:  taskspec that executes before
        children: taskspec next to be executed
        '''
        self.type=type
        self.state=Taskstate
        self.blockspec_list={}
        self.parents={}
        self.children={}
        self.task_id = 'task'+str(uuid.uuid4)

    def add_block(self,blockspec):
        '''
        add a blockspec to the Taskspec if the block exists in the Blockspec_List
        '''
        print("adding a block to the Task:")
        if Blockspec_List.exist(blockspec.block_id):
            self.blockspec_list[blockspec.block_id]=blockspec
        else:
            print("block not registered!")
        
    def del_block(self,block_id):
        '''
        delete a blockspec in the blockspec_list
        '''
        print('deleting a block:')
        if block_id in self.blockspec_list:
            self.blockspec_list.pop(block_id)
        else:
            print("no such a block!")
    
    def run():
        pass

    def Serialization():
        pass

    def Deserialization():
        pass

    def connect(self,taskspec):
        '''
        connect self to the taskspec
        '''

        self.children[taskspec.task_id]=taskspec
        pass

    def connect_if(self,taskspec,if_condition):
        '''
        connect self to the taskspec with an if_condition
        '''

        self.children[taskspec.task_id]=taskspec
        self.children[taskspec.task_id]["when"]=if_condition


class Taskspec_list:
    '''
    a list to maintain taskspec created
    for workflow to choose
    '''
    def __init__(self):
        self.taskspecs={}
        self.tasks_num=0

    def exist(self,task_id):
        return True if task_id in self.taskspecs else False
    
    def add_taskspec(self,taskspec):
        if taskspec.task_id in self.taskspecs:
            print("task exists!")
        else:
            self.taskspecs[taskspec.task_id]=taskspec
            self.tasks_num+=1

    def del_taskspec(self,task_id):
        if task_id not in self.taskspecs:
            print("task does not exist!")
        else:
            self.taskspecs.pop(task_id)
            self.tasks_num-=1

Taskspec_List=Taskspec_list()

    
def Dreate_taskspec(type='normal'):
    '''
    create a taskspec:
    params: 
        type: a tasktype(default to be normal)

    return:
        the taskspec object
    '''
    task=task(type)
    print("creating task:")
    Taskspec_List.add_taskspec(task)
    return task

def Delete_taskspec(task_id):
    '''
    delete a task
    params: a task_id
    '''
    print("deleting task:")
    if task_id in Taskspec_List:
        Taskspec_List.del_taskspec(task_id)
    else:
        print("no such a task!")

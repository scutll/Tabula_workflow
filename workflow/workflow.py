'''
workflow 的创建

- Methods:
    操作任务的方法尽量减少直接引用任务对象或者id,最好是名称,因此工作流任务的名称不能重复
	- create_task 创建任务
	- delete_task_by_id/by_name 删除任务
    - set_task_name 设置任务名
	- add_input 为指定任务添加输入
	- del_input 为指定任务删除输入
	- add_output 添加输出
	- del_output 删除输出
	- set_value_name 修改变量名-这样的话所有任务都得修改一次
	- show 展示任务连接关系，返回数据化形式的结构（给前端用）
	- conncet 连接任务用
	- disconnect 删除任务连接
    - init_tasks 初始化任务状态，全部清除为waiting状态
	- check_ 检查是否满足运行格式
		- 怎么样的任务流是可运行的?
	- run 运行工作流
	- 
	- serialization/deserialization 序列化/反序列化 （任务流里包括任务节点、变量表在内的所有信息）
'''
from Task.tasks import *
from Task.TaskStatus import TaskStatus
from workflow.tasklist import tasklist
from workflow.value_table import value_table 
from utils.id import get_workflow_id

class workflow:
    def __init__(self,name:str):
        '''
        - Attri:
            - tasklist 工作流中可用的任务
            - val_table 任务要使用的变量
            - current_task 现在正在运行的任务
            - 使用一个networkx构建的有向图构建工作流
            - 初始化时就有start_task和end_task
        '''
        self.name=name
        self.id=get_workflow_id()
        self.val_table=value_table()
        self.tasks=tasklist()
        self.current_task=None
        self.starttask=self.create_task("start","start_task")
        self.endtask=self.create_task("end","end_task")

    def create_task(self,type:str,name:None):
        '''
        按照需要的类型创建任务,并将任务添加到list中
        params:
        type: 要创建的任务类型
        name: 任务名称
        '''
        task_type={"start":start_task,"end":end_task,"print":print_task}
        if type not in task:
            print("notypeerror")
            return False
        task=task_type[type](name)
        self.tasks.add_task(task)
        return True
    
    def delete_task_by_Id(self,id):
        '''
        按id删除任务
        params:
        id: 任务id
        '''
        task=self.tasks.get_task_by_Id(id)
        if task is not None:
            self.tasks.del_task(task)
            return True
        else: 
            print("no this task in tasklist")
            return False

    def delete_task_by_name(self,name):
        '''
        按name删除任务
        params:
            name 任务名
        '''
        task=self.tasks.get_task_by_name(name)
        if task is not None:
            self.tasks.del_task(task)
            return True
        
        else:
            print("cannot find by name")
            return False
        
    def set_task_name(self,old_name,new_name):
        task=self.tasks.get_task_by_name(old_name)
        if task is None:
            print("cannot find by name")
            return False
        
        else:
            task.name=new_name
            return False
        
    def has_task(self,task):
        '''
        True 则任务成功被注册到工作流
        '''
        return True if self.tasks.list.has_node(task) else False


    def init_tasks(self):
        '''
        初始化任务状态，将开始任务外的所有任务设置成等待运行的状态
        '''
        for task in self.tasks.list:
            if task.type != "start":
                task.setstatus(TaskStatus.WAITING)
            elif task.type == "start":
                task.setstatus(TaskStatus.READY)
    
    def add_input(self,task:base_taskspec,input_name):
        '''
        为任务添加新的变量
            注册到变量表并添加到task的inputs里
        '''
        if input_name in task.inputs:
            print(f"{input_name} exists in task's inputs")
            return False
        if input_name not in self.val_table.values:
            self.val_table.add_value(input_name)
        task.add_input(input_name)
        return True
    
    def del_input(self,task:base_taskspec,input_name):
        '''
        为任务删除变量
        当该任务为最后一个拥有该变量的任务时将该变量移除出变量表
        '''
        if input_name not in self.val_table.values or task.inputs:
            print("fail to find the input")
            return False
        task.remove_input(input_name)

        NeedToRemove = True
        for task in self.tasks.list:
            if input_name in task.inputs or task.outputs:
                NeedToRemove = False
        if NeedToRemove:
            self.val_table.del_value(input_name)
            print("the last input deleted")
        return True

    def add_output(self,task:base_taskspec,output_name):
        '''
        为任务添加输出
            注册到变量表并加入outputs
        '''
        if output_name in task.outputs:
            print(f"{output_name} exists in task's outputs")
            return False
        
        if output_name not in self.val_table.values:
            self.val_table.add_value(output_name)
        
        task.add_output(output_name)
        return True
    
    def del_output(self,task:base_taskspec,output_name):
        '''
        为任务删除输出
            当其他变量以该输出为input时需要删除该input
        '''
        if output_name not in self.val_table.values or task.outputs:
            print("fail to find output")
            return False
        
        task.remove_output(output_name)
        for task in self.tasks.list:
            if output_name in task.inputs:
                self.del_input(task,output_name)
        return True
    
    def set_value_name(self,old,new):
        '''
        修改变量名,变量表和tasks的输入输出都要修改
        '''
        self.val_table.set_value_name(old,new)
        for task in self.tasks.list:
            if old in task.inputs:
                task.remove_input(old)
                task.add_input(new)
            if old in task.outputs:
                task.remove_output(old)
                task.add_output(new)

    def connect(self,front_task,back_task):
        '''
        连接任务
        front_task -> back_task
        '''
        self.tasks.connect(front_task,back_task)
        if not self.tasks.is_DAG():
            print("forms a non_DAG after connection")
            self.disconnect(front_task,back_task)
            return False
        return True


    def disconnect(self,front_task,back_task):
        '''
        解除任务连接
        front_task !=> back_task
        '''
        return self.tasks.disconnect(front_task,back_task)



    def check_(self):
        pass

    def show(self):
        pass

    def serialization(self):
        pass

    def deserialization(self):
        pass
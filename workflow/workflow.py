'''
workflow 的创建

- Methods:
    操作任务的方法尽量减少直接引用任务对象或者id,最好是名称,因此工作流任务的名称不能重复
'''
from Task.tasks import *
from workflow.tasklist import tasklist
from workflow.value_table import value_table 
from utils.id import get_workflow_id
from utils.translate import translate,detranslate
import asyncio

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
        self.start_=[]
        self.end_=[]
        # self.create_task("start","start")
        # self.create_task("end","end")

    def set_id(self,id):
        self.id = id

    def create_task(self,type:str,name:None):
        task_type={"start":start_task,"end":end_task,"print":print_task,"llm":llm_task,'intent_identify':intent_identify_task,'intent_identify_plus':intent_identify_task_multi_branch,
                   "insert_paragraph":insert_paragraph}
        '''
        按照需要的类型创建任务,并将任务添加到list中\n
        params: \n
        type: 要创建的任务类型\n
            start\n
            llm\n
            end
        name: 任务名称\n

        若任务为:
            start: 添加入start_ 列表
            end: 添加入end_ 列表
        '''
        
        if type not in task_type:
            print("notypeerror")
            return False
        task=task_type[type](self.val_table,name)
        if self.tasks.add_task(task):
            if type == "start":
                self.start_.append(task)
            elif type == "end":
                self.end_.append(task)
        return task
    
    def delete_task_by_Id(self,id):
        '''
        按id删除任务
        params:
        id: 任务id
        若任务为:
            start: 移出start_ 列表
            end: 移出end_ 列表

        '''
        task=self.tasks.get_task_by_Id(id)
        if task is not None:
            self.tasks.del_task(task)
            if task.type == "start":
                self.start_.remove(task)
            elif task.type == "end":
                self.end_.remove(task)
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
        if task is None:
            print("no task")
            return False

        if task is not None:
            self.tasks.del_task(task)
            return True
        
        else:
            print("cannot find by name")
            return False
        
    def set_task_name(self,old_name,new_name):
        task=self.tasks.get_task_by_name(old_name)
        if task is None:
            print("no task")
            return False    

        if task is None:
            print("cannot find and set task name")
            return False
        
        else:
            task.name=new_name
            return True
        
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
                task.set_status("waiting")
            elif task.type == "start":
                task.set_status("ready")
    
    def add_input(self,task,input_name):
        '''
        为任务添加新的变量
            注册到变量表并添加到task的inputs里
            params:
                task:name of task
        '''
        task=self.tasks.get_task_by_name(task)
        if task is None:
            print("no task")
            return False
        
        if task.input_limit is not None and task.input_limit <= len(task.inputs):
            print("number of input exceeds") 
            return False

        if input_name in task.inputs:
            print(f"{input_name} exists in task's inputs")
            return False
        if input_name not in self.val_table.values:
            self.val_table.add_value(input_name)
        task.add_input(input_name)
        return True
    
    def del_input(self,task,input_name):
        '''
        为任务删除变量
        当该任务为最后一个拥有该变量的任务时将该变量移除出变量表
        params:
                task:name of task
        '''
        task=self.tasks.get_task_by_name(task)

        if task is None:
            print("no task")
            return False
        if input_name not in self.val_table.values or input_name not in task.inputs:
            print("fail to find the input")
            return False
        task.remove_input(input_name)

        NeedToRemove = True
        for task in self.tasks.list:
            if input_name in task.inputs or input_name in task.outputs:
                NeedToRemove = False
        if NeedToRemove:
            self.val_table.del_value(input_name)
            print("the last input deleted")
        return True



    def add_output(self,task,output_name):
        '''
        为任务添加输出
            注册到变量表并加入outputs
        params:
                task:name of task
        '''
        task=self.tasks.get_task_by_name(task)
        if task is None:
            print("no task")
            return False

        if task.output_limit is not None and task.output_limit <= task.output_limit:
            print("number of output exceeds")
            return False

        if output_name in task.outputs:
            print(f"{output_name} exists in task's outputs")
            return False
        
        if output_name not in self.val_table.values:
            self.val_table.add_value(output_name)
        
        task.add_output(output_name)
        return True
    
    def del_output(self,task,output_name):
        '''
        为任务删除输出
            当其他变量以该输出为input时需要删除该input
        params:
                task:name of task
        '''
        task=self.tasks.get_task_by_name(task)
        if task is None:
            print("no task")
            return False

        
        if output_name not in self.val_table.values or output_name not in task.outputs:
            print("fail to find output")
            return False
        
        task.remove_output(output_name)
        for task in self.tasks.list:
            if output_name in task.inputs:
                self.del_input(task.name,output_name)
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


    def outputs_of_all_parents(self,name):
        '''
        返回该任务的所有父节点的输出
        params: name of task
        returns: a dict of outputs of parents
        {
            "task1":["output1","output2"]
        }
        '''
        if self.task(name) is None:
            print("no such a task")
            return {}
        
        def collect_outputs(task):
            parents=self.parents_of(task.name)

            if not parents:
                return {}
            # 递归实现,从后到前搜寻
            outputs={}
            for parent in parents:
                outputs[parent.name]=parent.outputs
                parent_outputs=collect_outputs(parent)
                outputs.update(parent_outputs)
            return outputs
        
        return collect_outputs(self.task(name))



    def outputs_of_parents(self,name):
        '''
        返回该任务的父节点的输出
        params: name of task
        returns: a dict of outputs of parents
        {
            "task1":["output1","output2"]
        }
        '''
        task=self.task(name)
        if task is None:
            print(f"{name} does not exist")
            return {}
        parents=self.parents_of(name)
        outputs={}
        for parent in parents:
            outputs[parent.name]=parent.outputs
        return outputs
        
    def set_value(self,value_name,value):
        if value_name not in self.val_table.values:
            print(f"{value_name} do not exist!")
            return False
        self.val_table.set_value(value_name,value)
        return True    
    
    def children_of(self,name):
        '''
        寻找任务的子节点
        '''
        return self.tasks.children_of(name)


    def parents_of(self,name):
        '''
        寻找任务的父节点
        '''
        return self.tasks.parents_of(name)

    

    def connect(self,front_task:str,back_task:str,other=None):
        '''
        连接任务
        params: names of tasks
        front_task -> back_task
        '''
        if self.tasks.connect(front_task,back_task,other):
            if self.task(front_task).outputs[0] is not None:
                self.add_input(back_task,self.task(front_task).outputs[0])
        else:
            print("fail to connect")
            return False
        
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


    def cancel(self,name):
        '''
        取消任务,使任务状态为canceled
        params:
            name: name of task
        '''
        task=self.task(name)
        if task is None:
            print("fail to find task")
            return False
        task.set_status("canceled")
        return True



    def task(self,name):
        '''
        根据任务名返回工作流里的任务
        name: 任务名
        '''
        return self.tasks.get_task_by_name(name)



    async def run_(self):
        '''
        运行工作流
        使用队列,初始入队start任务并出队,设置为current_task,运行完成后加入completed,每次检查completed里的successors,若input齐全且是在等待的状态(防止重复添加)入队,status为canceled的则省略(那样被取消的任务以后的任务都会被取消,而汇合点不会被取消),然后弹队并运行直到队空
        '''
        self.init_tasks()
        task_queue=list(self.start_)
        completed=[]
        
        while len(task_queue) != 0:
            self.current_task=task_queue.pop(0)
            print(self.current_task.name," running:")


            await asyncio.gather(self.current_task.run())

            if self.current_task.is_completed():
                completed.append(self.current_task)

            # print(completed)
            for task in reversed(completed):
                delete=True
                for next in list(self.tasks.list.successors(task)):
                    if next.input_ready() and next.is_waiting():
                      delete=False
                      task_queue.append(next)  
                      next.set_status("ready")

                    # else:
                    #     print("not ready")
                if delete is True:
                    completed.remove(task)


            # print("queue:",task_queue)       
        print("finished")


    def run(self):
        asyncio.run(self.run_())


    def check_(self):
        '''
        检查工作流能否运行:
            是否成环
        '''
        if self.tasks.is_DAG():
            return False
        return True

    def show(self):
        self.tasks.tasks()
        

    def serialization(self):
        dict_=dict()
        dict_["workflow_name"]=self.name
        dict_["workflow_id"] = self.id
        dict_["tasks"], dict_["connections"] = self.tasks.serialization()
        
        # values:
        values=dict()
        for val_name,value in self.val_table.values.items():
            if value["value"] is not None:
                values[val_name] = value["value"]
            else:
                continue
        
        dict_["values"] = values
        

        return detranslate(dict_)


    @classmethod
    def deserialization(self,json):
        # json是文件的路径
        isfile = isinstance(json,str)
        if isfile:
            with open(json,'r',encoding='utf-8') as file:
                data=json.load(file)
            workflow_ = workflow(data["workflow_name"])

        # json是json格式的字典   
        data = dict(json)
        data = translate(data)

        workflow_ = workflow(data["workflow_name"])
        if "workflow_id" in data and data["workflow_id"] is not None:
            workflow_.id = data["workflow_id"]

        #tasks:
        for key,task in data["tasks"].items():
            name = task["name"]
            (workflow_.create_task(task["type"],name)).deserialization(task,key)
            
        #connections:
        for connection in data["connections"]:
            front,back = connection["from"], connection["to"]
            workflow_.connect(front,back,connection["branch"])
            
        # values:
        if "values" not in data:
            return workflow_
        values=data["values"]
        for val_name,value in values.items():
            workflow_.set_value(val_name,value)
    
        return workflow_
            
                    
        

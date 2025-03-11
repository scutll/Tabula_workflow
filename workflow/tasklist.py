from Task.base_taskspec import base_taskspec 
from Task.tasks import intent_identify_task,intent_identify_task_multi_branch
import networkx as nx



class tasklist:
    '''
    使用id标识任务
    作为有向图容器存储已创建的任务
    格式:
    {
        "task_id": task
    }
    '''
    def __init__(self):
        self.len=0
        self.list=nx.DiGraph()

    def add_task(self,task):
        '''
        add a task into the list
        id 或 名称 重复会导致创建失败

        params: the task

        '''
        if task in self.list:
            print("task exists already")
            return False
        self.list.add_node(task)
        return True
    
    def del_task(self,task):
        '''
        delete a task

        params:the task
        '''
        if task not in self.list:
            print("task does not exist")
            return False
        self.list.remove_node(task)
        return True
    

    def connect(self,front:str,back:str,other=None):

        '''
        连接任务节点,未前后节点设置
        params:
        (str) name of tasks
            front -> back
            extra -> if/else for identify_task
        '''
        front=self.get_task_by_name(front)
        back=self.get_task_by_name(back)
        if front not in self.list or back not in self.list:
            print("front and back not in list both")
            return False
        
        
        elif front in self.list and back in self.list:
            if self.list.has_edge(front,back):
                print("connection exists already")
                return False
            self.list.add_edge(front,back)
            #意图识别使用，选择要连到否定还是肯定后续
            if isinstance(front,intent_identify_task):
                if other is None:
                    other = "if"
                front.connect(back,other)
            if isinstance(front,intent_identify_task_multi_branch):
                if other is None:
                    other = 0
                front.connect(back,other)
            return True
        
    def disconnect(self,front:str,back:str):
        '''
        删除节点连接
        params:(name of tasks)
            front !=> back
        '''
        front=self.get_task_by_name(front)
        back=self.get_task_by_name(back)
        if front not in self.list or back not in self.list:
            print("front and back not in list both")
            return False
        elif front and back in self.list:
            self.list.remove_edge(front,back)
            #删除已绑定的输出
            for input in front.outputs:
                if input in back.inputs:
                    back.inputs.remove(input)

            if isinstance(front,intent_identify_task):
                if front.branch["if"] == back:
                    front.branch["if"] = None
                elif front.branch["else"] == back:
                    front.branch["else"] = None
            
            if isinstance(front,intent_identify_task_multi_branch):
                for intent in front.intents:
                    if front.branch[intent] == back:
                        del front.branch[intent]
                        break

            return True


    def get_task_by_Id(self,id):
        '''
        search the task by id and return task
        return None if not exist
        params: id
        '''
        for task in self.list:
            if task.id == id:
                return task
        print(f"cannot find by id {id}")
        return None
    
    def get_task_by_name(self,name):
        '''
        search by name
        params:name
        '''
        for task in self.list:
            if task.name == name:
                return task
        print(f"cannot find by name {name}")
        return None
    
    def get_task_by_type(self,type):
        '''
        return a list of tasks of the according type
        '''
        res=[]
        for task in self.list:
            if task.type==type:
                res.append(task)

        return res
    
    def tasks(self):
        '''
        show all tasks in the list
        and return the list if necessary
        '''
        for task in self.list:
            print("--task:")
            print(f"name: {task.name}")
            print(f"  id: {task.id}")
            print(f"type: {task.type}")
            print(f"status: {task.status}")
            print()
            print("inputs:")
            for input in task.inputs:
                print(input)
            print()
            print("outputs:")
            for output in task.outputs:
                print(output)

            print('-'*25)
        return self.list
    
    def children_of(self,name:str):
        '''
        返回指定任务的所有子节点
        params: name of task
        returns: a list of children of the task
        '''
        task=self.get_task_by_name(name)
        if task is not None:
            return list(self.list.successors(task))
        else:
            print(name," does not exist")
            return [] 

    def parents_of(self,name:str):
        '''
        返回指定任务的所有父节点
        params: name of task
        returns: a list of parents of the task
        '''
        task=self.get_task_by_name(name)
        if task is not None:
            return list(self.list.predecessors(task))
        else:
            print(name," does not exist")
            return []


    def is_DAG(self):
        return nx.is_directed_acyclic_graph(self.list)
    
    def serialization(self):
        # dict_=list()
        tasks=dict()
        for task in self.list:
            if isinstance(task,base_taskspec):
                tasks[task.id]=task.serialization()
        # dict_.append(tasks)

        connections=list()
        for task in self.list:
            if isinstance(task,base_taskspec):
                successors=list(self.list.successors(task))
                for successor in successors:
                    branch_index=-1
                    if isinstance(task,intent_identify_task_multi_branch):
                        branch_index = task.intents.index(get_key_by_value(task.branch,successor))
                    connections.append((dict({
                        "from": task.name,
                        "to": successor.name,
                        "branch":branch_index
                    })))
        return tasks,connections

    def deserialization(self):
        pass

def get_key_by_value(dict_:dict,value_):
    for key,value in dict_.items():
        if value == value_:
            return key
    return None
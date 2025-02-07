from Task.base_taskspec import base_taskspec 
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
    

    def connect(self,front:str,back:str):

        '''
        连接任务节点,未前后节点设置
        params:
        (str) name of tasks
            front -> back
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

    def is_DAG(self):
        return nx.is_directed_acyclic_graph(self.list)
    
    def serialization(self):
        pass
    
    def deserialization(self):
        pass


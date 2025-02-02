from Task.base_taskspec import base_taskspec 


class tasklist:
    '''
    使用id标识任务
    作为容器存储已创建的任务
    格式:
    {
        "task_id": task
    }
    '''
    def __init__(self):
        self.len=0
        self.list={}

    def add_task(self,task):
        '''
        add a task into the list
        params: the task

        '''
        if task.id in self.list:
            print("task exists int list already")
            return False
        self.list[task.id]=task
        return True
    
    def del_task(self,task):
        '''
        delete a task

        params:the task
        '''
        if task.id not in self.list:
            print("task does not exist")
            return False
        del self.list[task.id]
        return True
    
    def get_task_by_Id(self,id):
        '''
        search the task by id and return task
        return None if not exist
        params: id
        '''
        if id not in self.list:
            print(f"cannot find such task by id {id}")
            return None
        return self.list[id]
    
    def get_task_by_name(self,name):
        '''
        search by name
        params:name
        '''
        for task in self.list.values():
            if task.name == name:
                return task
        print(f"cannot find by name {name}")
        return None
    
    def get_task_by_type(self,type):
        '''
        return a list of tasks of the according type
        '''
        res=[]
        for task in self.list.values():
            if task.type==type:
                res.append(task)

        return res
    
    def tasks(self):
        '''
        show all tasks in the list
        and return the list if necessary
        '''
        for task in self.list.values():
            print("--task:")
            print(f"name: {task.name}")
            print(f"  id: {task.id}")
            print(f"type: {task.type}")
            print('-'*25)
        return self.list

    
    
    def serialization(self):
        pass
    
    def deserialization(self):
        pass


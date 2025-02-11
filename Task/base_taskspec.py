'''
基本的任务单元
    可执行任务类型的开发基础
    输入和输出使用名称引用
'''
from utils.id import get_task_id
from Task.TaskStatus import TaskStatus,taskstatus
from workflow.value_table import value_table
from workflow.value_status import valuestatus

class base_taskspec:

    def __init__(self,val_table:value_table,name=None):
        '''
        创建任务基本内容:
            val_table: 工作流的变量表
            name: 任务名称  默认为id前8位

        '''
        self.status=TaskStatus.ZERO
        self.id=get_task_id()
        self.name=name if name is not None else self.id[0:8]
        self.val_table=val_table
        #output初始拥有
        # self.outputs=[
        #     f"output_id_{self.id}"
        # ]
        # self.set_outputs()
        self.inputs=[]
        self.outputs=[]
    
    def run(self):
        raise NotImplementedError("run not implemented!")
    

    
    def cancel(self):
        '''
        turn the task into canceled status
        '''
        print("task canceled!")
        self.set_status("canceled")
    
    
    
    def get_status(self):
        return self.status
    


    def input_ready(self):
        '''
        check if all inputs are ready
        '''
        for input in self.inputs:
            input=self.val_table.values[input]
            if input["value"] is None or input["status"] is valuestatus.uninitialized:
                return False
        self.status=TaskStatus.READY
        return True
    
    def add_input(self,input):
        '''
        将value_table上的input绑定到task上
        input:the string of name of the value
        '''
        if input not in self.val_table.values:
            print(f"{input} add to table")
            self.val_table.add_value(input)

        self.inputs.append(input)
        return True

    def remove_input(self,input):
        '''
        删除指定的输入
        return True if succeed
        input: a str of the name of value
        '''
        # if input not in self.val_table.values:
        #     print(f"{input} does not exist in valueTable")
        #     return False
        if input not in self.inputs:
            print(f"{input} not in inputs")
            return False
        self.inputs.remove(input)
        return True
    


    def change_input(self,target,change):
        '''
        将绑定的变量替换为另外一个
        target: 要替换的目标    str
        change: 替换后的变量    str
        '''
        if target not in self.inputs:
            print(f"inputs dont have {target}")
            return False
        if target not in self.val_table.values or change not in self.val_table.values:
            print("valtable dont have both") 
            return False

        self.remove_input(target)
        self.add_input(change)
        return True


    def remove_output(self,output):
        '''
        删除设置的输出(任务的输出，不影响value_table)

        '''
        # if output not in self.val_table.values:
        #     print(f"{output} does not exist in valueTable")
        #     return False
        if output not in self.outputs:
            print(f"{output} not in outputs")
            return False
        self.outputs.remove(output)
        return True


    # def set_outputs(self):
    #     '''
    #     将task的所有output注册到value_table
    #     output: strings
    #     '''
    #     for output in self.outputs:
    #         if output not in self.val_table.values:
    #             self.val_table.add_value(output)
    #         else:
    #             continue
        
    def add_output(self,output):
        '''
        将value_table 上的output绑定到task上
        '''
        if output not in self.val_table.values:
            print(f"{output} add to table")
            self.val_table.add_value(output)

        self.outputs.append(output)
        return True

    def change_output(self,target,change):
        '''
        将绑定的变量替换为另外一个
        target: 要替换的目标    str
        change: 替换后的变量    str
        '''
        if target not in self.outputs:
            print(f"outputs dont have {target}")
            return False
        if target not in self.val_table.values or change not in self.val_table.values:
            print("valtable dont have both") 
            return False

        self.remove_output(target)
        self.add_output(change)
        return True

    def set_status(self,status:str):
        '''
        设置状态:
        params: (str)status 
        ZERO
        READY
        WAITING
        COMPLETED
        CANCELED
        RUNNING
        ERROR
        '''
        status=status.lower()

        status_dict={"zero":TaskStatus.ZERO,"ready":TaskStatus.READY,"waiting":TaskStatus.WAITING,"completed":TaskStatus.COMPLETED,"canceled":TaskStatus.CANCELED,"running":TaskStatus.RUNNING,"error":TaskStatus.ERROR}
        
        if status_dict[status] not in taskstatus:
            print("unknown status!")
            return False
        self.status=status_dict[status]

    def set_value(self,value_name,value):
        return self.val_table.set_value(value_name,value)

    def value(self,value_name):
        return self.val_table.get_value(value_name)


    '''
     状态判断
     is_ready
     is_completed
     is_canceled
    '''   


    def is_ready(self):
        return True if self.status == TaskStatus.READY else False
    
    def is_completed(self):
        return True if self.status == TaskStatus.COMPLETED else False
    
    def is_canceled(self):
        return True if self.status == TaskStatus.CANCELED else False
    

    


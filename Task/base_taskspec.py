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
            name: 任务名称

        '''
        self.status=TaskStatus.ZERO
        self.name=name
        self.id=get_task_id()
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
        self.status=TaskStatus.CANCELED
    
    
    
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
        return True
    
    def add_input(self,input):
        '''
        将value_table上的input绑定到task上
        input:the string of name of the value
        '''
        if input not in self.val_table.values:
            print(f"{input} does not exist")
            return False

        self.inputs.append(input)
        return True

    def remove_input(self,input):
        '''
        删除指定的输入
        return True if succeed
        input: a str of the name of value
        '''
        if input not in self.val_table.values:
            print(f"{input} does not exist in valueTable")
            return False
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
        删除设置的输出

        '''
        if output not in self.val_table.values:
            print(f"{output} does not exist in valueTable")
            return False
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
            print(f"{output} does not exist")
            return False

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

    def setstatus(self,status):
        if status not in taskstatus:
            print("unknown status!")
            return False
        self.status=status
            

    


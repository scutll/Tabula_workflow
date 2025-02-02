'''
基本的任务单元
    可执行任务类型的开发基础
    输入和输出使用名称引用
'''
from utils.id import get_task_id
from Task.TaskStatus import TaskStatus
from workflow.value_table import val_table
from workflow.value_status import valuestatus

class base_taskspec:

    def __init__(self,name=None):
        self.status=TaskStatus.ZERO
        self.name=name
        self.id=get_task_id()
        #output初始拥有
        self.outputs=[
            f"output_id_{self.id}"
        ]
        self.set_outputs()
        self.inputs=[]
    
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
            input=val_table.values[input]
            if input["value"] is None or input["status"] is valuestatus.uninitialized:
                return False
        return True
    
    def add_input(self,input):
        '''
        将value_table上的input绑定到task上
        input:the string of name of the value
        '''
        if input not in val_table.values:
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
        if input not in val_table.values:
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
        if target not in val_table.values or change not in val_table.values:
            print("valtable dont have both") 
            return False

        self.remove_input(target)
        self.add_input(change)
        return True


    def remove_output(self,output):
        '''
        删除设置的输出
        要删除outputs 和 val_table 上的
        '''
        if output not in self.outputs or output not in val_table.values:
            print("output do not exist")
            return False
        
        self.outputs.remove(output)
        val_table.del_value(output)
        return True


    def set_outputs(self):
        '''
        将task的所有output注册到value_table
        output: strings
        '''
        for output in self.outputs:
            if output not in val_table.values:
                val_table.add_value(output)
            else:
                continue
        
    def add_output(self,output_name):
        '''
        为task新建一个output,并注册到val_table
        '''
        if output_name in self.outputs or output_name in val_table.values:
            print(f"{output_name} exist already")
            return False

        self.outputs.append(output_name)
        val_table.add_value(output_name)
        return True

    def change_output(self,target,change):
        '''
        修改输出
        (跟改名类似)
        '''
        if target not in self.outputs:
            print(f"outputs dont have {target}")
            return False
        
        if change in val_table:
            print(f"{change} exists already")
            return False
        
        self.remove_output(target)
        self.add_output(change)
        return True

    

    


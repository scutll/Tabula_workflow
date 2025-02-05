from Task.TaskStatus import TaskStatus
from Task.base_taskspec import base_taskspec
from workflow.value_table import value_table

class start_task(base_taskspec):
    '''
    工作流的开始任务，接受用户的输入
    默认有一个输入(DEFAULT_START_INPUT)
    '''
    def __init__(self,value_table:value_table,name=None):
        super().__init__(value_table,name)
        self.type="start"
        self.val_table.add_value("DEFAULT_START_INPUT")
        self.add_input("DEFAULT_START_INPUT")

    
    def run():
        print("workflow starts:")
    
    


class end_task(base_taskspec):
    '''
    工作流的结束任务，将一些变量以一定方式组织成文本输出给用户
    '''
    def __init__(self,value_table:value_table,name=None):
        super().__init__(value_table,name)
        self.type="end"


        '''
        输出的组织形式：
            在outputs里找values
            values: 用到的变量
            content: 组织形式，使用f-string形式
        '''
        self.content={
            "values": [],
            "content":None
        }

    def set_content(self,content):
        '''
        设置输出格式，使用{变量名}做变量输出，此方法用于绑定要使用的变量名，
        到run方法里再替换为变量内容
        ''' 
        for input in self.inputs:
            if str("{"+input+"}") in content:
                self.content["values"].append(input)

        self.content["content"]=content
        pass



    def run(self):
        '''
        将content里的占位符替换为变量内容并输出
        并不改变content内容
        '''
        values=self.content["values"]
        content=self.content["content"]
        for val in values:
            replave_val=self.val_table.get_value(val) if self.val_table.get_value(val) is not None else ""
            content=content.replace(str("{"+val+"}"),replave_val)
        print(content)
        pass





class print_task(base_taskspec):
    '''
    只是简单的把input打印出来
    测试用
    '''
    def __init__(self,value_table=value_table,name=None):
        super().__init__(value_table,name)
        self.type="print"


    def run(self):
        print(f"running task{self.name} {self.id}")
        for input in self.inputs:
            input=self.val_table.get_value(input)
            print(input)
        print("-"*25)

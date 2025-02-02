from Task.TaskStatus import TaskStatus
from Task.base_taskspec import base_taskspec
from Task.tasklist import tasklist
from workflow.value_table import val_table

class start_task(base_taskspec):
    '''
    工作流的开始任务，接受用户的输入
    默认有一个输入(DEFAULT_START_INPUT)
    '''
    def __init__(self):
        super().__init__()
        self.type="start"
        val_table.add_value("DEFAULT_START_INPUT")
        self.add_input("DEFAULT_START_INPUT")
        self.next=[]
        self.before=[]
    
    def run():
        print("workflow starts:")
    
    


class end_task(base_taskspec):
    '''
    工作流的结束任务，将一些变量以一定方式组织成文本输出给用户
    '''
    def __init__(self,name=None):
        super().__init__()
        self.type="end"
        self.next=[]
        self.before=[]

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
            replave_val=val_table.get_value(val) if val_table.get_value(val) is not None else ""
            content=content.replace(str("{"+val+"}"),replave_val)
        print(content)
        pass





class print_task(base_taskspec):
    '''
    只是简单的把input打印出来
    测试用
    '''
    def __init__(self,name=None):
        super().__init__(name)
        self.type="print"
        self.next=[]
        self.before=[]

    def run(self):
        print(f"running task{self.name} {self.id}")
        for input in self.inputs:
            input=val_table.get_value(input)
            print(input)
        print("-"*25)

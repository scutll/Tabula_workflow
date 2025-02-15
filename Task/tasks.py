from Task.TaskStatus import TaskStatus
from Task.base_taskspec import base_taskspec
from workflow.value_table import value_table
from utils.llm_api import run_llm
from time import sleep

class start_task(base_taskspec):
    '''
    工作流的开始任务，接受用户的输入
    默认有一个输入(DEFAULT_START_INPUT)
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="start"

        self.add_input("DEFAULT_START_INPUT")
        self.add_output("DEFAULT_START_OUTPUT")
    
    def run(self):
        self.set_value(self.outputs[0],self.value(self.inputs[0]))
        self.set_status("completed")
    
    


class end_task(base_taskspec):
    '''
    工作流的结束任务，将一些变量以一定方式组织成文本输出给用户
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="end"
        self.output_limit=1
        # self.add_input("DEFAULT_END_INPUT")
        self.add_output("DEFAULT_END_OUTPUT")

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

        # for output in self.outputs:
        #     if str("{"+output+"}") in content:
        #         self.content["values"].append(output)

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
        self.set_value(self.outputs[0],content)
        self.set_status("completed")





class print_task(base_taskspec):
    '''
    只是简单的把input打印出来
    测试用
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="print"


    def run(self):
        print(f"running task{self.name} {self.id}")
        for input in self.inputs:
            input=self.val_table.get_value(input)
            print(input)
        print("-"*25)



class llm_task(base_taskspec):
    '''
    调用大模型的任务
    接受inputs组成的文本然后输出
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="llm"
        self.content=None
        self.input_content=None
        self.output_limit=1
        self.add_output(str(f"{self.name}_output"))


    def run(self):
        '''
        使用content的内容向大语言模型提问,获取输出到output
        '''
        sleep(20) #防止ai频率过快
        self.set_content(self.input_content)
        print("question: ",self.content)
        output=self.outputs[0]
        self.set_value(output,run_llm(self.content))
        self.set_status("completed")


    
    def set_input_content(self,content:str):
        '''
        设置工作流时使用,将之后要使用的格式存下来
        '''
        self.input_content=content

    def set_content(self,content:str):
        '''
        设置输出为一定格式如:
            {input1} is {input2},how to {input3}?
        寻找用到的input
        将{input} 替换为input在变量表中的实际内容
        将设置好的文本传递到content中
        '''
        tmp=content
        for input in self.inputs:
            replave_val=self.val_table.get_value(input) if self.val_table.get_value(input) is not None else ""
            if "{"+input+"}" in tmp:
                tmp=tmp.replace(str("{"+input+"}"),replave_val)
        self.content=tmp

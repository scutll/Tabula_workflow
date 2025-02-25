from Task.TaskStatus import TaskStatus
from Task.base_taskspec import base_taskspec
from workflow.value_table import value_table
from utils.llm_api import run_llm,run_ii
from time import sleep

class start_task(base_taskspec):
    '''
    工作流的开始任务，接受用户的输入
    默认有一个输入(name_input)
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="start"

        self.add_input(str(f"{self.name}_input"))
        self.add_output(str(f"{self.name}_output"))
    
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
        self.add_output(str(f"{self.name}_output"))

        '''
        输出的组织形式：
            在outputs里找values
            values: 用到的变量
            content: 组织形式，使用f-string形式
        '''
        self.output_content=str(f"{self.outputs[0]}")
        

    def set_output_content(self,content):
        '''
        设置输出格式，使用{变量名}做变量输出，此方法用于绑定要使用的变量名，
        到run方法里再替换为变量内容
        ''' 
        self.output_content=content


    def set_content(self,content:str):
        tmp=content
        for input in self.inputs:
            replave_val=self.val_table.get_value(input) if self.val_table.get_value(input) is not None else ""
            if "{"+input+"}" in tmp:
                tmp=tmp.replace(str("{"+input+"}"),replave_val)
        return tmp



    def run(self):
        '''
        将content里的占位符替换为变量内容并输出
        并不改变content内容
        '''
        content=self.set_content(self.output_content)
        self.set_value(self.outputs[0],content)
        print(self.value(self.outputs[0]))
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
        self.input_content=None
        self.output_limit=1
        self.add_output(str(f"{self.name}_output"))


    def run(self):
        '''
        使用content的内容向大语言模型提问,获取输出到output
        '''
        content=self.set_content(self.input_content)
        print("question: ",content)
        sleep(31) #防止ai频率过快
        output=self.outputs[0]
        self.set_value(output,run_llm(content))
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
        return tmp


class intent_identify_task(base_taskspec):
    '''
    意图识别任务，接受输入和条件，输送到大模型让ai识别用户想要进行哪一个分支
    如
    input:
        i am a big {input}
    if 
        it is a big dog
    else

    让ai去判断满不满足if的条件
    '''

    def __init__(self, val_table, name=None):
        super().__init__(val_table, name)
        self.type="itent_identiey"
        self.identify_content=None
        self.input_content=None
        self.if_=None
        self.add_output(str(f"{self.name}_output"))
        self.branch={
            "if":None,
            "else":None,
        }

    def set_if(self,if_:str):
        '''
        设置if的条件
        '''
        self.if_=if_

    def set_input_content(self,content):
        '''
        设置工作流时使用,将之后要使用的格式存下来
        '''
        self.input_content=content


    def set_content(self,content):
        '''
        设置输出为一定格式如:
            {input1} is {input2},how to {input3}?
        寻找用到的input
        将{input} 替换为input在变量表中的实际内容
        将设置好的文本传递到content中
        '''
        tmp=str(content)
        for input in self.inputs:
            replave_val=self.val_table.get_value(input) if self.val_table.get_value(input) is not None else ""
            if "{"+input+"}" in tmp:
                tmp=tmp.replace(str("{"+input+"}"),replave_val)
        return tmp
    
        
    def input_ready(self):
        if self.if_ is None:
            print("set if!")
            return False
        if self.input_content is None:
            print("set content!")
            return False
        return super().input_ready()


    '''
    if 和 else之间的选择
    通过取消另一个任务不运行来实现
    '''
    def pick_if(self):
        if_=self.branch["else"]
        if if_ is None:
            print("invalid else task to cancel!")
            return False
        if_.set_status("canceled")
        return True
    
    def pick_else(self):
        else_=self.branch["if"]
        if else_ is None:
            print("invalid if task to cancel!")
            return False
        else_.set_status("canceled")
        return True


    def connect(self,task,choice):
        if choice != "if" and choice != "else":
            print(choice,"is an invalid choice")
            return False
        self.branch[choice]=task
        return True


    def run(self):
        content=str({
            "content":self.set_content(self.input_content),
            "if":self.if_
            })
        print(content)
        sleep(30)
        output=self.outputs[0]
        result=run_ii(content)
        print(result)
        self.set_value(output,result)
        if "if" in result:
            self.pick_if()
        elif "else" in result:
            self.pick_else()
        else:
            print("fail to predict branch")
        self.set_status("completed")
from Task.TaskStatus import TaskStatus
from Task.base_taskspec import base_taskspec
from workflow.value_table import value_table
from utils.llm_api import run_llm,run_ii
from time import sleep
import asyncio
from collections import OrderedDict as odict
from globals.request import sendMsg
import re

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
    
    async def run(self):
        self.set_value(self.outputs[0],self.value(self.inputs[0]))
        self.set_status("completed")
    
    def serialization(self):
        return super().serialization()
    
    def deserialization(self, dict_,id):
        return super().deserialization(dict_,id)
         

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
        values_to_be_used = filter_value(content)
        
        # 添加content中必要的变量

        for value in values_to_be_used:
            if value not in self.inputs and self.val_table.in_table(value):
                self.add_input(value)
        


    def set_content(self,content:str):
        tmp=content
        for input in self.inputs:
            replave_val=self.val_table.get_value(input) if self.val_table.get_value(input) is not None else ""
            if "{"+input+"}" in tmp:
                tmp=tmp.replace(str("{"+input+"}"),replave_val)
        return tmp



    async def run(self):
        '''
        将content里的占位符替换为变量内容并输出
        并不改变content内容
        '''
        content=self.set_content(self.output_content)
        self.set_value(self.outputs[0],content)
        print(self.value(self.outputs[0]))
        self.set_status("completed")
        
        
        

    def serialization(self):
        dict_=super().serialization()
        dict_["output_content"]=self.output_content
        return dict_

    def deserialization(self, dict_,id):
        super().deserialization(dict_,id)
        # self.output_content=dict_["output_content"]
        self.set_output_content(dict_["output_content"])
        return True




class print_task(base_taskspec):
    '''
    只是简单的把input打印出来
    测试用
    '''
    def __init__(self,val_table:value_table,name=None):
        super().__init__(val_table,name)
        self.type="print"


    async def run(self):
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


    async def run(self):
        '''
        使用content的内容向大语言模型提问,获取输出到output
        '''
        content=self.set_content(self.input_content)
        print("question: ",content)
        await asyncio.sleep(31) #防止ai频率过快
        output=self.outputs[0]
        self.set_value(output,run_llm(content))
        self.set_status("completed")


    
    def set_input_content(self,content:str):
        '''
        设置工作流时使用,将之后要使用的格式存下来
        '''
        self.input_content=content
        values_to_be_used = filter_value(content)


        for value in values_to_be_used:
            if value not in self.inputs and self.val_table.in_table(value):
                self.add_input(value)


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
    
    def serialization(self):
        dict_=super().serialization()
        dict_["input_content"]=self.input_content
        return dict_

    
    def deserialization(self, dict_,id):
        super().deserialization(dict_,id)
        # self.input_content = dict_["input_content"]
        self.set_input_content(dict_["input_content"])
        return True
    

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
        self.type="intent_identify"
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


    async def run(self):
        content=str({
            "content":self.set_content(self.input_content),
            "if":self.if_
            })
        print(content)
        await asyncio.sleep(30)
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



class intent_identify_task_multi_branch(base_taskspec):
    '''
    意图识别任务，接受输入和条件，输送到大模型让ai识别用户想要进行哪一个分支
    如
    input:
        i am a big {input}
    intent1: 
        it is a big dog
    intent2:
        it is a cat
    intent3:
        it is a bag

    让ai去判断哪条分支比较合理的条件
    '''

    def __init__(self, val_table, name=None):
        super().__init__(val_table, name)
        self.type="intent_identify_plus"
        self.identify_content=None
        self.input_content=None
        self.intents=[]
        self.add_output(str(f"{self.name}_output"))
        self.branch=odict()

    def set_intent(self,intent:str):
        '''
        设置if的条件
        '''
        self.intents.append(intent)
    
    def del_intent(self,intent:str):
        if intent in self.intetns:
            self.intents.remove(intent)
        else:
            print(f"no intent as {intent}")

    def switch_intent(self,old,new):
        if old not in self.intents:
            print(f"no intent as {old}")
        self.intents.remove(old)
        self.set_intent(new)



    def set_input_content(self,content):
        '''
        设置工作流时使用,将之后要使用的格式存下来
        '''
        self.input_content=content
        values_to_be_used = filter_value(content)

        for value in values_to_be_used:
            if value not in self.inputs and self.val_table.in_table(value):
                self.add_input(value)


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
        if not self.branch_filled():
            print("branch not filled!")
            return False
        if self.input_content is None:
            print("set content!")
            return False
        return super().input_ready()


    def connect(self,task,choice:int):
        '''
        使用索引来搜索intent:
            添加intent并知道该intent的索引后才可以connect
        '''
        if choice >= len(self.intents):
            print(choice,"is an invalid choice")
            return False
        if  self.intents[choice] in self.branch and self.branch[self.intents[choice]] is not None:
            print("occupied branch!")
            return False
        self.branch[self.intents[choice]]=task
        return True

    def disconnect(self,choice):
        '''
        使用索引删除intent分支绑定的任务
        '''
        if choice >= len(self.intents):
            print(choice,"is an invalid choice")
            return False
        del self.branch[self.intents[choice]]
        return True


    def pick(self,choice:int):
        '''
        使用索引来选择intent
        '''
        if choice >= len(self.intents):
            print("invalid choice!")
            return False
        self.branch[self.intents[choice]].set_status("waiting")
        return True


    def intents_(self):
        '''
        展示所有intents选项及其索引
        '''
        res=str()
        for i, intent in self.intents:
            res += f"{i} : {intent}\n"
        print(res,end="")
        return str(res)

    def branch_filled(self):
        '''
        检测branch是否都有连接相应任务
        若是则return True
        否则打印未连接的分支并返回False
        '''
        filled = True
        for intent in self.intents:
            if intent not in self.branch or self.branch[intent] is None:
                filled = False
                print(f"branch {intent} not filled")
        return filled

    

    async def run(self):
        content={
            "content":self.set_content(self.input_content),
            "intents":self.intents
            }
        print(content)
        for task in self.branch.values():
            task.set_status("canceled")

        await asyncio.sleep(30)
        output=self.outputs[0]
        result=int(run_ii(content))
        print(result)
        self.set_value(output,result)
        if result < len(self.intents):
            self.pick(result)
        else:
            self.pick(0)
            print("fail to predict branch, randomly choose:")
        self.set_status("completed")


    def serialization(self):
        dict_=super().serialization()
        dict_["identify_content"]=self.identify_content
        dict_["input_content"]=self.input_content
        dict_["intents"]=self.intents
        
        return dict_
    
    def deserialization(self, dict_,id):
        super().deserialization(dict_,id)
        if "identify_content" not in dict_:
            dict_["identify_content"] = None
        self.identify_content, self.intents = dict_["identify_content"], list(dict_["intents"])
        self.set_input_content(dict_["input_content"])
        return True




def filter_value(content:str):
    return re.findall(r"\{(.*?)\}",content)


'''
块插入节点，可以设置插入的块类型
自身并不输出，但输出会被设置成response
'''
available_block_type = ["paragraph","header","math","input","checklist","list","code","table","button"]
format_insert = {
            "type":"insertBefore",
            "data":None,
            "blockType":None,
            "id":None
        }


class insert_after_block_task(base_taskspec):

    def __init__(self, val_table, name=None):
        super().__init__(val_table, name)
        self.block_type=None
        self.output_content = None
        self.target_block = None
        self.add_output(str(f"{self.name}_output"))

    async def send_insrt_info(self,data):
        response = await sendMsg(data)
        return response


    def set_target_block(self,target_block_id):
        self.target_block = target_block_id



    
class insert_paragraph(insert_after_block_task):

    def __init__(self, val_table, name=None):
        super().__init__(val_table, name)
        self.type="insert_paragraph"
        self.block_type = "paragraph"
        self.output_content = None


    def set_output_content(self,content):
        '''
        设置输出格式，使用{变量名}做变量输出，此方法用于绑定要使用的变量名，
        到run方法里再替换为变量内容
        ''' 
        self.output_content=content
        values_to_be_used = filter_value(content)
        
        # 添加content中必要的变量
        for value in values_to_be_used:
            if value not in self.inputs and self.val_table.in_table(value):
                self.add_input(value)
        


    def set_content(self,content:str):
        tmp=content
        for input in self.inputs:
            replave_val=self.val_table.get_value(input) if self.val_table.get_value(input) is not None else ""
            if "{"+input+"}" in tmp:
                tmp=tmp.replace(str("{"+input+"}"),replave_val)
        return tmp
    

    async def run(self):

        msg = format_insert
        msg["data"] = {"text":self.set_content(self.output_content)}
        msg["blockType"] = "paragraph"
        msg["id"] = self.target_block

        print("sending: ",msg)

        response = self.send_insrt_info(msg)
        self.set_value(self.outputs[0],response)
        return True

    def serialization(self):
        serial = super().serialization()
        serial["blcok_type"] = "paragraph"
        serial["output_content"] = self.output_content
        serial["target_block"] = self.target_block


    def deserialization(self, dict_, id=None):
        super().deserialization(dict_, id)
        self.block_type = dict_["block_type"]
        self.target_block = dict_["target_block"]
        self.output_content = dict_["output_content"]
'''
### blockspec
- block的定义，定义block的内容，功能，接口
	- Attri
		- name：块名称，默认为None
		- id ： 使用blck+uuid4标识
		- content： 块的内容（文字文本或其他内容的标识）
	- method：
        - get_content √
		- get_id：获得id √
		- set_name：修改块名称 x√
		- set_content: 修改块内容 x√
        - add_content: 追加块内容 x√
'''
from ..utils.id import get_block_id

class blockspec:
    def __init__(self,content=None,name=None):
        self.name=name
        self.content=content
        self.id=get_block_id()

    def get_id(self):
        '''
        get id for a certain block
        '''
        return self.id
    
    def set_name(self,name):
        '''
        set the block's name:
        params: a str for the name of block

        修改名称的同时要通知任务和blocklist修改名称
        '''
        self.name=name



    def set_content(self,new_content):
        '''
        set the block's content
        params: new content for block
        '''
        self.content=new_content



    def add_content(self,add_content):
        '''
        add content into back of origional content
        '''
        self.content+=add_content


    def get_content(self):
        '''
        return original content of content
        '''
        return self.content
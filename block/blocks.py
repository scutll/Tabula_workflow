'''
define certain type of blocks
    super: blockspec
    Attri:
        id
        certains
    method
        serialize
        deserialize
'''

'''
### blockspec
- block的定义，定义block的内容，功能，接口
	- Attri
		- name：块名称，默认为None
		- id ： 使用blck+uuid4标识
		- content： 块的内容（文字文本或其他内容的标识）
	- method：
		- get_id：获得id
		- set_name：修改块名称
		- set_content: 修改块内容
        - add_content: 追加块内容
		
'''
from block.blockspec import blockspec
from utils.id import get_block_id
from block.type import blocktype

class textblock(blockspec):
    def __init__(self,content=None,name=None):
        super().__init__(content,name)
        self.id=get_block_id()
        self.type=blocktype.text

    def content(self):
        '''
        return content of the block
        '''
        return self.content
    
    def get_content(self):
        return super().get_content()
    
    def set_content(self, new_content):
        '''
        set content for block
        '''
        super().set_content(new_content)

    def add_content(self, add_content):
        '''
        add content to block's original content
        '''
        super().add_content(add_content)
from blocks import *
import ordereddict
'''
- 使用一个OrderedDict记录创建且未被删除的块，带顺序
- BolckList
	- 应实现功能
		- 按id寻找块 √
		- 按块名词寻找块 √
		- 块的移动，调整顺序
			- 移动到指定块后面 √
		- 删除块 √
		- 添加块 √
		- 维护块的数量 √
'''
class blocklist:

    def __init__(self):
        '''
        create a blocklist
        '''
        self.block_list=ordereddict()
    
    def getblockbyId(self,id):
        if id in self.block_list:
            return self.block_list[id]
        else:
            print(f"cannot find by id: {id}")
            return None
        
    def getblockbyName(self,name):
        for block in self.block_list.values():
            if name==block.name:
                return block
        print("cannot find by name")
        return None
    

    def add_block(self,block):
        '''
        params: a block instance
        '''
        if block.id in self.block_list:
            print("id exists already")
            return False
        
        self.block_list[block.id]=block
        return True
    

    def remove_block(self,id):
        '''
        params: id of a block
        '''
        if id is not str:
            print('id is not a string')
            return False
        if id not in self.block_list:
            print("id not exist to delete")
            return False
        del self.block_list[id]
        return True
    
    
    def len(self):
        return len(self.block_list)
    

    def move_after(self,src,dest):
        '''
        move a block to the back of another
        if dest is None, src comes to the front
        params:
            src: block to be moved
            dest: to locate
        '''
        if src.id not in self.block_list:
            print("src block doesn't exist")
            return False
        if dest is not None and dest.id not in self.block_list:
            print("dest block doesn't exist")
            return False

        block=self.block_list.pop(src.id)
        tmp_list=list(self.block_list.items())

        target_index=next(i for i,(id_,_) in enumerate(tmp_list) if id_ == dest.id) if dest is not None else 0

        tmp_list.insert(target_index,(src.id,src))
        self.block_list=ordereddict(tmp_list)
        return True
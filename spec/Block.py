import uuid

'''
specification of blocks

    block_id  : to identify a block
    type      : to identify the type of block
    context   : what the user exactly write in the block


'''

class Blockspec_list:
    '''
    a list to store created block
    identify a blockspec with block_id
    '''

    def __init__(self):
        self.blockspecs={}
        self.blocks_num=0

    def exist(self,block_id):
        return True if block_id in Blockspec_List else False



    def add_blockspec(self,blockspec):
        if blockspec.block_id in self.blockspecs:
            print("block exists!")
        else:
            self.blockspecs[blockspec.block_id]=blockspec
            self.blocks_num +=1


    def del_blockspec(self,block_id):
        if block_id not in self.blockspecs:
            print("block does not exist!")
        else:
            self.blockspecs.pop(block_id)
            self.blocks_num-=1 
        

Blockspec_List=Blockspec_list()


class Blocktype:
    '''
    defines types of block
    '''


    Text="text"
    Checkout="checkout"

    

class Blockspec:
    '''
    specification of blocks

    block_id  : to identify a block
    type      : to identify the type of block
    context   : what the user exactly write in the block
    


    Del_blockspec        :delete a blockspec
    Create_blockspec     :create a blockspec
    Get_block_type   :return type of a block
    Get_block_context:return context of a block
    Set_block_context:set context of a block(add\delete\write)
    Serialization    :serialization to json or else
    Deserialization  :deserialization from json to a block
    '''
    
    def __init__(self,type=Blocktype.Text,context=""):
        self.type=type
        self.context=context
        self.block_id='bloc'+str(uuid.uuid4())

    def Get_block_type(self):
        return self.type

    def Get_block_context(self):
        return self.context
    
    def Serialization(self):
        pass

    def Deserialization(self):
        pass



def Create_blockspec(type=Blocktype.Text,context=""):
    '''
    create a blockspec:
    params:
        type: a Blocktype (default to be text)
        context:default to be null str

    return:
        the blockspec object
    '''
    block=Blockspec(type,context)
    print("creating block:")
    Blockspec_List.add_blockspec(block)
    return block



def Delete_blockspec(block_id):
    '''
    delete a block
    params: a block_id
    
    '''
    print("deleting block:")
    if block_id in Blockspec_List:
        Blockspec_List.del_blockspec(block_id)
    else:
        print("no such a block!")
    
'''
维护变量名及其名称映射的变量表
表形式:
{
    "value_name":{"value":value , "status":status}
}
'''
from workflow.value_status import valuestatus

class value_table:

    def __init__(self):
        self.values={}



    def add_value(self,value_name,value=None,status=valuestatus.uninitialized):
        '''
        add a value into table
        return True if succeed
        params:
            value_name: the name of value
            value: the actual value(None if an empty value)
        '''
        if value_name in self.values:
            print(f"{value_name} exists already!")
            return False
        self.values[value_name]={"value":value,"status":status}
        return True
    
    def add_const_value(self,value_name,value):
        '''
        add a const value into table
        return True if succeed
        '''
        if value_name in self.values:
            print(f"{value_name} exists already")
            return False
        self.values[value_name]={"value":value,"status":valuestatus.const}
        return True




    def del_value(self,value_name):
        '''
        delete a value from the table
        return True if succeed
        params:
        value_name
        '''
        if value_name not in self.values:
            print(f"{value_name} does not exist!")
            return False
        del self.values[value_name]
        return True
    
    def get_value(self,value_name):
        '''
        get the value from table(a copy)
        '''
        if value_name not in self.values:
            print(f"{value_name} does not exist")
            return None
        return self.values[value_name]["value"]
    
    def set_value(self,value_name,value_toset):
        '''
        set a value according to a name
        return True if succeed
        params:
        value_name: name of the value
        value_toset: the value you want to set to be
        '''
        if value_name not in self.values:
            print(f"{value_name} does not exist")
            return False
        if self.values[value_name]["status"] is valuestatus.const:
            print("fail to set an const value!")
        

        #类型转换
        '''
        val原始元素类型:
            str: 任意类型可转
            int/float: 数字/float或可转数字的字符串
            bool: 可转换为bool的
            其他:暂不支持
        '''
        val=self.values[value_name]["value"]
        if val is None:
            val=value_toset
        elif isinstance(val,str):
            val=str(value_toset)
        elif isinstance(val,(int,float)):
            if isinstance(value_toset,(int,float,bool)):
                val=value_toset
            elif isinstance(value_toset,str):
                if value_toset.isdigit():
                    val=float(value_toset)
                else:
                    print("value_toset cannot convert into digit")
                    return False
        elif isinstance(val,bool):
            val=bool(value_toset)
        else:
            print(f"value's type: {type(value_toset)} does not fit with original value:{type(val)}")
            return False

        self.values[value_name]["status"]=valuestatus.ready
        self.values[value_name]["value"]=val
        return True
    
    def set_value_name(self,old,new):
        '''
        在变量表里修改名称
        '''
        if old not in self.values:
            print(f"fail to find {old}")
            return False
        if new in self.values:
            print(f"{new} exists")
            return False
        
        self.add_value(new,self.get_value(old),self.values[old]["status"])
        self.del_value(old)

    def in_table(self,value:str):
        return value in self.values

    def deserialization(self):
        pass
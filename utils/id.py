'''
id related operations
'''
from uuid import uuid4


'''
get an id for block
'blck' + uuid4
'''
def get_block_id():
    return 'blck'+str(uuid4())



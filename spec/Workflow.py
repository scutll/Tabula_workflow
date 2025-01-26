import uuid
from spec.Task import *
'''
specificaltion of workflow
'''

class workflowstatus:
    '''
    Status of workflowspec:
        READY
        RUNNING
        FINISHED
    '''
    WAITING=0
    READY=1
    RUNNING=2
    FINISHED=4

class workflowspec:
    '''
    holds a list of task and manages the execution of tasks
    BUT HOW TO set the conditions and sequence of tasks 

    attri:
        workflow_id
        task_sequence: defines the sequence of how to run tasks
        status

    interface:
        add_taskspec
        del_taskspec
        cur_running_taskspec
        run
        start_task
        stop_task
        is_completed
        is_running
        Serialization/Deserialization
        view_workflow_spec
    '''

    def __init__(self,status=workflowstatus.WAITING):
        self.workflow_id = 'wofl'+str(uuid.uuid4())
        self.status=status
        self.task_sequence={}
    
    def add_taskspec(self):
        '''
        add one task to workflow
        '''
        pass

    def del_taskspec(self):
        '''
        delete one task in workflow
        '''

        pass


    def cur_running_taskspec(self):
        '''
        return task running currently
        '''
        pass

       
    def run(self):
        '''
        start workflow
        '''
        pass

    
    def start_task(self):
        '''
        start to run the task in workflow
        '''

        pass


    def stop_task(self):
        '''
        stop task currently working
        '''

        pass


    def is_completed(self):
        '''
        return True if workflow is finished
        '''

        pass


    def is_running(self):
        '''
        return True is workflow is running
        '''

        pass



    def Serialization(self):
        pass



    def Deserialization(self):
        pass


    def view_workflow_spec(self):
        '''
        show visualized connection of task in workflow
        '''

        pass



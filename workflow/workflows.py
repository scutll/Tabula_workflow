from workflow.workflow import *

class Workflows:

    def __init__(self):
        self.num_workflows = 0
        self.workflows = dict()

    def add_workflow(self,workflow:workflow):
        if workflow.id in self.workflows:
            print(f"workflow {workflow.name} exists already")
            return False
        self.workflows[workflow.id] = workflow
        self.num_workflows += 1
        return True

    def get_workflow(self,id:str):
        if id not in self.workflows:
            print(f"workflow {id} not exists")
        return self.workflows[id] if id in self.workflows else None
    
    def del_workflow(self,id:str):
        if self.get_workflow_id(id) is None:
            print(f"workflow {id} not exists")
            return False
        del self.workflows[id]
        return True
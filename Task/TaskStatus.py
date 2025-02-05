'''
Status of tasks
ZERO 0 被创建后放在tasklist,且工作流还未开始
READY  输入齐全可以运行
WAITING 等待输入齐全
COMPLETED 完成
RUNNING 运行中未完成
CANCELED 取消
ERROR 未正常取消或完成
'''

class TaskStatus:
    ZERO=0
    READY=1
    WAITING=2
    COMPLETED=4
    CANCELED=8
    RUNNING=16
    ERROR=32


taskstatus = {value for key, value in TaskStatus.__dict__.items() if not key.startswith("__")}
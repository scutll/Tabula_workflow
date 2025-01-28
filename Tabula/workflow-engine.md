## main 
使用websockets与前端通信，作为工作流引擎的主工作端
main通过调用创建工作流、设置工作流任务等接口运行对前端输入数据进行处理


# 工作流的实现
- 使用Workflow对象创建工作流
- 使用Task对象作为工作流的基本执行单元

## Workflow
- 管理Task列表和Task的执行顺序或关系，并管理当前工作流运行状态
- 如何实现Task的工作顺序设置、调换？
	- 节点通过连线连接，按照连线顺序和控制条件来设置顺序
	- 某个节点(Task)等待输入的变量全部被计算出且上一个节点已经运行完并输出才对输入进行处理

#### 可能需要的接口
- 添加任务
- 删除任务
- 连接任务
- 检查工作流构建是否合法
- 获取当前在执行的任务
- 开始工作流执行
- 停止工作流执行
- 工作流序列化/反序列化
- 查看Task之间的关系（浏览工作流）



## baseTask
- 作为工作流的执行单元，每个时刻执行一个任务
- 基本的任务类型，可以继承出不同用途的Task类型
- 包含基本内容：
	- 任务的执行状态
		- 输入齐全 READY
		- 等待上一个任务输出 WAITING
		- 完成 COMPLETED
		- 取消 CANCELED（不选取这个分支）
	- 任务的输入，输出列表（使用一定绑定机制）
- 需要一定的并发机制，等待其他任务完成后的输出作为该任务的输入（未计算出为None）


#### 可能需要的接口
- 检查任务运行状态
- 获取唯一id

## TaskSpec
- baseTask的具体类型，可以设计出拥有不同功能的多种TaskSpec
- 除拥有baseTask的基本内容外，拥有专属的性质与功能
	- 需要共有的内容：
		- id

#### 可能需要的接口
- 创建任务
- 设置输入
	- 添加输入
	- 指定输入
	- 将输入与上一个输出绑定
- 设置输出
	- 添加输出
	- 指定输出


## Trigger
- 触发器，不完全依赖于工作流，使用时间或事件触发
- 可以通过工作流设置一个触发器


#### 接口
- 创建触发器
- 删除触发器
- 设置触发器类型
1. 时间
	- 设置时间
		- 定时或一段时间后
2. 事件
	- 设置事件
- 设置触发执行事件
	- 调用接口
	- 调用大模型
- 设置输入输出
- 在输入流中加入触发器
- 序列化/反序列化






工作流创建的流程
- 块(Block)是编辑器单元，包含类型与内容，块id，可在块中嵌入工作流
- 为工作流设置任务（节点）：
	- 任务spec设置了关于操作块的基本内容（添加块，设置输入输出）
	- 创建包含块列表等信息的spec实例化MyTaskSpec
	- 使用Task来初始化，获得一个可以用来执行的Task对象


- 应该使用多种spec以构建不同类型的任务节点 （大模型、接口...）
- 如何标识设置的输入输出
- 判断条件应该使用什么，一个bool函数？
```Python
#创建包含块的Spec
class MyTaskSpec(if_TaskSpec):
	def __init__(self):
		super.__init__()
		self.setinput()
		self.setinput()
		
		##self.type=="if_condition"
		self.add_condition()
		self.add_condition()
		self.judg_condition.set("and")


		self.setoutput("output")
	...
#Spec实例化
task_spec=MyTaskSpec()

#创建可执行的任务
task=Task(task_spec)

```
- 使用任务组成工作流：
	- WorkflowSpec设置了有哪些任务以及任务之间的连接
	- 定义数据流的传输和处理逻辑
```python
#创建包含任务的spec
class MyWorkflowSpec(WorkflowSpec):
	def __init__():
		super().__init__
		self.start=StartTask()
		self.task1=task1
		self.task2=task2
		...
		self.end=()

		self.task1.connect(self.task2)
		self.task2.connect(self.end)
		...
		
#创建Spec实例
workflow_spec=MyWorkflowSpec()

#可实际执行的任务流
workflow=Workflow(workflow_spec)

```

- 前端设置工作流后将任务关系图（json or 其他）传输给后端，再通过任务关系图创建工作流对象
- 检查工作流格式是否正确，是否可执行
- 执行工作流
```Python
async def Workflow.run():
#逐个任务运行，每个任务运行前检查输入参数是否齐全
```









## block
- 文档内容的基本单元，包含块类型、内容等
- 块类型标识内容的作用（代码块，checkout_list、工作流 ...）
- 工作流可以嵌入块中，使用工作流影响块的内容


#### 可能用到的接口
- 创建块
- 删除块
- 获取块类型
- 获取块内容
- 修改块内容（追加、写入）
- 检查块内容类型
- 块序列化/反序列化

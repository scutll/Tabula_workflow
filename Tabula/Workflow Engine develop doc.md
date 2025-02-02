## **block**
- 设计编辑器块的定义、制作操作块的接口
- 每种块都有专属属性或功能
- blocklist用于维护所有已创建且未被删除的block

### blocklist
- 使用一个OrderedDict记录创建且未被删除的块，带顺序
- 使用块id匹配blocklist内容
- BolckList
	- 应实现功能
		- 按id寻找块
		- 按块名词寻找块
		- 块的移动，调整顺序
			- 移动到指定块后面
		- 删除块
		- 添加块
		- 维护块的数量
### blockspec
- block的定义，定义block的内容，功能，接口
	- Attri
		- name：块名称，默认为None
		- id ： 使用blck+uuid4标识
		- content： 块的内容（文字文本或其他内容的标识）
	- method：
		- get_id：获得id
		- set_name：修改块名称
		- get_content：返回原始内容
		- set_content: 修改块内容
		- add_content：追加块内容
### type
- block的类型
	- checkout
	- text
	- workflow
	- header1
	- header2
	- header3
	- header4

## blocks
- 定义多种继承自blockspec的block类型，细化其类型
	- Attri：
		- type
		- 专属属性
	- method：
		- 序列化
		- 反序列化
		- 专属方法
- CheckoutBlock
- WorkflowBlock
- TextBlock
- HeaderBlock



## **Task_spec**
- 设计多种类型的任务，在base的基础上衍生不同的功能
- 每一种spec都是用于创建实际Task对象的蓝图
- 使用tasklist维护已创建且未被删除的任务，工作流记录对任务的id引用，

### TaskStatus
- 任务状态类型
	- 输入齐全 READY
	- 等待上一个任务输出 WAITING
	- 完成 COMPLETED
	- 取消 CANCELED（不选取这个分支）
### base_Taskspec
- 基本的任务单元，包含任务的基本信息，是所有任务类型的开发基础
	- Attri：
		- taskstatus
		- outputs
		- inputs
		- name 任务名称
		- id task+uuid4
	- Methods：
		- run（父类不定义）
		- cancel 取消任务运行
	- input需要从table已有的变量中选
		- input_ready 检查输入是否全部齐全
		- status 获取当前状态
		- add_input 绑定输入
		- remove_input 删除已绑定的输入
		- change_input 将已绑定的输入替换为另一个输入
	- output创建时要绑定到table
		- remove_output 删除输出
		- set_outputs 绑定所有输出
		- add_output 绑定输出变量
		- change_output 替换输出变量
### tasks
- 设计各种任务类型
- 基本属性方法
	- Attri：
		- type 任务节点类型
		- next 任务后面连接的节点（列表）
		- before 任务之前连接的节点（列表）
	- Methods:
		- connect_ 连接任务
		- disconnect_ 解除连接
		- serialization 序列化
		- deserialization 反序列化
		- run 运行任务
- start_task
- end_task
- LLM_task
- print_task
- api_task
### tasklist
- 存储可使用的任务节点
- 使用id标识任务
- Attri：
	- len 任务数量
- Method：
	- add_task 添加任务
	- del_task 删除任务
	- get_task_by_Id 按id查找任务
	- get_task_by_name 按name查找任务
	- get_task_by_type 按类型查找任务
	- tasks 查阅所有已经添加的任务
	- serialization/deserialization 序列化/反序列化
	- 

## **Workflow_spec**
- 创建工作流的蓝图
	- current_task 现在正在运行的任务
	- show 展示任务连接关系，返回数据化形式的结构（给前端用）
	- conncet 连接任务用
	- disconnect 删除任务连接
	- check_ 检查是否满足运行格式
		- 怎么样的任务流是可运行的?
	- 使用一个networkx构建的有向图构建工作流
	- 初始化时就有start_task和end_task
### value_status
- 标记变量的使用状态
	- uninitialized 创建后未被初始化
	- ready 作为输入可使用
	- const 常量不可被修改
### value_table
- 变量表，维护可以被引用的变量，唯一变量名，Task使用变量名绑定变量
- 变量使用name，value(实际)，status等信息
- task使用name绑定自身inputs、outputs，修改的是table的value
	- Attri：
		- values 被记录的变量，未就绪的(除了设置好的)为None，
			- 变量类型：
			- int
			- float
			- str
			- bool
	- Methods：
		- set_value 按名字寻找变量并修改为指定值
		- add_value 添加变量
		- add_const_value 添加const变量
		- del_value 删除变量
		- get_value 获取变量值


## **Trigger**
- 触发器，设置按事件或按时间触发的任务


## **Utils**
- 实现模块，用于实现一些日志功能或序列化与反序列化功能
### id
- 为多种类型的单元获取id
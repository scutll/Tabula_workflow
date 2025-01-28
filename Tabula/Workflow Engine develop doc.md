## **block**
- 设计编辑器块的定义、制作操作块的接口
- 每种块都有专属属性或功能

### blocklist
- 使用一个OrderedDict记录创建且未被删除的块，带顺序
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
		- del_block: 删除块，将块移除出块列表
### type
- block的类型
	- checkout
	- normal
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
		- add_block:添加块，将块添加入块列表
		- 序列化
		- 反序列化
		- 专属方法
## **base_Taskspec**
- 基本的任务单元，包含任务的基本信息，是所有任务类型的开发基础

## **Task_spec**
- 设计多种类型的任务，在base的基础上衍生不同的功能
- 每一种spec都是用于创建实际Task对象的蓝图
## **Workflow_spec**
- 创建工作流的蓝图

## **Trigger**
- 触发器，设置按事件或按时间触发的任务


## **Utils**
- 实现模块，用于实现一些日志功能或序列化与反序列化功能
'''
标记变量的使用状态
	uninitialized 创建后未被初始化
	ready 作为输入可使用
	const 常量不可被修改
'''

class valuestatus:
    uninitialized=0
    ready=1
    const=2
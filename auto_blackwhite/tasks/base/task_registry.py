# Task Registry for managing and registering tasks in the application

class TaskRegistry:
    """注册表，管理所有 worker 任务"""
    _tasks = []
    
    @classmethod
    def register(cls, task_instance):
        cls._tasks.append(task_instance)
    
    @classmethod
    def get_all(cls):
        return cls._tasks
    
    @classmethod
    def start_all(cls):
        for task in cls._tasks:
            # 假设每个任务都有 start() 方法，或者直接 run_loop 在线程中启动
            # 实际启动逻辑在外部完成
            pass
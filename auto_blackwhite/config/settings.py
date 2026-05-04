# 全局配置（坐标、阈值、等待时间）
# config/settings.py
# 所有坐标、阈值、延时等配置集中在此

# 设备连接
DEVICE_ADDR = "127.0.0.1:5555"  # 雷电模拟器默认ADB地址

# 提神配置
TISHEN_CHECK_INTERVAL = 10  # 秒
TISHEN_CIRCLE_REGION = (100, 200, 150, 250)  # (left, top, right, bottom) 圆圈区域
TISHEN_CIRCLE_CLICK = (125, 225)  # 圆圈中心点击坐标
TISHEN_OPTIONS = [(100, 300), (100, 350)]  # 前两个提神选项的坐标

# 选天赋配置
TALENT_POSITIONS = [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]  # ABCD四个选项坐标
TALENT_SELECT_COUNT = 3  # 需要选3次

# 时间分配配置
TIME_ALLOC_BUTTON = (x, y)  # “时间分配”按钮坐标
WORK_TIME_SLIDER = (x, y)   # 工作时间滑块
WORK_TIME_TARGET = 4        # 目标工作时间
RESEARCH_PLUS_BUTTON = (x, y)  # 研究时间“+”号位置
MAX_CLICK_COUNT = 20        # 最大点击次数（防止无限循环）

# 规划队列检测
PLAN_QUEUE_BUTTON = (x, y)  # 规划队列按钮坐标
PLAN_QUEUE_CIRCLE_REGION = (left, top, right, bottom)  # 圆圈所在小区域

# 自我提升-活力研究
SELF_IMPROVE_BUTTON = (x, y)  # “自我提升”按钮
VITALITY_RESEARCH_REGION = (left, top, right, bottom)  # 活力研究等级数字区域
VITALITY_TARGET_LEVEL = 150

# 工作与科研
WORK_BUTTON = (x, y)          # “工作”按钮
RESEARCH_TAB = (x, y)         # “科研”标签

# 净收入
INCOME_REGION = (left, top, right, bottom)  # 净收入显示区域
INCOME_THRESHOLD = 500

# 雇佣研究助理
LIFE_BUTTON = (x, y)
EMPLOY_BUTTON = (x, y)
RESEARCH_ASSISTANT = (x, y)
EXPENDITURE_REGION = (left, top, right, bottom)  # 支出数字区域
TARGET_EXPENDITURE = 503

# 职位识别
POSITION_REGION = (left, top, right, bottom)  # 职位文字区域
# 职位等级阈值（研究主任）
DIRECTOR_LEVEL_THRESHOLD = 10

# 交通-防弹专用车
TRAFFIC_BUTTON = (x, y)
SCROLL_START = (x1, y1)   # 滑动起点
SCROLL_END = (x2, y2)     # 滑动终点
CAR_BUTTON_TEMPLATE = "images/防弹专用车.png"  # 模板图片路径

# 结算画面
SETTLEMENT_REGION = (left, top, right, top)  # 结算画面特征区域
SETTLEMENT_CLICK_POS = (x, y)  # 任意可点击坐标

# 全局等待时间
SHORT_WAIT = 0.5
MEDIUM_WAIT = 1.0
LONG_WAIT = 3.0
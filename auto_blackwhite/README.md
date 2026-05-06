# Auto Black & White

一个基于状态机和图像识别的自动化脚本，用于在 Android 模拟器（例如 LDPlayer）中自动执行游戏的流程。

## 概览

本项目通过 `uiautomator2` 控制模拟器设备，结合 `pytesseract` OCR 和 `opencv-python` 图像检测，构建了一套可自动执行游戏开局、时间分配、提神、招聘、职位检测及循环结算的机器人脚本。

脚本由两个核心部分组成：

- `main.py`：启动入口，负责连接设备、初始化控制器、启动提神线程和状态机主循环。
- `fsm/`：状态机实现，按游戏流程分类封装每个关键步骤。

## 主要功能

- 自动连接 Android 模拟器设备
- 自动点击选天赋、配置时间分配、启用规划队列
- 识别活力研究等级并循环升级至目标值
- 自动检查净收入并雇佣研究助理
- 识别职位并根据规则决定是否升级/等待结算
- 提神任务独立线程定时检测并完成提神流程
- 基于日志记录运行状态和错误信息

## 项目结构

```
auto_blackwhite/
  main.py
  README.md
  requirements.txt
  config/
    settings.py
    secrets.py.example
  core/
    connector.py
    controller.py
    recognizer.py
  fsm/
    context.py
    state_machine.py
    state.py
    states/
      start.py
      select_talent.py
      time_allocate.py
      check_plan_queue.py
      self_improve.py
      switch_to_work.py
      check_income.py
      hire_assistant.py
      check_position.py
      buy_car_and_upgrade.py
      wait_settlement.py
  tasks/
    tishen.py
    base_task.py
    watchdog.py
  utils/
    logger.py
```

## 依赖

- Python 3.8+
- uiautomator2
- opencv-python
- pillow
- pytesseract

可以通过以下命令安装依赖：

```bash
pip install -r requirements.txt
```

## 配置

核心配置位于 `config/settings.py`：

- `DEVICE_ADDR`：模拟器 ADB 地址，默认 `127.0.0.1:5555`
- `TISHEN_*`：提神检测与点击坐标
- `TALENT_POSITIONS`：选天赋的位置坐标
- `TIME_ALLOC_BUTTON`、`WORK_TIME_SLIDER`、`RESEARCH_PLUS_BUTTON`：时间分配与研究加号坐标
- `PLAN_QUEUE_BUTTON`、`PLAN_QUEUE_CIRCLE_REGION`：规划队列启用按钮和圆圈检测区域
- `SELF_IMPROVE_BUTTON`、`VITALITY_RESEARCH_REGION`、`VITALITY_TARGET_LEVEL`：活力研究相关配置
- `WORK_BUTTON`、`RESEARCH_TAB`：工作/科研切换按钮坐标
- `INCOME_REGION`、`INCOME_THRESHOLD`：净收入识别区域及阈值
- `LIFE_BUTTON`、`EMPLOY_BUTTON`、`RESEARCH_ASSISTANT`、`EXPENDITURE_REGION`：助理雇佣流程坐标与支出识别区域
- `POSITION_REGION`、`DIRECTOR_LEVEL_THRESHOLD`：职位识别区域与研究主任等级阈值
- `TRAFFIC_BUTTON`、`SCROLL_START`、`SCROLL_END`、`CAR_BUTTON_TEMPLATE`：交通界面购买车辆相关坐标和模板路径
- `SETTLEMENT_REGION`、`SETTLEMENT_CLICK_POS`：结算界面检测与点击位置

> 注意：坐标值在当前工程中大多为占位值，需要根据实际游戏界面截图和模拟器分辨率进行精准调整。

## 运行方式

在项目根目录运行：

```bash
python main.py
```

脚本启动后将执行以下主要流程：

1. 连接 Android 模拟器设备
2. 启动提神检测线程
3. 进入状态机主循环
4. 执行选天赋、时间分配、规划队列、自我提升、工作切换、净收入检查、雇佣助理、职位检测、买车升级、等待结算等步骤
5. 结算完成后循环回到初始状态

## 关键模块说明

### `core/connector.py`
负责使用 `uiautomator2` 连接设备，并在连接断开时重试。

### `core/controller.py`
提供带锁的点击、滑动、截图、像素读取和返回按键操作，确保多线程场景下的设备访问安全。

### `core/recognizer.py`
使用 `pytesseract` 和 `opencv` 做 OCR 数字识别、圆圈检测与职位文字识别。

### `fsm/state_machine.py`
实现游戏流程状态机，按名称管理状态对象，并执行状态迁移。

### `tasks/tishen.py`
独立线程定期检测提神机会并完成提神操作。

## 已知限制与改进方向

- 当前坐标多数为占位值，必须针对实际游戏界面进行标定。
- `TimeAllocateState`、`BuyCarAndUpgradeState`、`CheckPositionState` 等部分逻辑为框架形式，需补充具体界面识别与操作细节。
- `secrets.py.example` 目前为空，可用于扩展私有配置或 API 秘钥。
- 状态机中没有全局异常保护，建议后续加入更严格的错误恢复与超时处理。
- 推荐在 `GameController` 内进一步完善锁策略，避免状态机与提神线程产生并发冲突。

## 日志

日志输出通过 `utils/logger.py` 管理，写入 `logs/game.log`，同时输出到控制台。

## 贡献

如需扩展：

- 增加真实界面元素识别逻辑
- 补全更多游戏状态和异常处理
- 支持更多模拟器连接方式
- 添加单元测试和界面配准工具

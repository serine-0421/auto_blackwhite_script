# Auto Black & White 自动化脚本

一个基于状态机、图像识别和模拟器控制的游戏自动化项目，目标是在 Android 模拟器（如 LDPlayer）中自动执行游戏流程并完成核心操作。

## 特色

- 使用 `uiautomator2` 连接并控制 Android 模拟器
- 基于状态机 `GameStateMachine` 管理游戏流程和状态迁移
- `GameController` 提供带锁的点击、滑动、返回、截图和像素读取
- `Recognizer` 结合 `opencv-python` 与 `pytesseract` 实现数字 OCR、圆形检测和文本识别
- `TishenTask` 作为独立任务周期性检查并自动执行提神流程
- 日志输出到 `logs/game.log`，并同步打印到控制台

## 依赖

- Python 3.8+
- uiautomator2
- opencv-python
- pillow
- pytesseract

## 安装

建议使用虚拟环境：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r auto_blackwhite/requirements.txt
```

## 运行

在项目根目录执行：

```bash
python auto_blackwhite/main.py
```

运行后会：

1. 初始化日志系统
2. 连接 Android 模拟器
3. 启动提神任务线程
4. 启动状态机主循环

## 配置

主要配置位于 `auto_blackwhite/config/settings.py`：

- `DEVICE_ADDR`：ADB 设备地址
- `TISHEN_*`：提神检测区域、点击坐标和选项坐标
- `TALENT_POSITIONS`：选天赋的坐标列表
- `TIME_ALLOC_BUTTON` / `WORK_TIME_SLIDER` / `RESEARCH_PLUS_BUTTON`：时间分配界面坐标
- `PLAN_QUEUE_BUTTON` / `PLAN_QUEUE_CIRCLE_REGION`：规划队列入口和圆圈识别区域
- `SELF_IMPROVE_BUTTON` / `VITALITY_RESEARCH_REGION` / `VITALITY_TARGET_LEVEL`：自我提升与活力研究配置
- `WORK_BUTTON` / `RESEARCH_TAB`：工作与科研界面按钮位置
- `INCOME_REGION` / `INCOME_THRESHOLD`：净收入识别区域和阈值
- `LIFE_BUTTON` / `EMPLOY_BUTTON` / `RESEARCH_ASSISTANT`：雇佣助理流程所需坐标
- `POSITION_REGION` / `DIRECTOR_LEVEL_THRESHOLD`：职位识别区域和等级阈值
- `TRAFFIC_BUTTON` / `SCROLL_START` / `SCROLL_END` / `CAR_BUTTON_TEMPLATE`：买车升级界面参数
- `SETTLEMENT_REGION` / `SETTLEMENT_CLICK_POS`：结算界面检测和点击位置
- `SHORT_WAIT`, `MEDIUM_WAIT`, `LONG_WAIT`：全局等待间隔

> 注意：当前配置中的多数坐标为占位值，必须根据实际游戏界面和模拟器分辨率重新校准。

## 核心模块

### `auto_blackwhite/main.py`
入口脚本，负责初始化日志、连接设备、创建控制器与识别器、启动提神任务和状态机。

### `auto_blackwhite/core/connector.py`
设备连接管理模块，封装 `uiautomator2` 连接与重试逻辑，并支持 ADB 环境修复。

### `auto_blackwhite/core/controller.py`
基础控制模块，提供带锁的点击、滑动、返回、截图与像素读取，并加上重试机制。

### `auto_blackwhite/core/recognizer.py`
图像识别模块，负责 OCR 数字识别、圆形检测和文字识别。

### `auto_blackwhite/fsm/machine.py`
状态机引擎，负责注册状态、执行状态逻辑并进行状态迁移。

### `auto_blackwhite/tasks/tishen.py`
提神任务模块，实现独立轮询任务，自动识别并完成提神流程。

### `auto_blackwhite/utils/logger.py`
日志配置模块，支持环形日志文件与控制台输出。

## 项目结构

```
auto_blackwhite/
  main.py
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
    machine.py
    state.py
    states/
      growth/
        check_income.py
        check_plan_queue.py
        hire_assistant.py
        self_improve.py
      progression/
        buy_car_and_upgrade.py
        check_position.py
        switch_to_work.py
        wait_settlement.py
      startup/
        select_talent.py
        start.py
        time_allocate.py
      system/
  tasks/
    base_task.py
    tishen.py
    watchdog.py
  utils/
    logger.py
```

## 当前状态与改进点

- 已实现设备连接、控制器、识别器、状态机框架和提神任务
- 当前 `config/settings.py` 中坐标与识别区域仍为占位值，需要校准
- 识别逻辑依赖 `pytesseract` 与 `opencv-python`，建议在真实游戏界面中调试
- 需要补充更多状态执行逻辑、稳定性与异常恢复处理

## 使用建议

1. 安装并配置 `tesseract` OCR 引擎
2. 启动模拟器并确认 `adb connect <DEVICE_ADDR>` 成功
3. 调整 `auto_blackwhite/config/settings.py` 中的坐标与区域配置
4. 逐步运行并观察 `logs/game.log` 日志输出，定位问题

## 贡献

欢迎补充状态执行逻辑、增强识别算法、完善异常处理、添加测试及坐标校准工具。

# Auto Black & White 自动化脚本

一个基于状态机、图像识别和模拟器控制的游戏自动化项目，目标是在 Android 模拟器（如 LDPlayer）中自动执行游戏流程。
## 主要特点

- 通过 `uiautomator2` 连接和控制 Android 模拟器
- 采用状态机 `GameStateMachine` 管理游戏流程
- `GameController` 提供带锁的点击、滑动、截图与设备操作
- `Recognizer` 使用 `pytesseract` 和 `opencv-python` 做 OCR 数字识别、圆形检测与文字识别
- `TishenTask` 独立线程定时检查并自动完成提神
- 日志输出到 `logs/game.log`，支持文件和控制台双输出

## 目录结构

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

## 安装依赖

推荐使用虚拟环境后安装依赖：

```bash
pip install -r auto_blackwhite/requirements.txt
```

## 运行方式

在项目根目录运行：

```bash
python auto_blackwhite/main.py
```

脚本会执行：

1. 连接模拟器设备
2. 初始化 `GameController` 和 `Recognizer`
3. 启动 `TishenTask` 提神线程
4. 启动状态机主循环执行游戏流程

## 配置说明

核心配置在 settings.py 中管理，包括：

- `DEVICE_ADDR`：ADB 设备地址
- `TISHEN_*`：提神检测、点击区域与选项坐标
- `TALENT_POSITIONS`：选天赋坐标
- `TIME_ALLOC_BUTTON` / `WORK_TIME_SLIDER` / `RESEARCH_PLUS_BUTTON`：时间分配界面坐标
- `PLAN_QUEUE_BUTTON` / `PLAN_QUEUE_CIRCLE_REGION`：规划队列按钮与圆圈识别区域
- `SELF_IMPROVE_BUTTON` / `VITALITY_RESEARCH_REGION` / `VITALITY_TARGET_LEVEL`：活力研究相关配置
- `WORK_BUTTON` / `RESEARCH_TAB`：工作/科研按钮位置
- `INCOME_REGION` / `INCOME_THRESHOLD`：净收入识别区域与阈值
- `LIFE_BUTTON` / `EMPLOY_BUTTON` / `RESEARCH_ASSISTANT`：雇佣助理流程坐标
- `POSITION_REGION` / `DIRECTOR_LEVEL_THRESHOLD`：职位识别区域与等级阈值
- `TRAFFIC_BUTTON` / `SCROLL_START` / `SCROLL_END` / `CAR_BUTTON_TEMPLATE`：买车升级界面坐标和模板
- `SETTLEMENT_REGION` / `SETTLEMENT_CLICK_POS`：结算检测与点击位置
- 全局等待时间：`SHORT_WAIT`、`MEDIUM_WAIT`、`LONG_WAIT`

> 注意：当前坐标配置多为占位值，必须根据实际游戏界面和模拟器分辨率重新校准。

## 核心模块

### main.py
项目入口，负责：
- 初始化日志
- 连接设备
- 启动提神线程
- 启动状态机循环

### connector.py
负责连接模拟器设备，并在连接断开时自动重试。

### controller.py
提供：
- `click()`
- `swipe()`
- `press_back()`
- `screenshot()`
- `get_pixel_color()`

使用 `threading.RLock()` 和 `_safe_exec()` 进行线程安全执行与重试处理。

### recognizer.py
提供图像识别能力：
- 数字 OCR：`read_number()`
- 圆形检测：`has_circle()`
- 文本识别：`read_text()`

### machine.py
实现状态机：
- `GameStateMachine`
- 注册多个游戏状态
- 通过 `transition_to()` 执行状态迁移
- `run()` 进行主循环

### tishen.py
独立提神处理线程，周期性检查是否可提神并自动点击提神选项。

### logger.py
日志配置模块，使用 `RotatingFileHandler` 记录日志文件，同时输出控制台。

## 当前实现状态与改进点

- `GameController` 已实现线程安全执行与重试框架
- `Recognizer` 包含 OCR、圆圈检测、文字识别基础能力
- 状态机框架已搭建完毕，包含完整流程状态注册
- `TishenTask` 已实现提神周期检测与自动操作

待完善项：

- 需要校准所有坐标与识别区域
- 部分接口调用（如 `TishenTask` 的 `ocr_number` / `safe_click`）目前与 `Recognizer`/`GameController` 方法命名存在不一致，需要统一
- 需要补充具体界面识别与状态执行逻辑
- 建议补强异常恢复、超时处理和业务级重试

## 贡献建议

- 补全各状态的实际游戏操作逻辑
- 增加更稳定的图像识别与模板匹配
- 添加单元测试与流程回归测试
- 提供坐标标定工具或界面校对脚本
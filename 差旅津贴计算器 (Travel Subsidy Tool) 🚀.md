# 差旅津贴计算器 (Travel Subsidy Tool) 🚀

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/Romandora/travel_subsidy_tool)](https://github.com/Romandora/travel_subsidy_tool)

这是一个基于 Python 开发的轻量级图形化界面 (GUI) 工具，旨在帮助财务人员和出差员工快速准确地计算差旅补贴。

---

## 💡 功能亮点

- **智能匹配**：内置不同等级城市的补贴标准，一键计算。
- **离线使用**：支持打包为独立的 `.exe` 文件，无需安装 Python 即可在 Windows 上运行。
- **精准导出**：支持计算结果的实时显示，减少人工计算误差。

## 📦 下载与运行

### 对于普通用户 (无需安装编程环境)
1. 点击右侧的 [Releases](https://github.com/Romandora/travel_subsidy_tool/releases) 页面。
2. 下载最新的 `差旅津贴计算器.exe`。
3. **双击运行**即可开始计算。

### 对于开发者 (源码调试)
如果你希望在本地运行或修改代码，请确保已安装 **Python 3.10+**：

1.**克隆项目**

```bash
git clone [https://github.com/Romandora/travel_subsidy_tool.git](https://github.com/Romandora/travel_subsidy_tool.git)
cd travel_subsidy_tool
```

2.**安装依赖**

Bash

```
pip install -r requirements.txt
```

3.**启动程序**

Bash

```
python main_gui.py
```

------

## 🛠️ 构建 (Build) 说明

本项目使用 `PyInstaller` 进行打包。如果你修改了代码并想生成自己的 `.exe`，请运行：

Bash

```
# 生成单文件无后台终端的程序
pyinstaller --onefile --noconsole --name "差旅津贴计算器" main_gui.py
```

------

## 📂 项目结构

Plaintext

```
travel_subsidy_tool/
├── main_gui.py           # 程序主入口 (GUI 逻辑)
├── requirements.txt      # 项目依赖库清单
├── utils/                # 核心算法与工具类
├── .gitignore            # Git 忽略规则 (已配置忽略 build/dist)
└── README.md             # 项目说明文档
```

------

## 🤝 贡献与反馈

如果你在使用过程中发现 BUG 或有新的功能建议，欢迎：

1. 提交 [Issue](https://www.google.com/search?q=https://github.com/Romandora/travel_subsidy_tool/issues)
2. 发起 Pull Request

## 📄 开源协议

本项目基于 **MIT License** 协议开源。详情请参阅 [LICENSE](https://www.google.com/search?q=LICENSE) 文件。

------

**作者：** [Romandora](https://www.google.com/search?q=https://github.com/Romandora)

**项目地址：** [https://github.com/Romandora/travel_subsidy_tool](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/Romandora/travel_subsidy_tool)


#AI应用开发学习
一个为期5个月的AI应用开发系统学习记录，从python基础到AI agent开发。

## 📅 学习进度
| 周次 | 主题 | 状态 |
|------|------|------|
| Week 01 | Python 基础 + 工程化 | 进行中 |

## 📁 项目结构
ai-dev-journey/
├── week01/              # 第1周：Python 基础
│   ├── chat.py          # API 聊天程序（阿里云百炼）
│   ├── contacts.py      # 命令行通讯录
│   ├── employee.py      # 面向对象：Employee 类体系
│   └── log_analyzer.py # 日志分析器
├── requirements.txt     # Python 依赖
└── README.md           # 项目说明

## 环境准备
```bash
# 1. 创建 conda 环境
conda create -n ai-dev python=3.11 -y
conda activate ai-dev

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
# 在项目根目录创建 .env 文件，写入：
DASHSCOPE_API_KEY=你的阿里云百炼Key

##运行示例
# 运行通讯录
python week01/contacts.py

# 运行员工类演示
python week01/employee.py

# 运行日志分析器
python week01/log_analyzer.py

# 运行 API 聊天
python week01/chat.py

🛠️ 技术栈
Python 3.11
阿里云百炼 API（通义千问）
Git / GitHub
Conda 环境管理

📝 学习笔记
Python vs C++ 语法差异速查（整理中）
EAFP 异常处理思维
模块化与代码组织

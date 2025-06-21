# Python 后端与 AI Agent 使用说明

## 目录结构

```
scut_se_train_10086/
├── python_backend/         # FastAPI 后端服务与数据处理脚本
├── python_agent/           # AI Agent 及工具函数
│   ├── main.py             # Agent CLI 入口
│   ├── agent.py            # Agent 核心逻辑
│   ├── tools/              # 封装 API 的工具函数
│   ├── requirements.txt    # Agent 依赖
│   └── test_agent_from_env.py # 单元测试脚本（可选）
├── venv/                   # Python 虚拟环境
└── ...
```

---

## 一、如何启动 Python 后端服务

1. **进入项目根目录**

```bash
cd /Users/wuyutong/workspace/scut/scut_se_train_10086
```

2. **确保虚拟环境已创建并安装依赖**

```bash
python3 -m venv venv
./venv/bin/pip install -r python_backend/requirements.txt
```

3. **启动 FastAPI 后端服务**

```bash
./venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

> 注意：需在 `python_backend` 目录下执行，或指定 `api.main:app` 的相对路径。

---

## 二、如何启动和调用 AI Agent

1. **安装 Agent 依赖**

```bash
./venv/bin/pip install -r python_agent/requirements.txt
```

2. **配置 `.env` 文件**

在 `python_agent` 目录下创建 `.env` 文件，内容如下（请替换为你自己的模型服务信息）：

```
OPENAI_BASE_URL=https://你的Qwen模型API地址/v1
OPENAI_API_KEY=sk-xxxxxxx
LLM_MODEL=Qwen/Qwen2-72B-Instruct
```

3. **启动 Agent CLI**

```bash
./venv/bin/python python_agent/main.py
```

你会看到类似如下的欢迎界面：

```
--- 数据分析助手 ---
您好！我是您的数据分析助手，请问有什么可以帮您？
例如: '查一下区域 3747835140194172928 的人群构成' ...
输入 'exit' 或 'quit' 即可退出程序。
--------------------
您 >
```

直接输入自然语言问题，Agent 会自动调用后端 API 并用大模型总结结果。

---

## 三、`test_agent_from_env.py` 的意义

- 这是一个**自动化测试脚本**，用于验证 Agent 能否正确加载 `.env` 配置、调用后端 API 并获得 LLM 总结。
- 适合在开发/部署后做一次端到端自检。
- 运行方式：

```bash
./venv/bin/python python_agent/test_agent_from_env.py
```

- 你会看到 Agent 自动发起一次查询，并输出完整的 LLM 推理与 API 调用流程。

---

## 四、端到端流程总结

1. **数据生成与入库**：
    - 使用 Python 脚本模拟数据生成，写入 MySQL。
    - 离线脚本定时聚合，生成画像等统计表。
2. **后端服务**：
    - FastAPI 提供标准 RESTful API，供外部系统/Agent 查询。
3. **AI Agent**：
    - 通过自然语言理解用户意图，自动选择合适的 API 工具函数。
    - 调用后端 API 获取结构化数据。
    - 用大模型（如 Qwen）对数据进行总结、解释和自然语言输出。
4. **测试与验证**：
    - 可用 `test_agent_from_env.py` 做自动化端到端测试。
    - 也可用 CLI 交互式体验。

---

如有任何问题，欢迎随时联系开发者！ 
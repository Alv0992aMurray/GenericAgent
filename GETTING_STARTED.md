# 🚀 新手上手指南

> 完全没接触过编程也没关系，跟着做就行。Mac / Windows 都适用。
>
> 如果你已经有 Python 环境，直接跳到[第 2 步](#2-配置-api-key)。

---

## 1. 安装 Python

### Mac

打开「终端」（启动台搜索 "终端" 或 "Terminal"），粘贴这行命令然后回车：

```bash
brew install python
```

如果提示 `brew: command not found`，说明还没装 Homebrew，先粘贴这行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

装完后再执行 `brew install python`。

### Windows

1. 打开 [python.org/downloads](https://www.python.org/downloads/)，点黄色大按钮下载
2. 运行安装包，**底部的 "Add Python to PATH" 一定要勾上**
3. 点 "Install Now"

### 验证

终端 / 命令提示符里输入：

```bash
python3 --version
```

看到 `Python 3.x.x` 就 OK。Windows 上也可以试 `python --version`。

> ⚠️ **版本提示**：推荐 **Python 3.11 或 3.12**。不要使用 3.14（与 pywebview 等依赖不兼容）。
> 个人备注：我本地用的是 3.11.9，运行稳定，推荐优先选这个版本。

---

## 2. 配置 API Key

### 下载项目

1. 打开 [GitHub 仓库页面](https://github.com/lsdefine/GenericAgent)
2. 点绿色 **Code** 按钮 → **Download ZIP**
3. 解压到你喜欢的位置

### 创建配置文件

进入项目文件夹，把 `mykey_template.py` 复制一份，重命名为 `mykey.py`。

用任意文本编辑器打开 `mykey.py`，填入你的 API 信息。**选一种填就行**，不用的配置删掉或留着不管都行。

> ⚠️ **注意**：`mykey.py` 已被 `.gitignore` 排除，不会被提交到 Git，密钥安全。但如果你用其他方式同步文件（如云盘），注意不要把这个文件上传到公开位置。

### 配置示例

**最常见的用法：**

```python
# 变量名含 'oai' → 走 OpenAI 兼容格式 (/chat/completions)
oai_config = {
    'apikey': 'sk-你的密钥',
    'apibase': 'http://你的API地址:端口',
    'model': '模型名称',
}
```

```python
# 变量名含 'claude'（不含 'native'）→ 走 Claude 兼容格式 (/messages)
claude_config = {
    'apikey': 'sk-你的密钥',
    'apibase': 'http://你的API地址:端口',
    'model': 'claude-sonnet-4-20250514',
}
```

```python
# MiniMax 使用 OpenAI 兼容格式，变量名含 'oai' 即可
# 温度自动修正为 (0, 1]，支持 M2.7 / M2.5 全系列，204K 上下文
oai_minimax_config = {
    'apikey': 'eyJh...',
    'apibase': 'https://api.minimax.io/v1',
    'model': 'MiniMax-M2.7',
}
```

**使用标准工具调用格式（适合较弱模型）：**

```python
# 变量名同时含 'native' 和 'claude' → Claude 标准工具调用格式
native_claude_config = {
    'apikey': 'sk-ant-你的密钥',
    'apibase': 'https://api.anthropic.com',
    'model': 'claude-sonnet-4-20250514',
}
```

> 💡 还支持 `native_oai_config`（OpenAI 标准工具调用）、`sider_cookie`（Sider）等，详见 `mykey_template.py` 中的注释。

### 关键规则

**变量命名决定接口格式**（不是模型名决定的）：

| 变量名包含 | 触发的 Session | 适用场景 |
|-----------|---------------|---------|
| `oai` | OpenAI 兼容 | 大多数 API 服务、OpenAI 官方 |
| `claude`（不含 `native`） | Claude 兼容 | Claude API 服务 |
| `native` + `claude` | Claude 标准工具调用 | 较弱模型推荐，工具调用更规范 |
| `native` + `oai` | OpenAI 标准工具调用 | 较弱模型推荐，工具调用更规范 |

> 例：用 Claude 模型，但 API 服务提供的是 OpenAI 兼容接口 → 变量名用 `oai_xxx`。
> 例：用 MiniMax 模型 → 变量名用 `oai_minimax_config`，MiniMax 走 OpenAI 兼容接口。

**`apibase` 填写规则**（会自动拼接端点路径）：

| 你填的内容 | 系统行为 |
|-----------|----------|
| `http://host:2001` | 自动补 `/v1/chat/completions` |
| `http://host:2001/v1` | 自动补 `/chat/completions` |
| `http://host:2001/v1/chat/completions` | 直接使用，不拼接 |

---

## 3. 初次启动

终端里进入项目文件夹，运行：

```bash
cd 你的解压路径
python3 agentmain.py
```

这就是**命令行模式**，已经可以用了。你会看到一个输入提示符，直接打字发送任务即可。

试试你的第一个任务：

```
帮我在桌面创建一个 hello.txt，内容是 Hello World
```

> 💡 Windows 上如果 `python3` 不识别，换成 `python agentmain.py`。

---

## 4. 让 Agent 自己装依赖

Agent 启动后，只需要一句话，它就会自己搞定所有依赖：

```
请查看你的代码，安装所有用得上的 python 依赖
```

Agent 会自己读代码、找

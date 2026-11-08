# Commands

```shell
python3 -m venv venv
source venv/bin/activate

pip3 install -r ./requirements.txt
cp .env.example .env

jupyter-lab --no-browser
```

在本目录启动 Jupyter，这样 `bash` 的工作目录就是这个文件夹。`.env` 里填 `DEEPSEEK_API_KEY`。

# 这个例子做什么

`bash` 不是 DeepSeek 内置工具。notebook 把函数 schema 放进 `tools`，模型如果决定调用，就返回 `tool_calls`。notebook 再用 `bash -c` 在本机执行 `command`，把 stdout / stderr 以 `role: tool` 送回去，模型才写出最终回答。

命令超时 5 秒，输出超过 4000 字符会截断。模型给出的字符串会按当前用户权限执行。

# Ask Yamu DeepSeek API Setup

当前 Ask Yamu 已支持 DeepSeek API。`qa-metadata-v2.md` 和 `assets/qa-data.json` 会继续保留，作为 DeepSeek 的公开问答知识库和 API 不可用时的本地 fallback。

## 本地启动

在 `personal-ai-portfolio` 目录中设置环境变量并启动：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
$env:DEEPSEEK_MODEL="deepseek-v4-flash"
node server.js
```

然后打开：

```text
http://localhost:8787
```

不要再用 `file:///.../index.html` 测试 API 版本。直接打开 HTML 文件时，浏览器没有后端代理，Ask Yamu 会尝试访问 `http://localhost:8787/api/chat`，如果后端没启动就会回到本地预设问答。

## 线上部署提醒

API Key 不能写进 `app.js` 或 `index.html`。上线时需要把 `server.js` 改造成部署平台支持的后端接口，或部署到支持 Node 服务的平台，并在平台环境变量中配置：

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_MODEL`
- `DEEPSEEK_BASE_URL`

## 当前策略

- 三个推荐问题仍然优先展示固定回答，确保首页核心信息稳定。
- 用户在输入框自由提问时，优先调用 DeepSeek。
- 如果 DeepSeek 请求失败，会自动 fallback 到现有预设问答匹配。
- DeepSeek 的回答被限制在个人主页公开信息和问答知识库范围内，避免编造或展开未公开信息。

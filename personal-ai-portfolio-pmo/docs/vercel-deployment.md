# Vercel Deployment

当前项目已经准备好 Vercel 部署结构：

- 静态页面：`index.html`、`styles.css`、`app.js`、`assets/`
- DeepSeek 接口：`api/chat.js`
- 本地预览服务：`server.js`
- Vercel 配置：`vercel.json`

## 推荐部署流程

1. 把 `personal-ai-portfolio` 推送到 GitHub 仓库。
2. 登录 Vercel，选择 Add New Project。
3. 导入该 GitHub 仓库。
4. Framework Preset 选择 Other。
5. Build Command 留空。
6. Output Directory 留空。
7. 在 Environment Variables 添加：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

8. 点击 Deploy。

部署完成后，Vercel 会生成类似这样的访问链接：

```text
https://your-project-name.vercel.app
```

## 本地测试与线上测试的区别

本地测试：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
node server.js
```

访问：

```text
http://localhost:8787
```

线上测试：

```text
https://your-project-name.vercel.app
```

前端 `app.js` 会自动判断：

- 如果是 `file:///` 打开，会调用 `http://localhost:8787/api/chat`
- 如果是 Vercel 域名打开，会调用 `/api/chat`

## 注意事项

- 不要把真实 API Key 写入 `.env.example`、`app.js`、`index.html` 或任何 GitHub 可见文件。
- `.env` 已经被 `.gitignore` 忽略，可以用于本地保存密钥。
- `qa-metadata-v2.md` 继续保留，作为问答元数据源。
- `assets/qa-data.json` 会被 `api/chat.js` 读取，作为 DeepSeek 的公开问答知识库。

# Cloudflare Pages Deployment

如果 Vercel 在中国境内访问不稳定，可以把当前项目部署到 Cloudflare Pages。

## 项目结构

当前项目已经支持 Cloudflare Pages：

- 静态页面：`index.html`、`styles.css`、`app.js`、`assets/`
- Cloudflare API：`functions/api/chat.js`
- Vercel API：`api/chat.js`
- 本地测试服务：`server.js`

前端仍然请求：

```text
/api/chat
```

在 Cloudflare Pages 上，这个路径会由 `functions/api/chat.js` 处理。

## Cloudflare Pages 设置

在 Cloudflare Pages 里选择：

```text
Connect to Git
```

选择仓库：

```text
RohanaD-611/Codex-projects
```

构建设置：

```text
Framework preset: None
Root directory: personal-ai-portfolio/personal-ai-portfolio-pmo
Build command: 留空
Build output directory: .
```

如果 Cloudflare 界面要求填写 Build command，可以填：

```text
echo "No build step"
```

## 环境变量

在 Cloudflare Pages 的 Settings > Environment variables 里添加：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

建议 Production 和 Preview 都添加。

## 部署后测试

部署完成后，Cloudflare 会给你一个类似这样的链接：

```text
https://your-project.pages.dev
```

打开后测试：

1. 首页是否正常加载。
2. 右下角 Ask Yamu 是否能打开。
3. 输入自由问题，确认能调用 DeepSeek。
4. 如果回答 fallback，优先检查环境变量是否配置在 Production 环境。

## 注意事项

- 不要把真实 API Key 写入 GitHub。
- `functions/api/chat.js` 是 Cloudflare Pages 专用接口。
- `api/chat.js` 是 Vercel 专用接口，保留不影响 Cloudflare 部署。
- `server.js` 只用于本地测试。

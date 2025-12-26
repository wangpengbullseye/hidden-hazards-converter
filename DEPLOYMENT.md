# Streamlit应用部署指南

## 🚀 本地运行

### 1. 安装依赖

```bash
cd ToDataJson
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开：`http://localhost:8501`

---

## ☁️ 部署到Streamlit Cloud

### 1. 准备工作

确保你的项目包含以下文件：
- ✅ `app.py` - 主应用文件
- ✅ `requirements.txt` - 依赖列表
- ✅ `ToJson.py` - 转换工具
- ✅ `Validator.py` - 验证工具
- ✅ `煤矿采空区普查数据集Schema.json` - Schema定义

### 2. 上传到GitHub

```bash
# 初始化Git仓库
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit: 煤矿采空区数据集转换工具"

# 推送到GitHub
git remote add origin https://github.com/your-username/coal-mine-data-converter.git
git push -u origin main
```

### 3. 部署到Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的仓库和分支
5. 主文件路径设置为：`ToDataJson/app.py`
6. 点击 "Deploy"

等待几分钟，应用就会部署完成！

---

## 🐳 Docker部署

### 1. 创建Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. 构建镜像

```bash
docker build -t coal-mine-converter .
```

### 3. 运行容器

```bash
docker run -p 8501:8501 coal-mine-converter
```

访问：`http://localhost:8501`

---

## 📦 其他部署选项

### Heroku

1. 创建 `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. 部署:
```bash
heroku create your-app-name
git push heroku main
```

### AWS EC2

1. 启动EC2实例
2. 安装Python和依赖
3. 运行应用:
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Azure

使用Azure App Service部署Streamlit应用。

---

## ⚙️ 配置说明

### .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

### 环境变量

可以通过环境变量配置：

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 🔒 安全建议

1. **文件上传限制**
   - 限制文件大小（默认200MB）
   - 只接受CSV和JSON文件

2. **数据清理**
   - 及时清理临时文件
   - 不保存用户上传的数据

3. **HTTPS**
   - 生产环境使用HTTPS
   - Streamlit Cloud自动提供HTTPS

---

## 📊 性能优化

### 缓存

使用Streamlit缓存提高性能：

```python
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
```

### 文件大小限制

在 `.streamlit/config.toml` 中设置：

```toml
[server]
maxUploadSize = 200
```

---

## 🐛 故障排查

### 问题1: 模块导入错误

**解决**: 确保 `requirements.txt` 包含所有依赖

### 问题2: 文件上传失败

**解决**: 检查文件大小限制和格式

### 问题3: 端口被占用

**解决**: 更改端口
```bash
streamlit run app.py --server.port=8502
```

---

## 📞 技术支持

如有问题，请联系：
- GitHub Issues: [项目地址]
- Email: [联系邮箱]

---

**版本**: 1.0.0  
**更新日期**: 2024-12-26


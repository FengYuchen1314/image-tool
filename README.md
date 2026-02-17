# 🖼️ Image Tool 图片处理工具

一个简洁优雅的在线图片处理工具，支持批量上传、格式转换和图片压缩。

## ✨ 功能特性

- 📤 批量上传多张图片
- 🔄 支持格式转换：JPEG、PNG、WEBP、BMP（保留原格式）
- 📦 压缩质量可调
- 📥 单文件直接下载或批量打包下载
- 🌍 中英文双语支持

## 🚀 快速部署

### 前置要求

- Docker
- Docker Compose

### 部署步骤

1. **克隆仓库**

   ```bash
   git clone https://github.com/FengYuchen1314/image-tool.git
   cd image-tool
   ```

2. **启动服务**

   ```bash
   docker-compose up -d
   ```

3. **访问**

   浏览器打开：http://localhost:30050

## 📋 docker-compose.yml

```yaml
services:
  image-tool:
    build: .
    container_name: image-tool
    ports:
      - "30050:30050"
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

| 配置项 | 说明 |
|--------|------|
| ports:30050 | 访问端口，可自定义 |
| volumes:./uploads | 本地持久化文件夹 |
| restart:unless-stopped | 自动重启 |

## ☁️ 使用预构建镜像（即将支持）

如果你想直接使用预构建镜像（无需本地构建），请关注仓库更新。

## 🛠️ 本地构建（可选）

```bash
# 构建镜像
docker build -t image-tool .

# 运行容器
docker run -d -p 30050:30050 -v $(pwd)/uploads:/app/uploads image-tool
```

## 📱 在 NAS 上部署

1. 克隆仓库到 NAS 或上传所有文件
2. 在 NAS 的 Docker 界面创建项目/堆栈
3. 导入 docker-compose.yml
4. 映射端口 30050
5. 启动即可

## 📄 许可证

MIT License

# 图片处理工具 Docker 部署

## 快速启动

### 方式一：使用 Docker Compose（推荐）

```bash
docker-compose up -d
```

### 方式二：直接使用 Docker

```bash
# 构建镜像
docker build -t image-tool .

# 运行容器
docker run -d -p 30050:30050 -v $(pwd)/uploads:/app/uploads image-tool
```

## 访问

- 本地：`http://localhost:30050`
- NAS：`http://<你的NAS IP>:30050`

## 数据持久化

上传的图片保存在 `uploads` 文件夹中，映射到容器内 `/app/uploads`。

## 在 NAS 上部署

1. 上传项目文件夹到 NAS
2. 在 NAS 的 Docker 界面选择"导入"
3. 选择 docker-compose.yml 或构建 Dockerfile
4. 映射端口 30050
5. 启动即可

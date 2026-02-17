# 🖼️ Image Tool / 图片处理工具

[English](#english) | [中文](#中文)

---

## English

Online image processing tool, supports batch upload, format conversion and compression.

### Features

- Batch upload multiple images
- Format conversion: JPEG, PNG, WEBP, BMP, keep original format
- Adjustable compression quality
- Single file download or batch zip download
- Chinese/English bilingual support

### 🚀 Deployment

#### Python (Direct Run)

```bash
pip install -r requirements.txt
python app.py
```

Access: http://localhost:30050

#### Server (Docker)

```bash
git clone https://github.com/FengYuchen1314/image-tool.git
cd image-tool
docker-compose up -d
```

> ⚠️ Note: Pulling `python:3.11-slim` image may take some time depending on your network. Please be patient, the build will complete successfully.

Access: http://localhost:30050

#### NAS

1. Download project (ZIP or git clone)
2. Upload to NAS
3. Go to project directory in NAS file manager
4. Use NAS Docker/docker-compose to run docker-compose.yml

Access: http://<NAS IP>:30050

---

## 中文

在线图片处理工具，支持批量上传、格式转换、压缩。

### 功能

- 批量上传多张图片
- 格式转换：JPEG、PNG、WEBP、BMP、保持原格式
- 压缩质量可调
- 单文件下载或批量打包下载
- 中英文双语支持

### 🚀 部署

#### Python 直接运行

```bash
pip install -r requirements.txt
python app.py
```

访问：http://localhost:30050

#### 服务器 Docker 部署

```bash
git clone https://github.com/FengYuchen1314/image-tool.git
cd image-tool
docker-compose up -d
```

> ⚠️ 注意：首次拉取 `python:3.11-slim` 镜像可能需要一定时间（取决于网络状况），请耐心等待，构建一定会成功。

访问：http://localhost:30050

#### NAS 部署

1. 下载项目（ZIP 或 git clone）
2. 上传到 NAS
3. 在 NAS 文件管理器中进入项目目录
4. 使用 NAS 的 Docker/docker-compose 功能运行 docker-compose.yml

访问：http://<NAS IP>:30050

# 🖼️ Image Tool 图片处理工具

在线图片处理工具，支持批量上传、格式转换、压缩。

## 功能

- 批量上传多张图片
- 格式转换：JPEG、PNG、WEBP、BMP、保持原格式
- 压缩质量可调
- 单文件下载或批量打包下载
- 中英文双语支持

---

## Python 直接运行

```bash
pip install -r requirements.txt
python app.py
```

访问：http://localhost:30050

---

## 服务器 Docker 部署

```bash
git clone https://github.com/FengYuchen1314/image-tool.git
cd image-tool
docker-compose up -d
```

访问：http://localhost:30050

---

## NAS 部署

1. 下载项目（ZIP 或 git clone）
2. 上传到 NAS
3. 在 NAS 文件管理器中进入项目目录
4. 使用 NAS 的 Docker/docker-compose 功能运行 docker-compose.yml

访问：http://<NAS IP>:30050

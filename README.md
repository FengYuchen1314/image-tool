# 🖼️ Image Tool 图片处理工具

在线图片处理工具，支持批量上传、格式转换、压缩。

## 功能

- 批量上传多张图片
- 格式转换：JPEG、PNG、WEBP、BMP、保持原格式
- 压缩质量可调
- 单文件下载或批量打包下载
- 中英文双语支持

## 本地部署

```bash
git clone https://github.com/FengYuchen1314/image-tool.git
cd image-tool
docker-compose up -d
```

访问：http://localhost:30050

## NAS 部署

1. 克隆仓库或上传文件到 NAS
2. 进入目录
3. 运行：`docker-compose up -d`

访问：http://<NAS IP>:30050

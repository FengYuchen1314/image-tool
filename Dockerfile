FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 30050

CMD ["python", "app.py"]

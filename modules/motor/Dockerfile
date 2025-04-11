# ベースイメージとしてPythonを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libgpiod-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY modules/motor/motor.py .

# デフォルトのコマンドを設定
CMD ["python", "motor.py"]

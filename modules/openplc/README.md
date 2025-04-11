# OpenPLC Module

このディレクトリには、OpenPLCをDockerコンテナとして構築・実行するためのファイルが含まれています。

参考URL

https://qiita.com/MoriokaReimen/items/ba0451dbccd06a8788bc

## Dockerイメージのビルド

以下のコマンドを使用してDockerイメージをビルドします。

```bash
sudo docker compose build
```

## Docker Composeで実行

```bash
[almalinux@almalinux openplc]$ sudo docker compose up
WARN[0000] /home/almalinux/work/legofactory/modules/openplc/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 1/1
 ✔ Container openplc-openplc-1  Recreated                                                                                                                                                  0.0s 
Attaching to openplc-1
openplc-1  |  * Serving Flask app "webserver" (lazy loading)
openplc-1  |  * Environment: production
openplc-1  |    WARNING: Do not use the development server in a production environment.
openplc-1  |    Use a production WSGI server instead.
openplc-1  |  * Debug mode: off
openplc-1  |  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```



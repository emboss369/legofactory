# legofactory

## ラズパイ5

### ピン配置
https://www.sunfounder.com/blogs/news/comprehensive-guide-to-the-pin-diagram-of-raspberry-pi-5-understanding-gpio-pins-and-their-functions


## modules

### motor

sudo dnf install -y python3-pip
cd modules/motor/
pip install -r requirements.txt

https://qiita.com/kareki/items/41888b069cafa9d91939
sudo chmod 666 /dev/gpiochip*

python motor.py --test



Almalinuxにはgpioユーザーがないので作成


```sh
# gpio グループが存在するか確認・作成
sudo groupadd gpio


# 現在のユーザー（almalinux）を gpio グループに追加し、即時反映
sudo usermod -aG gpio $USER
newgrp 
# /dev/gpiochip* の権限とオーナーを一時変更
sudo chown root:gpio /dev/gpiochip*
sudo chmod 660 /dev/gpiochip*
# 永続設定（再起動しても維持するために udev ルール作成）
echo 'KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/99-gpiochips.rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# 設定後の確認
groups
ls -l /dev/gpiochip*

ここで gpio グループに入っていて、
/dev/gpiochip* が root gpio crw-rw---- になっていることを確認。

# sudo不要で実行できること
python3 motor.py --test
```

## OpenPLC

### AlmaLinux 9.3にDockerをインストール

https://higmasan.com/docker/install/install-docker-on-almalinux-9-3/

```sh
[almalinux@almalinux motor]$ dnf repolist | grep docker
[almalinux@almalinux motor]$ 
[almalinux@almalinux motor]$ sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
Adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
[almalinux@almalinux motor]$ dnf repolist | grep docker
docker-ce-stable                                          Docker CE Stable - aarch64
[almalinux@almalinux motor]$ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
[almalinux@almalinux motor]$ docker --version
Docker version 28.0.4, build b8034c0
[almalinux@almalinux motor]$ sudo systemctl start docker
[almalinux@almalinux motor]$ systemctl status docker
# ユーザをdockerグループに所属させる
[almalinux@almalinux motor]$ groups
almalinux adm systemd-journal gpio
[almalinux@almalinux motor]$ sudo usermod -aG docker $USER
[almalinux@almalinux motor]$ su - $USER
Password: 
[almalinux@almalinux ~]$ groups
almalinux adm systemd-journal docker gpio
[almalinux@almalinux openplc]$ docker compose version
Docker Compose version v2.34.0

```
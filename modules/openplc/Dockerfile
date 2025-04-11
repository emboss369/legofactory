FROM balenalib/raspberry-pi:buster


###########################################################################
# install dependency
###########################################################################
USER root
WORKDIR /root/
RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get -y install autoconf automake bison build-essential cmake flex git libtool make pkg-config python3-pip python2.7 sqlite3 sudo wget
RUN wget https://project-downloads.drogon.net/wiringpi-latest.deb && sudo dpkg -i wiringpi-latest.deb
RUN apt-get install -y python3-setuptools
RUN pip3 install flask==2.2.5 flask-login==0.6.2 pyserial pymodbus jinja2==3.0.3 itsdangerous==2.0.1 werkzeug==1.0.1
RUN sudo apt-get clean

###########################################################################
# install open plc
###########################################################################
# add openplc user
RUN useradd --create-home --shell /bin/bash openplc
RUN adduser openplc sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER openplc
WORKDIR /home/openplc

# compile and install open plc
RUN git clone -b development https://github.com/thiagoralves/OpenPLC_v3.git
WORKDIR /home/openplc/OpenPLC_v3
RUN sudo ./install.sh rpi
COPY config.ini etc/config.ini

###########################################################################
# configure exposed ports
###########################################################################
# HTTP port
EXPOSE 8080/tcp
# Modbus port
EXPOSE 502/tcp
# DNP3 port
EXPOSE 20000/tcp
# EtherNet/IP port
EXPOSE 44818/tcp

###########################################################################
# configure entry point
###########################################################################
# USER openplc
USER openplc
WORKDIR /home/openplc/OpenPLC_v3
CMD ["sudo", "./start_openplc.sh"]
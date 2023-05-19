FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y wget curl tar sudo ssh openssh-server rsync

# Download and extract Hadoop
RUN wget http://mirror.olnevhost.net/pub/apache/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz && \
    tar -xzvf hadoop-3.3.1.tar.gz && \
    mv hadoop-3.3.1 /opt/hadoop && \
    rm hadoop-3.3.1.tar.gz
#install java
RUN apt-get install -y openjdk-8-jdk vim
# Set environment variables
ENV HADOOP_HOME /opt/hadoop
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

#add config
#ADD config/* $HADOOP_HOME/etc/hadoop/
#RUN chmod +x $HADOOP_HOME/etc/hadoop/*

# Start SSH server
#CMD ["/usr/sbin/sshd", "-D"]
#RUN mkdir /var/run/sshd && \
#    echo 'root:password' | chpasswd && \
#    ssh-keygen -A

#RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
#    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
#    sed -i 's/#X11Forwarding yes/X11Forwarding yes/' /etc/ssh/sshd_config && \
#    sed -i 's/#X11UseLocalhost yes/X11UseLocalhost no/' /etc/ssh/sshd_config && \
#    sed -i 's/#UsePAM yes/UsePAM no/' /etc/ssh/sshd_config


# command bin/bash


RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys
# copy ssh config
#ADD ssh_configs/ssh_config /root/.ssh/config
#delete all tmp file: namenode, datanode
RUN rm -rf /tmp/*
#ADD start-ssh/* /
#RUN chmod +x /start-ssh.sh
# CMD bash /start-ssh.sh


#CMD ["/usr/sbin/sshd", "-D"]
#RUN /etc/init.d/ssh start
#CMD ["tail", "-f" ,"/dev/null"]

######## install spark
RUN apt-get install -y net-tools ca-certificates python3 #python3-pip
RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1
# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.3.2 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"


RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

#RUN . "/opt/spark/bin/load-spark-env.sh"

#expose port hadoop and spark
expose 9870 8088 9864 8080 9000 8032 50010 8042 19888 18080 4040 35371 43351 8888 33457
CMD ["tail", "-f" ,"/dev/null"]

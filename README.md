truoc het vo remove folder data
# bước 1:
bash start-ssh.sh
# bước 2: vào từng container
- namenode: /start-node/start-namenode.sh
- datanode: /start-node/start-datanode.sh  (vô từng datanode)
- resourcemanager: /start-node/start-resoucemanager
- vô lại từng datanode để run nodemanager: /start-node/start-nodemanager.sh

# spark
tạo thư mục /spark-logs
sbin/start-all.sh
bin/pyspark
muốn xem spark ui: sbin/....

# Hive
nhớ export HADOOP_VERSION=3.3.1
run command: hive
tải file jar bỏ vào spark/jars
command:

hdfs dfs -mkdir -p  /user/hive/warehouse
schematool -dbType postgres -initSchema
hive --service metastore

tạo database bằng hive trước, rồi viết câu query trên spark sau, lúc đó bảng tạo ra mới có ở trên hdfs

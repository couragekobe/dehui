# 当发生如下错误时
# Did you install mysqlclient or MySQL-python?

# 解决运行时无法安装 mysqlclient
# 需要使用pymysql

# 添加对pymysql 的支持
import pymysql

pymysql.install_as_MySQLdb()
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

SEX_CHOICES = (
    ('1', '男'),
    ('0', '女'),
)

# 定义用户的类型
USERTYPE = (
    (0, '开发管理员'),
    (1, '管理员'),
    (2, '卖家'),
    (3, '买家')
)

class User(AbstractUser):
    '''用户信息存储数据表， 如果要使用此数据表进行用户信息管理，需要在settings.py 中加入全局变量:
        AUTH_USER_MODEL = 'user.User'
        此类会从AbstrctUser,原auth_user下的 以下字段
        +--------------+--------------+------+-----+---------+----------------+
        | Field        | Type         | Null | Key | Default | Extra          |
        +--------------+--------------+------+-----+---------+----------------+
        | id           | int(11)      | NO   | PRI | NULL    | auto_increment |
        | password     | varchar(128) | NO   |     | NULL    |                |
        | last_login   | datetime(6)  | YES  |     | NULL    |                |
        | is_superuser | tinyint(1)   | NO   |     | NULL    |                |
        | username     | varchar(150) | NO   | UNI | NULL    |                |
        | first_name   | varchar(30)  | NO   |     | NULL    |                |
        | last_name    | varchar(30)  | NO   |     | NULL    |                |
        | is_staff     | tinyint(1)   | NO   |     | NULL    |                |
        | is_active    | tinyint(1)   | NO   |     | NULL    |                |
        +-------------- 以下为后派生的字段 -----+-----+---------+----------------+
        | date_joined  | datetime(6)  | NO   |     | NULL    |                |
        | nickname     | varchar(30)  | YES  |     | NULL    |                |
        | mobile       | varchar(13)  | NO   | UNI | NULL    |                |
        | email        | varchar(254) | YES  | UNI | NULL    |                |
        | sex          | varchar(10)  | YES  |     | NULL    |                |
        | is_delete    | tinyint(1)   | NO   |     | NULL    |                |
        | usertype     | int(11)      | NO   |     | NULL    |                |
        +--------------+--------------+------+-----+---------+----------------+
    '''
    # headp = models.ImageField('头像', upload_to='headphoto', default='/headphoto/touxiang.png', null=False, blank=True)
    nickname = models.CharField('昵称', max_length=30, null=True, blank=True)
    mobile = models.CharField("手机号", max_length=13, null=False, unique=True)
    email = models.EmailField("邮箱", null=True, unique=True)
    sex = models.CharField('性别', max_length=10, null=True, blank=True, choices=SEX_CHOICES, default='1')
    is_delete = models.BooleanField("是否禁用", default=False)
    usertype = models.IntegerField("用户类型",choices=USERTYPE,default=3)
    # create_time = models.DatetimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']

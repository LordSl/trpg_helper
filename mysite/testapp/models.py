from django.db import models

# Create your models here.
class TRPGHelper(models.Model):

    # 选项
    # null 是否允许为空
    # blank 是否允许为空白
    # db_column 列名
    # db_index 是否创建索引
    # default 默认值
    # primary_key 是否为主键
    # unique 是否只允许唯一值

    id = models.AutoField(db_column='id', primary_key=True)

    userName = models.CharField(default='\0', unique=True, max_length=256)

    state = models.CharField(default='\0', max_length=256)

    roomName = models.CharField(default='\0', max_length=256)


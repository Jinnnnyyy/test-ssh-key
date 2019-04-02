from django.db import models

# Create your models here.
# 商品类别
class Types(models.Model):
    # 类别名称
    name = models.CharField(max_length=32)
    # 父类目id
    pid = models.IntegerField(default=0)

    path = models.CharField(max_length=255)

    class Meta:
        db_table = "myweb_type"  # 更改表名
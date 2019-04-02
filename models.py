#coding=utf-8
from django.db import models
# Create your models here.
# 用户信息
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    ushou=models.CharField(max_length=20)
    # 这里的default和blank是python层面的默认值，不影响数据库，只有更改到了数据库，才需要迁移
    uaddress=models.CharField(max_length=100,default='')
    uyoubian=models.CharField(max_length=5,default='')
    uphone=models.CharField(max_length=11,default='')
    uid=models.IntegerField(default=1)
    code = models.CharField(max_length=6)

    class Meta():
        db_table='userinfo'
    def toDict(self):
        return {'id': self.id, 'username': self.uname,  'password': self.upwd}
    # 订单信息
class OrderInfo(models.Model):
    oid=models.CharField(max_length=20,primary_key=True)
    # 购买者
    user=models.ForeignKey('UserInfo')
    # 添加时间,默认添加时间，不可以修改
    odate=models.DateTimeField(auto_now=True)
    # 订单状态，是否支付，默认为否，实际中，可以定义为int，支付，未支付，已发货等等
    oIspay=models.BooleanField(default=False)
    # 订单金额
    ptotal=models.DecimalField(max_digits=6,decimal_places=2)
    # 订单收货人
    orecive=models.CharField(max_length=5)
    # 订单地址
    oaddress=models.CharField(max_length=29)
    # 电话
    ophone=models.CharField(max_length=11,default='')
    # 邮编
    oyoubian=models.CharField(max_length=5,default='')
    class Meta():
        db_table='orderinfo'
# 商品模型类
class GoodsInfo(models.Model):
    typeid = models.IntegerField()
    typename=models.CharField(max_length=32)
    goods = models.CharField(max_length=32)
    company = models.CharField(max_length=50)
    descr = models.TextField()
    price = models.FloatField()
    picname = models.CharField(max_length=255)
    state = models.IntegerField(default=1)
    store = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.DateField()

    class Meta:
        db_table = "goods_info"  # 更改表名
    def toDict(self):
        return {'id':self.id,'goods':self.goods,'price':self.price,'picname':self.picname}
# 订单详情模型类
class OrderDetailInfo(models.Model):
    goods=models.ForeignKey(GoodsInfo)
    order=models.ForeignKey(OrderInfo)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    count=models.IntegerField()
    class Meta():
        db_table = 'orderdetailinfo'
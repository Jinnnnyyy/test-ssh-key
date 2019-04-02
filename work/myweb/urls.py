"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from myweb import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^user_log/$',views.log,name='log'),
    url(r'^userinfo_handle/$',views.userinfo_handle1,name='userinfo_handle'),
    url(r'^user_register/$',views.register,name='register'),
    url(r'^register_handle/$',views.register_handle,name='register_handle'),
    url(r'^user_regist_exist/$',views.regiset_exist,name='user_regist_exist'),
    url(r'^user_logout/$',views.logout,name="user_logout"),
    # 添加购物车
    url(r'^cartadd/(?P<gid>[0-9]+)$',views.addCart,name='cart_add'),
    # 删除购物车
    url(r'^delcart/$',views.defcart,name='cart_del'),
    # 清空购物车
    url('^clearcart/$',views.cartclear,name='cart_clear'),
    # 查看购物车
    url(r'^cartinfo/$',views.cartinfo,name='cart_info'),
    url(r'^cartchange/$',views.cartchange,name='cart_change'),
    # 用户中心
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_center_order/$',views.user_center_order,name='user_center_order'),
    url(r'^user_center_site/$',views.user_center_site,name='user_center_site'),
    # 列表信息处理
    url(r'list/$',views.listinfo,name='list_info'),
    # 详情页处理
    url(r'detail/$',views.detailinfo,name='detail_info'),
    # 订单处理
    url(r'^ordersadd/$',views.ordersadd,name='order_add'),
    url(r'^ordersconfig/$',views.ordersconfig,name='order_config'),
    url(r'^orderinsert/$',views.ordersinsert,name='order_insert')
]

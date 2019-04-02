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
from myadmin import views

urlpatterns = [
    url(r'^$', views.welcome,name='admin_welcome'),
    url(r'help/$',views.help,name='admin_hple'),
    url(r'afterset/$',views.afterset,name='admin_afterset'),
    # 登录
    url(r'login/$',views.log,name='admin_login'),
    url(r'verify/$', views.verifycode, name='admin_verify'),
    url(r'verify/([0-9]+)',views.verifycode,name='admin_verify'),
    url(r'doLogin/$',views.dolog,name='admin_dolog'),
    url(r'logout/$',views.logout,name='admin_logout'),
    # 会员信息管理
    url(r'user_manage/$', views.user_manage, name='admin_user_manage'),
    url(r'user_add/$',views.user_add,name='admin_user_add'),
    url(r'add_user/$', views.add_user, name='admin_add_user'),
    url(r'update_user/(?P<id>[0-9]+)$', views.update_user, name='admin_update_user'),
    url(r'update_user_conf/(?P<id>[0-9]+)$', views.update_user_conf, name='admin_update_user_conf'),
    url(r'del_user/(?P<id>[0-9]+)$', views.del_user, name='admin_del_user'),
    # 商品类别管理
    url(r'scan_goods_kind/(?P<pindex>[0-9]*)$',views.scan_goods_kind,name='admin_scan_goods_kind'),
    # url(r'add_goods_kind/$',views.add_goods_kind,name='admin_add_goods_kind'),
    url(r'add_goods_kind/(?P<tid>[0-9]+)$', views.add_goods_kind, name="admin_add_goods_kind"),
    url(r'goods_kind_insert/$', views.goods_kind_insert, name="admin_goods_kind_insert"),
    url(r'goods_kind_del/(?P<tid>[0-9]+)$', views.goods_kind_del, name="admin_goods_kind_del"),
    url(r'goods_kind_edit/(?P<tid>[0-9]+)$', views.goods_kind_edit, name="admin_goods_kind_edit"),
    url(r'goods_kind_update/(?P<tid>[0-9]+)$', views.goods_kind_update, name="admin_goods_kind_update"),
    # 商品信息管理
    url(r'goods_info/(?P<pindex>[0-9]*)$',views.goods_info,name='admin_goods_info'),
    url(r'goods_set/$',views.goods_set,name='admin_goods_set'),
    url(r'goods_info_insert/$', views.goods_info_insert, name="admin_goods_info_insert"),
    url(r'goods_info_del/(?P<gid>[0-9]+)$', views.goods_info_del, name="admin_goods_info_del"),
    url(r'goods_info_edit/(?P<gid>[0-9]+)$', views.goods_info_edit, name="admin_goods_info_edit"),
    url(r'goods_info_update/(?P<gid>[0-9]+)$', views.goods_info_update, name="admin_goods_info_update"),
    # 订单信息管理
    url(r'new_order/$',views.new_order,name='admin_new_order'),
    url(r'old_order/$', views.old_order, name='admin_old_order'),

    #搜索查询
    url(r'goods_search/(?P<pindex>[0-9]*)$',views.goods_search,name='myadmin_goods_search')




]

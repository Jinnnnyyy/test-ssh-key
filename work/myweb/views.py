from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from myweb.models import UserInfo,OrderInfo,OrderDetailInfo,GoodsInfo
from hashlib import md5
from myweb.models import *
from myadmin.models import Types
import datetime
# Create your views here.
# 加载公共信息
def loadinfo(request):
    kind = Types.objects.filter(pid=0)
    return kind
def index(request):
    kind = loadinfo(request)
    user = request.session.get('userinfo', '登录')
    context = {'user': user, 'kind': kind}
    return render(request, 'myweb/index.html', context)


# 登录
def log(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request,'myweb/login.html',context)
# 处理登录信息
def userinfo_handle1(request):
    post=request.POST
    name = post.get('username')
    print(name)
    pwd = post.get('pwd')
    print(pwd)
    m1=md5()
    m1.update(bytes(pwd,encoding="utf8"))
    pwd1=m1.hexdigest()
    try:
        user=UserInfo.objects.get(uname=name)
        if user.upwd==pwd1:
            request.session['userinfo']=user.toDict()
            return  redirect('/')
        else:
           context={'name':name,'pwd':'密码错误'}
    except:
        print('user not exist')
        context = {'name': '账号不存在', 'pwd': ''}
    return render(request, 'myweb/login.html', context)

def userinfo_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    # filter返回的是一个列表对象，如果没有结果，返回空列表，不报错
    # get返回的是一个对象，如果没有查到值，会报错
    user=UserInfo.objects.filter(uname=uname)
    print(len(user))
    print(user[0].uname)
    if len(user)==1:
        m=md5()
        m.update(bytes(upwd,encoding='utf8'))
        if m.hexdigest()==user[0].upwd:
            red=HttpResponseRedirect('/user_center_info/')
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                # max_age设置coolie的过期时间，-1马上过期，时间是秒
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=user[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname,'upwd':upwd}
            return render(request,'myweb/login.html',context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'myweb/login.html', context)
# 退出
def logout(request):
    del request.session['userinfo']
    return redirect('/')

# 注册
def register(request):
    return render(request,'myweb/register.html')
# 处理注册信息
def register_handle(request):
    # 接收前台的数据
    post=request.POST
    name=post.get('user_name')
    pwd=post.get('pwd')
    cpwd=post.get('cpwd')
    email=post.get('email')
    # allow=post.get('allow')
    # 判断两次密码是否一致
    if pwd!=cpwd:
        return redirect('/user_register/')
    # 密码加密
    s1=md5()
    s1.update(bytes(pwd, encoding="utf8"))
    upwd1=s1.hexdigest()
    # 创建对象
    user=UserInfo()
    user.uname=name
    user.upwd=upwd1
    user.uemail=email
    user.save()
    return redirect('/user_log/')
# 判断用户是否存在，前台ajax请求
def regiset_exist(request):
    name=request.GET['user_name']
    # 获取用户名，从数据库中查询，只需要统计是否有相同名字的用户即可
    count=UserInfo.objects.filter(uname=name).count()
    print(count)
    return JsonResponse({'count':count})
# 列表信息处理
def listinfo(request):
    kind = loadinfo(request)
    tid=int(request.GET.get('tid',0))
    # k1=kind.filter(id=tid)
    lists=GoodsInfo.objects.filter()
    if tid>0:
        lists=lists.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
    context={'goodlist':lists,'kind':kind}
    # 获取对应的类别对象信息
    k1 = kind.filter(id=tid)
    ty={'id':tid,'name':k1[0].name}
    request.session['typeinfo']=ty
    return render(request,'myweb/list.html',context)
# 详情页处理
def detailinfo(request):
    gid=int(request.GET.get('tid'))
    goods=GoodsInfo.objects.get(id=gid)
    goods.clicknum+=1
    # goods.save()
    # 拿到商品对应的类别id
    tid=goods.typeid
    # 分隔路径，拿到根类别的id
    # print(Types.objects.get(id=tid).path.split(','))
    tys=Types.objects.get(id=tid).path.split(',')
    tyid=tys[1]
    # print(tyid)
    ty=Types.objects.get(id=tyid)
    ty1 = {'id': tyid, 'name': ty.name}
    request.session['typeinfod']=ty1
    context={'goods':goods}
    return render(request,'myweb/detail.html',context)
# 浏览购物车
def cartinfo(request):
    kind = loadinfo(request)
    context={'kind':kind}
    if 'shoplist' not in request.session:
        request.session['shoplist']={}
    return render(request,'myweb/cart.html',context)
# 清空购物车
def cartclear(request):
    request.session['shoplist']={}
    return render(request,'myweb/cart.html')
# 添加购物车
def addCart(request,gid):
    # gid=request.GET.get('tid')
    goods=GoodsInfo.objects.get(id=gid)
    shop=goods.toDict()
    shop['m']=int(request.POST.get('m'))
    print(shop)
    # 获取购物车的信息
    # print(request.session['shoplist'])
    # 添加一句判断，如果首先就添加购物车，要判断shoplist的session是否存在
    if 'shoplist' not in request.session:
        request.session['shoplist'] = {}
    if  request.session['shoplist']!='':
        shoplist=request.session['shoplist']
        print('1%s'%shoplist)
    else:
        shoplist={}
     # 判断新添加的商品是否在购物车中，在就只增加数量
    if gid in shoplist:
        shoplist[gid]['m']+=shop['m']
        print('新商品')
    else:
        shoplist[gid]=shop
        # print('2%s'%shoplist)
    # 将购物车信息存入session
    request.session['shoplist']=shoplist
    # 重定向到购物车页面
    return redirect('/cartinfo/')
# 改变购物车
def cartchange(request):
    # 先取session
    shoplist=request.session['shoplist']
    print(shoplist)
    # 获取前台传过来的商品id和数量
    gid=request.GET.get('gid')
    print(shoplist[gid])
    num=int(request.GET.get('num'))
    if num<1:
        num=1
    # 将商品数据存入shoplist对象中
    shoplist[gid]['m']=num
    # 重新写入session
    request.session['shoplist']=shoplist
    # 重定向到cartinfo页面
    return redirect('/cartinfo/')

# 删除购物车
def defcart(request):
    gid=request.GET.get('gid')
    # print(gid)
    shoplist=request.session['shoplist']
    # print(shoplist)
    #
    del shoplist[gid]
    request.session['shoplist']=shoplist
    return redirect('/cartinfo/')

# 用户中心
def user_center_info(request):
    id=request.session['userinfo']['id']
    user_email=UserInfo.objects.get(id=id).uemail
    user_address=UserInfo.objects.get(id=id).uaddress
    # 根据点击量，排序取出前4个商品
    goods=GoodsInfo.objects.all().order_by('-clicknum' )[0:5]
    list={}
    for g in goods:
        list[g.toDict()['id']]=g.toDict()
    print(goods)
    request.session['newgoods']=list
    context={'title':'用户中心',
             'user_email':user_email,
             'user_address':user_address,
             'user_name':request.session['userinfo']['username']}
    return render(request,'myweb/user_center_info.html',context)

# 地址信息
def user_center_site(request):
    user=UserInfo.objects.get(id=request.session['userinfo']['id'])
    print(user)
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user}
    return render(request,'myweb/user_center_site.html',context)

# 订单处理
def ordersadd(request):
    gid=request.GET.get('gids','')
    if len(gid)==0:
        context={"info":'未选择商品，请先选择商品再提交'}
        return render(request,'myweb/info.html',context)
    # 对商品id进行切割,得到商品id组成的列表
    gids=gid.split(',')
    # 从session中获取到对应的商品信息
    shoplist=request.session['shoplist']
    # 定义一个订单字典进行存储
    orderlist={}
    # 在遍历商品时，最好统计出对应商品的价格
    total=0
    # 遍历提交的商品id拿到对应的商品信息
    for gi in gids:
        orderlist[gi]=shoplist[gi]#以商品id为键，实际商品对象对值存入orderlist.
        total+=shoplist[gi]['price']*shoplist[gi]['m']
    # 将订单列表和总价都存入session
    request.session['orderlist']=orderlist
    request.session['total']=total
    return render(request,'myweb/place_order.html')
# 确认订单
def ordersconfig(request):
    logerid=request.session['userinfo']['id']
    post = request.POST
    recinfo={}
    recinfo['orecive'] = post.get('ushou')
    recinfo['oaddress'] = post.get('uaddress')
    recinfo['oyoubian'] = post.get('uyoubian')
    recinfo['ophone'] = post.get('uphone')
    request.session['recinfo']=recinfo
    return render(request,'myweb/config.html')
# 提交订单
def ordersinsert(request):
    try:
        # 1、要添加订单信息
        logerid = request.session['userinfo']['id']
        total = request.session['total']
        order = OrderInfo()
        post = request.POST
        order.user_id = logerid
        recinfo=request.session['recinfo']
        import time
        order.oid=int(time.time())
        order.orecive = recinfo['orecive']
        order.oaddress = recinfo['oaddress']
        order.oyoubian = recinfo['oyoubian']
        order.ophone =  recinfo['ophone']
        order.odate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order.oIspay = 0
        order.ptotal = total
        order.save()
        print(order)
        # 2、添加订单详情信息，遍历订单中商品对象，将每个商品信息存入订单详情表中
        orderlist=request.session['orderlist']
        print(orderlist)
        shoplist=request.session['shoplist']
        for gid,good in orderlist.items():
            print(good)
            # 下过订单的商品就要从shoplist里面删除
            del shoplist[gid]
            # 每个商品就是一个详情
            odetail=OrderDetailInfo()
            odetail.order_id=order.oid
            odetail.goods_id=good['id']
            odetail.price=good['price']*good['m']
            odetail.count=good['m']
            odetail.save()
            # 清除订单表和总价表的session
        del request.session['orderlist']
        del request.session['total']
        context={"info":'支付成功'}
        return render(request,'myweb/info.html',context)
    except:
        context={"info":"支付失败"}
        return render(request, 'myweb/info.html', context)
# 订单信息
def user_center_order(request):
    # 从session中获取登录这id
    logerid=request.session['userinfo']['id']
    # # 从订单表中查出对应的订单
    order=OrderInfo.objects.filter(user_id=logerid)
    print(order)
    # # 如果定义到这儿，会出现所有的订单信息及商品信息重复
    #所以将定义放在for一层循环里
    # detaillist1 = {}
    # 声明全局变量存所有订单信息
    detaillist = []

    for o1 in order:
        # 声明局部变量存每一个订单信息，防止后面的订单信息覆盖前面的订单信息
        detaillist1 = {}
        print(detaillist)
        print(detaillist1)
        # 遍历订单获取一个一个订单
        print("o1%s"%o1)
        # 每个订单对应一个详细商品信息，每次在订单下初始化，
        # 防止所有的商品都被重复添加
        goodinfo = []
        # 获取订单id
        id1=o1.oid
        print("订单编号%s"%id1)
        # 将订单基本信息存储
        detaillist1['oid']=o1.oid
        detaillist1['ptotal']=o1.ptotal
        detaillist1['odate']=o1.odate
        # 在订单详情里，根据订单号找到所属的订单号
        orderdetail=OrderDetailInfo.objects.filter(order_id=id1)
        print("商品详情%s"%orderdetail)
        # 获取到是列表，遍历列表，拿到详细商品信息
        for o2 in orderdetail:
                print("o2%s"%o2)
                detaillist1['price']=o2.price
                detaillist1['goodsid']=o2.goods_id
                good = GoodsInfo.objects.get(id=o2.goods_id)
                list1=good.toDict()
                list1['count']=o2.count
                goodinfo.append(list1)
                print(goodinfo)
        # 将订单详情获取完后，加到detaillist1字典中
        detaillist1['goodinfo']=goodinfo
        print(detaillist1)
        # 一个订单遍历完成，加到detaillist列表中
        detaillist.append(detaillist1)
        print('一个订单遍历完成，加%s'%detaillist)
        print("sss")
    # print(goodinfo)
    context={"detaillist":detaillist}
    # # 遍历订单，取出对应的订单详情
    #
    # return HttpResponse("ok")
    return render(request,'myweb/user_center_order.html',context)
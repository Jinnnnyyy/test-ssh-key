from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from myweb.models import UserInfo,GoodsInfo,OrderDetailInfo,OrderInfo
from myadmin.models import Types
import time,random
import os
from PIL import Image,ImageDraw,ImageFont
from django.core.paginator import Paginator
# Create your views here.
# 登录页面
def log(request):
    return render(request,'myadmin/login.html')
# 验证码
def verifycode(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 30
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/msyh.ttf', 23)
    # font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
 # 实现登录
def dolog(request):
    post=request.POST
    name=post.get('name')
    pwd=post.get('pwd')
    code=post.get('verifycode')
    print(code)
    print(request.session['verifycode'])
    if code!=request.session['verifycode']:
        context={'info':'验证码错误'}
        return render(request,'myadmin/login.html',context)
    else:
        # 从数据库中取数据
        try:
            # 从数据库中获取登录信息
            user = UserInfo.objects.get(uname=name)
            print(code)
            if user.uid == 2:
                # 验证密码
                import hashlib
                m = hashlib.md5()
                print(code)
                m.update(bytes(pwd, encoding="utf8"))
                if user.upwd == m.hexdigest():
                    print(code)
                    # 此处表示登录成功，将登录成功后的信息放入到session中
                    request.session['adminuser'] = user.toDict()
                    return render(request,'myadmin/index.html')
                else:
                    context = {'info': '登录密码错误！'}
            else:
                context = {'info': '登录者不是后台管理员！'}
        except:
            context = {'info': '登录账号错误！'}

            return render(request, "myadmin/login.html", context)

#后台设置
def afterset(request):
    return render(request,'myadmin/index.html')
def logout(request):
    del request.session['adminuser']
    return redirect('/myadmin')


def welcome(request):
    return render(request,'myadmin/welcome.html')
# 帮助页面
def help(request):
    return render(request,'myadmin/help.html')

def user_manage(request):
    user=UserInfo.objects.all()
    context={'user':user}
    return render(request, 'myadmin/user_manage.html',context)
# 会员添加
def add_user(request):
    post=request.POST
    user=UserInfo()
    user.uname=post.get('uname')
    user.uemail=post.get('uemail')
    upwd=post.get('upwd')
    import hashlib
    m = hashlib.md5()
    m.update(bytes(upwd, encoding="utf8"))
    user.upwd = m.hexdigest()
    user.uphone=post.get('uphone')
    user.uid=post.get('uid')
    user.save()
    return redirect('/myadmin/user_manage/')
# 修改用户信息
def update_user(request,id):
    user = UserInfo.objects.all()
    user1=UserInfo.objects.get(id=id)
    context={'user':user,'user1':user1}
    return render(request,'myadmin/update_user.html',context)
# 确认修改
def update_user_conf(request,id):
    post=request.POST
    user=UserInfo.objects.get(id=id)
    user.uname=post.get('uname')
    user.uemail=post.get('uemail')
    user.uphone=post.get('uphone')
    user.uid=post.get('uid')
    user.save()
    return redirect('/myadmin/user_manage/')
# 删除信息
def del_user(request,id):
    user=UserInfo.objects.get(id=id)
    user.delete()
    return redirect('/myadmin/user_manage/')
# 添加会员
def user_add(request):
    return render(request, 'myadmin/user_add.html')
# 浏览商品类别
def scan_goods_kind(request,pindex):
    kind=Types.objects.all()
    # print(kind[0].name)
    # 创建分页对象
    p=Paginator(kind,8)
    # 获取到当前页码
    if pindex=="":
        pindex=1
    pindex=int(pindex)
    list=p.page(pindex)
    # 生成页码范围
    plist=p.page_range
    context={'kind':list,'plist':plist,'pindex':pindex}
    print(context)
    return render(request, 'myadmin/scan_goods_kind.html',context)
# 添加商品类别页面
def add_goods_kind(request,tid):
    # 参数是字符串
    if int(tid)==0:
        context={'pid':0,'pname':'根类别','path':'0,'}
        return render(request, 'myadmin/add_goods_kind.html', context)
    else:
        ob = Types.objects.filter(id=tid)
        context = {'pid': ob[0].id, 'path': ob[0].path + str(ob[0].id) + ',', 'pname': ob[0].name}
        return render(request, 'myadmin/add_goods_kind.html',context)
#添加到数据库
def goods_kind_insert(request):
    try:
         kind=Types()
         kind.pid=request.POST.get('pid')
         kind.path=request.POST.get('path')
         kind.name=request.POST.get('name')
         kind.save()
         context={'info':'添加成功'}
    except:
        context={'info':'添加失败'}
    return render(request,'myadmin/info.html',context)
# 类别信息删除
def goods_kind_del(request,tid):
    try:
        # 获取被删除商品的子类别信息量，若有数据，就禁止删除当前类别
        row = Types.objects.filter(pid=tid).count()
        if row > 0:
            context = {'info': '删除失败：此类别下还有子类别！'}
            return render(request, "myadmin/info.html", context)
        ob = Types.objects.get(id=tid)
        ob.delete()
        context = {'info': '删除成功！'}
    except:
        context = {'info': '删除失败！'}
    return render(request, "myadmin/info.html", context)
#类别信息修改
def goods_kind_edit(request,tid):
    try:
        ob = Types.objects.get(id=tid)
        context = {'type': ob}
        return render(request, "myadmin/edit.html", context)
    except:
        context = {'info': '没有找到要修改的信息！'}
    return render(request, "myadmin/info.html", context)
#修改到数据库
def goods_kind_update(request,tid):
    try:
        kind=Types.objects.get(id=tid)
        kind.name=request.POST.get('name')
        kind.save()
        context={'info':'修改成功'}
    except:
        context={'info':'修改失败'}
    return render(request, "myadmin/info.html", context)

# 浏览商品信息
def goods_info(request,pindex):

    goods=GoodsInfo.objects.all()
    print(goods)
    for ob in goods:
        type=Types.objects.get(id=ob.typeid)
        ob.typename=type.name#添加商品类别
    p=Paginator(goods,5)#创建分页对象
    if pindex=='':
        pindex=1
    pindex = int(pindex)
    list=p.page(pindex)
    plist=p.page_range#得到页码范围
    context={'goods':list,'plist':plist,'pindex':pindex}
    return render(request,'myadmin/goods_info.html',context)
# 发布商品信息页面
def goods_set(request):
    kind=Types.objects.all()
    print(kind[0].id)
    context={'kind':kind}
    return render(request, "myadmin/goods_set.html",context)

# 发布到数据库
def goods_info_insert(request):
    try:
        # 判断并执行图片上传，缩放等处理
        myfile = request.FILES.get("pic", None)
        print('1%s'%myfile)
        if not myfile:
            return HttpResponse("没有上传文件信息！")
        # 以时间戳命名一个新图片名称
        filename = str(time.time()) + "." + myfile.name.split('.').pop()
        print('2%s'%filename)
        destination = open(os.path.join("./static/myadmin/goods/", filename), 'wb+')
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print('21%s' % filename)
        # 执行图片缩放
        im = Image.open("./static/myadmin/goods/" + filename)
        print('3')
        # 缩放到375*375:
        im.thumbnail((375, 375))
        print('4')
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/myadmin/goods/" + filename, 'png')
        print('5')
        # 缩放到220*220:
        im.thumbnail((220, 220))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/myadmin/goods/m_" + filename, 'png')
        print('7')
        # 缩放到220*220:
        im.thumbnail((75, 75))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/myadmin/goods/s_" + filename, 'png')
        print('8')

        # 获取商品信息并执行添加
        ob = GoodsInfo()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.descr = request.POST['descr']
        ob.picname = filename
        ob.state = 1
        ob.addtime = time.time()
        ob.save()
        context = {'info': '添加成功！'}
    except:
        context = {'info': '添加失败！'}

    return render(request, "myadmin/info.html", context)

# 删除商品信息
def goods_info_del(request,gid):
    try:
        # 获取被删除商品信的息量，先删除对应的图片
        ob = GoodsInfo.objects.get(id=gid)
        if ob.state>1:
            context={'info':'删除失败，只能删除新商品'
            }
            return render(request,'myadmin/info.html',context)
        # 执行图片删除
        os.remove("./static/myadmin/goods/" + ob.picname)
        os.remove("./static/myadmin/goods/m_" + ob.picname)
        os.remove("./static/myadmin/goods/s_" + ob.picname)
        # 执行商品信息的删除
        ob.delete()
        context = {'info': '删除成功！'}
    except:
        context = {'info': '删除失败！'}
    return render(request, "myadmin/info.html", context)
# 编辑商品信息
def goods_info_edit(request,gid):
    # try:
        # 获取要编辑的信息
        ob = GoodsInfo.objects.get(id=gid)
        # 获取商品的类别信息
        list = Types.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has')
        # 放置信息加载模板
        context = {"typelist": list, 'goods': ob}
        return render(request, "myadmin/goods_edit.html", context)
    # except:
    #     context = {'info': '没有找到要修改的信息！'}
    #     return render(request, "myadmin/info.html", context)
#修改到数据中
def goods_info_update(request,gid):
    b = False  # 一个标识，判断是否有新图片上传
    oldpicname = request.POST['oldpicname']
    try:
        if None != request.FILES.get("pic"):
            myfile = request.FILES.get("pic", None)
            if not myfile:
                return HttpResponse("没有上传文件信息！")
            # 以时间戳命名一个新图片名称
            filename = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open(os.path.join("./static/myadmin/goods/", filename), 'wb+')
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            # 执行图片缩放
            im = Image.open("./static/myadmin/goods/" + filename)
            # 缩放到375*375:
            im.thumbnail((375, 375))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/myadmin/goods/" + filename, 'png')
            # 缩放到220*220:
            im.thumbnail((220, 220))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/myadmin/goods/m_" + filename, 'png')
            # 缩放到220*220:
            im.thumbnail((100, 100))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/myadmin/goods/s_" + filename, 'png')
            b = True
            picname = filename
        else:
            picname = oldpicname
        ob = GoodsInfo.objects.get(id=gid)
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.descr = request.POST['descr']
        ob.picname = picname
        ob.state = 2
        ob.save()
        context = {'info': '修改成功！'}
        if b:#为真，表示有新图片上传，要删除老图片
            os.remove("./static/myadmin/goods/m_" + oldpicname)  # 执行老图片删除
            os.remove("./static/myadmin/goods/s_" + oldpicname)  # 执行老图片删除
            os.remove("./static/myadmin/goods/" + oldpicname)  # 执行老图片删除
    except:#添加失败了
        context = {'info': '修改失败！'}
        if b: #添加失败了，又上传了图片，要删除新图片
            os.remove("./static/myadmin/goods/m_" + filename)  # 执行新图片删除
            os.remove("./static/myadmin/goods/s_" + filename)  # 执行新图片删除
            os.remove("./static/myadmin/goods/" + filename)  # 执行新图片删除
    return render(request, "myadmin/info.html", context)

# 搜索查询
def goods_search(request,pindex):
    gname=request.GET.get('name','')
    kind=request.GET.get('kind','')
    list=GoodsInfo.objects.all()
    for ob in list:
        type = Types.objects.get(id=ob.typeid)
        ob.typename = type.name  # 添加商品类别
    if gname!='':
        list=list.filter(goods=gname)

    if kind!='':
        k=Types.objects.filter(name=kind)[0].id
        print(k)
        list=list.filter(typeid=k)
    p=Paginator(list,5)
    if pindex=="":
        pindex=1
    pindex=int(pindex)
    lists=p.page(pindex)
    plist=p.page_range
    context={'goods':lists,'plist':plist,'pindex':pindex}
    return render(request, 'myadmin/goods_info.html', context)
# 新订单信息
def new_order(request):
    order=OrderInfo.objects.filter()
    detaillist = []

    for o1 in order:
        # 声明局部变量存每一个订单信息，防止后面的订单信息覆盖前面的订单信息
        detaillist1 = {}
        print(detaillist)
        print(detaillist1)
        # 遍历订单获取一个一个订单
        print("o1%s" % o1)
        # 每个订单对应一个详细商品信息，每次在订单下初始化，
        # 防止所有的商品都被重复添加
        goodinfo = []
        # 获取订单id
        id1 = o1.oid
        print("订单编号%s" % id1)
        # 将订单基本信息存储
        detaillist1['oid'] = o1.oid
        detaillist1['ptotal'] = o1.ptotal
        detaillist1['odate'] = o1.odate
        # 在订单详情里，根据订单号找到所属的订单号
        orderdetail = OrderDetailInfo.objects.filter(order_id=id1)
        print("商品详情%s" % orderdetail)
        # 获取到是列表，遍历列表，拿到详细商品信息
        for o2 in orderdetail:
            print("o2%s" % o2)
            detaillist1['price'] = o2.price
            detaillist1['goodsid'] = o2.goods_id
            good = GoodsInfo.objects.get(id=o2.goods_id)
            list1 = good.toDict()
            list1['count'] = o2.count
            goodinfo.append(list1)
            print(goodinfo)
        # 将订单详情获取完后，加到detaillist1字典中
        detaillist1['goodinfo'] = goodinfo
        print(detaillist1)
        # 一个订单遍历完成，加到detaillist列表中
        detaillist.append(detaillist1)
        print('一个订单遍历完成，加%s' % detaillist)
        print("sss")
    # print(goodinfo)
    context = {"detaillist": detaillist}
    return render(request,'myadmin/new_order.html',context)
# 历史订单信息
def old_order(request):
    return render(request,'myadmin/old_order.html')
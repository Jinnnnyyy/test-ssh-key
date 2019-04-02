from django.shortcuts import render
from django.core.paginator import Paginator
from job.models import Job
# Create your views here.

# 网站首页
def index(request,pIndex):
    pIndex = int(pIndex)
    list = Job.objects.all()
    p = Paginator(list,100)
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    if pIndex < 1:
        pIndex = 1
    lists = p.page(pIndex)
    context = {'lists': lists, 'plist': p.page_range, 'pIndex': pIndex,'allpage':p.num_pages}
    return render(request,'job/index.html',context)


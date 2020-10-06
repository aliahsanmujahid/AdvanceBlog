from django.shortcuts import render, get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from comment.models import Comment
import random
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from itertools import chain


def news_detail(request,word):

    site = Main.objects.get(pk=3)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(name=word)
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    tagname = News.objects.get(name=word).tag
    tag = tagname.split(',')

    try:
       mynews  = News.objects.get(name=word)
       mynews.show = mynews.show + 1
       mynews.save()
    except:
       print('Can,t Add Show')

    code = News.objects.get(name=word).pk
    comment = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:3]
    cmcount = len(comment)
    
    return render(request, 'front/news_detail.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'shownews':shownews, 'popnews':popnews, 'popnews2':popnews2, 'tag':tag, 'trending':trending, 'code':code, 'comment':comment, 'cmcount':cmcount,})


def news_detail_short(request,pk):
    
    site = Main.objects.get(pk=3)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]

    shownews = News.objects.filter(rand=pk)
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    tagname = News.objects.get(rand=pk).tag
    tag = tagname.split(',')

    try :

        mynews = News.objects.get(rand=pk)
        mynews.show = mynews.show + 1
        mynews.save()

    except:

        print("Can't Add Show")

    code = News.objects.get(rand=pk).pk
    comment = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:3]
    cmcount = len(comment)

    return render(request, 'front/news_detail.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'shownews':shownews, 'popnews':popnews, 'popnews2':popnews2, 'tag':tag, 'trending':trending, 'code':code, 'comment':comment, 'cmcount':cmcount,})


def news_list(request):

    if not request.user.is_authenticated :
        return redirect('mylogin')

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        news = News.objects.filter(writer=request.user)
    elif perm == 1 :
        newss = News.objects.all()
        paginator = Paginator(newss,10)
        page = request.GET.get('page')
        print("-------------------------------------")
        print(page)
        try:
            news = paginator.page(page)

        except EmptyPage:
            news = paginator.page(paginator.num_pages)   

        except PageNotAnInteger:
            news = paginator.page(1)

         

    return render(request,'back/news_list.html',{'news': news})

def news_add(request):
    if not request.user.is_authenticated :
        return redirect('mylogin')
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    if len(str(day)) == 1 :
        day = "0" + str(day)
    if len(str(month)) == 1 :
        month = "0" + str(month)

   
    today = str(year) + "/" + str(month) + "/" + str(day)
    time = str(now.hour) + ":" + str(now.minute)

    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000,9999))
    rand = date + randint 
    rand = int(rand)
    while len(News.objects.filter(rand = rand)) != 0 :
        randint = str(random.randint(1000,9999))
        rand = date + randint 
        rand = int(rand)


    cat = SubCat.objects.all()

    if request.method == "POST":
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle=='' or  newscat=='' or  newstxtshort=='' or  newstxt=='': 
          error = "   All Field Required"     
          return render(request,'back/error.html',{'error':error})   
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            if str(myfile.content_type).startswith('image'):
                if myfile.size<500000:

                   filename = fs.save(myfile.name,myfile)
                   url = fs.url(filename)
                   newsname = SubCat.objects.get(pk=newsid).name
                   ocatid = SubCat.objects.get(pk=newsid).catid
                   b = News(rand=rand,tag=tag,name=newstitle, short_txt =newstxtshort,body_txt = newstxt,date = today,time=time,picname = filename,picurl = url,writer =request.user ,catname =newsname ,catid = newsid,show = 0,ocatid=ocatid)
                   b.save()
                   count = len(News.objects.filter(ocatid=ocatid))
                   b=Cat.objects.get(pk=ocatid)
                   b.count = count
                   b.save()
                else:
                   error = myfile.size  
                   return render(request,'back/error.html',{'error':error})    
            else:
              error = " Image Type Not Support "     
              return render(request,'back/error.html',{'error':error})    
        except:
            error = " Add An Image"     
            return render(request,'back/error.html',{'error':error})  
        return redirect('news_list')
    return render(request,'back/news_add.html',{'cat':cat})


def news_delete(request,pk):
    if not request.user.is_authenticated :
        return redirect('mylogin')

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user) :
            error = "Access Denied"
            return render(request, 'back/error.html' , {'error':error})


    try:
         b= News.objects.get(pk=pk)
         fs = FileSystemStorage()
         fs.delete(b.picname)
         ocatid = News.objects.get(pk=pk).ocatid
         b.delete()
         count = len(News.objects.filter(ocatid=ocatid))

         m=Cat.objects.get(pk=ocatid)
         m.count = count
         m.save()

    except:
         error = " Something Worng Delete"     
         return render(request,'back/error.html',{'error':error})  

    return redirect('news_list')


def news_edit(request,pk):
    if not request.user.is_authenticated :
        return redirect('mylogin')
    if len(News.objects.filter(pk=pk)) == 0:
        error = " News Dosn,t Exist "     
        return render(request,'back/error.html',{'error':error}) 
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user) :
            error = "Access Denied"
            return render(request, 'back/error.html' , {'error':error})
    
    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()
    if request.method == "POST":
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle=='' or  newscat=='' or  newstxtshort=='' or  newstxt=='': 
          error = "   All Field Required"     
          return render(request,'back/error.html',{'error':error})   
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            if str(myfile.content_type).startswith('image'):
                if myfile.size<500000:

                   filename = fs.save(myfile.name,myfile)
                   url = fs.url(filename)
                   newsname = SubCat.objects.get(pk=newsid).name

                   b = News.objects.get(pk=pk)

                   fss = FileSystemStorage()
                   fss.delete(b.picname)

                   b.name=newstitle
                   b.short_txt=newstxtshort
                   b.body_txt=newstxt
                   b.picname=filename
                   b.picurl=url
                   b.catname=newsname
                   b.catid=newsid
                   b.tag=tag
                   b.act = 0
                   b.save()
                else:
                   error = myfile.size  
                   return render(request,'back/error.html',{'error':error})    
            else:
              error = "  Image Type Not Support "     
              return render(request,'back/error.html',{'error':error})    
        except:
            newsname = SubCat.objects.get(pk=newsid).name

            b = News.objects.get(pk=pk)
            b.name=newstitle
            b.short_txt=newstxtshort
            b.body_txt=newstxt
            b.catname=newsname
            b.catid=newsid
            b.tag=tag
            b.act = 0

            b.save()
        return redirect('news_list')    
    return render(request,'back/news_edit.html',{'pk':pk,'news':news,'cat':cat})


def news_publish(request,pk):
    
    # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end

    
    news = News.objects.get(pk=pk)
    news.act = 1
    news.save()

    return redirect('news_list')   


def news_all_show(request,word):

    catid = Cat.objects.get(name=word).pk
    allnews = News.objects.filter(ocatid=catid)

    site = Main.objects.get(pk=3)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_news.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2, 'allnews':allnews})     

def all_news(request):

    allnews = News.objects.all()

    site = Main.objects.get(pk=3)
    news = News.objects.filter(act=1).order_by('-pk')

    f_rom = []
    t_o = []
    for i in range(30):
        b = datetime.datetime.now() -  datetime.timedelta(days=i)
        year = b.year
        month = b.month
        day = b.day
    
        if len(str(day)) == 1 :
           day = "0" + str(day)
        if len(str(month)) == 1 :
           month = "0" + str(month)
        b = str(year) + "/" + str(month) + "/" + str(day)  
        f_rom.append(b) 

    for i in range(30):
        b = datetime.datetime.now() -  datetime.timedelta(days=i)
        year = b.year
        month = b.month
        day = b.day
    
        if len(str(day)) == 1 :
           day = "0" + str(day)
        if len(str(month)) == 1 :
           month = "0" + str(month)
        b = str(year) + "/" + str(month) + "/" + str(day)  
        t_o.append(b)

    paginator = Paginator(allnews,3)
    page = request.GET.get('page')
        
    try:
        allnews = paginator.page(page)

    except EmptyPage:
        allnews = paginator.page(paginator.num_pages)   

    except PageNotAnInteger:
        allnews = paginator.page(1)

    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_news2.html', {'t_o':t_o,'f_rom':f_rom,'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2, 'allnews':allnews})     
 

def all_news_search(request):

    mysearch = ""
    mycatid = 0
    if request.method == "POST":
        txt = request.POST.get('txt')
        catid = request.POST.get('cat')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')
        print("======================",f_rom,t_o)

        if t_o < f_rom :
            msg = "Select Date Correctly"     
            return render(request,'front/msgbox.html',{'msg':msg})   
        
        
        mysearch = txt
        mycatid = catid
        #print("======================",catid)
        #print("======================",mycatid)
        if catid == "0" :
           if f_rom != "0" and t_o != "0" :

               a = News.objects.filter(name__contains = txt,date__gte=f_rom,date__lte=t_o)
               b = News.objects.filter(short_txt__contains = txt,date__gte=f_rom,date__lte=t_o)
               c = News.objects.filter(body_txt__contains = txt,date__gte=f_rom,date__lte=t_o)
           else:
               a = News.objects.filter(name__contains = txt)
               b = News.objects.filter(short_txt__contains = txt)
               c = News.objects.filter(body_txt__contains = txt)
        else:
           if f_rom != "0" and t_o != "0" : 
               a = News.objects.filter(name__contains = txt,ocatid=catid,date__gte=f_rom,date__lte=t_o)
               b = News.objects.filter(short_txt__contains = txt,ocatid=catid,date__gte=f_rom,date__lte=t_o)
               c = News.objects.filter(body_txt__contains = txt,ocatid=catid,date__gte=f_rom,date__lte=t_o)
           else :   
                a = News.objects.filter(name__contains = txt,ocatid=catid)
                b = News.objects.filter(short_txt__contains = txt,ocatid=catid)
                c = News.objects.filter(body_txt__contains = txt,ocatid=catid)
        allnewss = list(chain(a,b,c))
        allnews = list(dict.fromkeys(allnewss))
    else :
        #print("======================",mycatid,mysearch)
        if mycatid == 0 :
            if f_rom != "0" and t_o != "0" : 
                a = News.objects.filter(name__contains = mysearch,date__gte=f_rom,date__lte=t_o)
                b = News.objects.filter(short_txt__contains = mysearch,date__gte=f_rom,date__lte=t_o)
                c = News.objects.filter(body_txt__contains = mysearch,date__gte=f_rom,date__lte=t_o)
            else:
                a = News.objects.filter(name__contains = mysearch)
                b = News.objects.filter(short_txt__contains = mysearch)
                c = News.objects.filter(body_txt__contains = mysearch) 
        else : 
            if f_rom != "0" and t_o != "0" :   
               a = News.objects.filter(name__contains = mysearch,ocatid=mycatid,date__gte=f_rom,date__lte=t_o)
               b = News.objects.filter(short_txt__contains = mysearch,ocatid=mycatid,date__gte=f_rom,date__lte=t_o)
               c = News.objects.filter(body_txt__contains = mysearch,ocatid=mycatid,date__gte=f_rom,date__lte=t_o)
            else:
               a = News.objects.filter(name__contains = mysearch,ocatid=mycatid)
               b = News.objects.filter(short_txt__contains = mysearch,ocatid=mycatid)
               c = News.objects.filter(body_txt__contains = mysearch,ocatid=mycatid) 
        allnewss = list(chain(a,b,c))
        allnews = list(dict.fromkeys(allnewss))

    paginator = Paginator(allnews,3)
    page = request.GET.get('page')
    f_rom = []
    t_o = []
    for i in range(30):
        b = datetime.datetime.now() -  datetime.timedelta(days=i)
        year = b.year
        month = b.month
        day = b.day
    
        if len(str(day)) == 1 :
           day = "0" + str(day)
        if len(str(month)) == 1 :
           month = "0" + str(month)
        b = str(year) + "/" + str(month) + "/" + str(day)  
        f_rom.append(b) 

    for i in range(30):
        b = datetime.datetime.now() -  datetime.timedelta(days=i)
        year = b.year
        month = b.month
        day = b.day
    
        if len(str(day)) == 1 :
           day = "0" + str(day)
        if len(str(month)) == 1 :
           month = "0" + str(month)
        b = str(year) + "/" + str(month) + "/" + str(day)  
        t_o.append(b)    
    try:
        allnews = paginator.page(page)

    except EmptyPage:
        allnews = paginator.page(paginator.num_pages)   

    except PageNotAnInteger:
        allnews = paginator.page(1)

    site = Main.objects.get(pk=3)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_news2.html', {'t_o':t_o,'f_rom':f_rom,'mysearch':mysearch,'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2, 'allnews':allnews})                
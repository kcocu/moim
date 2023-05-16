from django.http import HttpResponse
from django.shortcuts import redirect, render
from all_info.models import GroupInfo, Info
# from django.core.paginator import Paginator
from make_moim.models import Make_Moim
from tag.models import Tag, TagMoim
from write.models import Good
# from django.contrib import messages

# Create your views here.
def board_moim(request):
    return render(request,'board_moim/board.html')
    
def list_moim(request):
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    moim_lists = Make_Moim.objects.all().order_by('-make_id')
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Make_Moim.objects.all().count()
    total_page = total_count//5 +1
    if page > total_page:
        page = total_page
        end = page * 5
        start = end -5
    
    # if total_count % 10 !=0:
    #     total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page+1)
    moim_lists = moim_lists[start:end]

    context = {
        'moim_lists' : moim_lists,
        'page_info' : page_info,
        'total_page' : total_page,
        'e_page' : e_page,
        'page':page
        # 'posts' : posts
    }
    return render(request,'board_moim/board_list.html', context)
def kick(request,pk):
    make_moim = Make_Moim.objects.get(make_id=pk)
    admin = GroupInfo.objects.filter(admin='1')[0]
    info_id = request.session['info_id']
    info_kick = request.POST.get('info_kick')
    print(info_kick)
    if admin.info_id == info_id:
        g=GroupInfo.objects.get(make_moim=make_moim, info=info_kick)
        g.delete()
        return redirect('board_moim:board_detail',pk)

def board_detail(request, pk):
    make_moim = Make_Moim.objects.get(make_id=pk)
    groupinfo = GroupInfo.objects.filter(make_moim=make_moim)
    comments = Good.objects.filter(make_moim=make_moim)
    context ={
        'make_moim':make_moim, 'comments':comments, 'groupinfo':groupinfo
    }
    return render(request, 'board_moim/detail.html',context)

def board_update(request, pk):
    make_moim = Make_Moim.objects.get(make_id=pk)
    admin = GroupInfo.objects.filter(admin='1')[0]
    info_id = request.session['info_id']
    if admin.info_id == info_id:
        if request.method == 'POST':
            make_id = request.POST.get('make_id')
            name = request.POST.get('name')
            commend = request.POST.get('commend')
            imgfile = request.POST.get('imgfile')
            location = request.POST.get('location')
            max_people = request.POST.get('max_people')
            category = request.POST.get('category')
            alltag=request.POST.get('tag')
            tags = alltag.split(',')
        
            try :
                TagMoim.objects.filter(make_moim=make_moim).delete()
                for i in tags:
                    newtag = Tag(name=i)
                    newtag.save()
                    tag_id=Tag.objects.all().order_by('-pk')[0]
                    t = TagMoim()

                    make_moim.make_id = make_id
                    make_moim.name = name
                    make_moim.commend = commend
                    make_moim.imgfile = imgfile
                    make_moim.location = location
                    make_moim.max_people = max_people
                    make_moim.category = category
                # make_moim.tags = tags
                    make_moim.save()
                    
                    t.tag = tag_id   
                    t.make_moim = make_moim
                    t.save()

                # return render(request, 'board_moim/detail.html')
                return redirect(f'/board_moim/{pk}/')
            except Exception as e:
                print(e)
                return render(request, 'board_moim/update_fail.html',{'make_moim':make_moim})
    else : 
        return HttpResponse(f'<h1>수정/삭제 권한이 없습니다.</h1><br><a href="/board_moim/{make_moim.make_id}">뒤로가기</a>')

    return render(request, 'board_moim/update.html',{'make_moim':make_moim})

def board_delete(request, pk):
    make_moim = Make_Moim.objects.get(make_id=pk)
    admin = GroupInfo.objects.filter(admin='1')[0]
    info_id = request.session['info_id']
    if admin.info_id == info_id:
        make_moim.delete()
        return redirect('/board_moim/list/')
    else : 
            return HttpResponse(f'<h1>수정/삭제 권한이 없습니다.</h1><br><a href="/board_moim/{make_moim.make_id}">뒤로가기</a>')

def comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        id = request.POST.get('id')
        make_moim = Make_Moim.objects.get(make_id=id)
        info_id=request.session.get('info_id')
        info=Info.objects.get(info_id=info_id)
        c = Good(content=comment, make_moim=make_moim, info=info)
        c.save()
        return redirect('/board_moim/%s/' %  id)

    # return render(request, 'board_moim/detail.html',{'make_moim':make_moim})

def search(request):
    csb=request.POST.get('change_search_bar')
    search = request.POST.get('search')
    
    tag = Tag.objects.filter(name__contains=search).order_by('-pk')
    make_moim = Make_Moim.objects.filter(name__contains=search).order_by('-make_id')
    category = Make_Moim.objects.filter(category__contains=search).order_by('-make_id')

    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분 귀찮으니까 각각 페이징 해주자
    tag_count = Tag.objects.filter(name__contains=search).count()
    name_count = Make_Moim.objects.filter(name__contains=search).count()
    category_count = Make_Moim.objects.filter(category__contains=search).count()
    tag_page = tag_count//5 +1
    name_page = name_count//5 +1
    category_page = category_count//5 +1
       
    if csb == 'all':
        page_tag = int(request.GET.get('page_tag',1)) #태그
        # if not page : page = '1'
        # page=int(page)
        end_tag = page_tag * 5
        start_tag = end_tag - 5
        s_page_tag = (page_tag-1)//10*10 + 1
        e_page_tag = s_page_tag +9
        
        page_ctg = int(request.GET.get('page_ctg',1)) #카테고리
        # if not page : page = '1'
        # page=int(page)
        end_ctg = page_ctg * 5
        start_ctg = end_ctg - 5
        s_page_ctg = (page_ctg-1)//10*10 + 1
        e_page_ctg = s_page_ctg +9
        
        if page_tag > tag_page: #태그
            page_tag = tag_page
            end_tag = page_tag * 5
            start_tag = end_tag -5
        
        if tag_count % 5 !=0:
            tag_page +=1

        if e_page_tag > tag_page : 
            e_page_tag = tag_page
            
        if page > name_page: #모임
            page = name_page
            end = page * 5
            start = end -5
        
        if tag_count % 5 !=0:
            name_page +=1

        if e_page > name_page : 
            e_page = name_page
            
        if page_ctg > category_page: #카테고리
            page_ctg = category_page
            end_ctg = page_ctg * 5
            start_ctg = end_ctg -5
        
        if category_count % 5 !=0:
            category_page +=1

        if e_page_ctg > category_page : 
            e_page_ctg = category_page

        page_info_ctg = range(s_page_ctg, e_page_ctg)
        category_list = category[start:end]
        page_info = range(s_page, e_page)
        moim_list = make_moim[start:end]
        page_info_tag = range(s_page_tag, e_page_tag)
        tag_list = tag[start:end]
        
        context ={
            'search':search, 'make_moim':make_moim, 'tag':tag,
            'category':category,'tag_list' : tag_list,
            'total_list' : moim_list,
            'category_list' : category_list,
            'page_info' : page_info,
            'page_info_ctg' : page_info_ctg,
            'page_info_tag' : page_info_tag,
            'total_page' : name_page,
            'tag_page' : tag_page,
            'category_page' : category_page,
            'e_page' : e_page,
            'page':page,
            'e_page_tag' : e_page_tag,
            'page_tag':page_tag,
            'e_page_ctg' : e_page_ctg,
            'page_ctg':page_ctg,
        }
        return render(request, 'board_moim/search.html', context)
    elif csb == 'search_title':
        if page > name_page: #이름
            page = name_page
            end = page * 5
            start = end -5
        
        if name_count % 5 !=0:
            name_page +=1

        if e_page > name_page : 
            e_page = name_page

        page_info = range(s_page, e_page)
        moim_list = make_moim[start:end]
        context ={
            'total_list' : moim_list,
            'page_info' : page_info,
            'total_page' : name_page,
            'e_page' : e_page,
            'page':page,'search':search, 'make_moim':make_moim,
        }
        return render(request, 'board_moim/search.html', context)
    elif csb == 'tag_title':
        page_tag = int(request.GET.get('page_tag',1))
        end_tag = page_tag * 5
        start_tag = end_tag - 5
        s_page_tag = (page_tag-1)//10*10 + 1
        e_page_tag = s_page_tag +9
        if page_tag > tag_page: #태그
            page_tag = tag_page
            end_tag = page_tag * 5
            start_tag = end_tag -5
        
        if tag_count % 5 !=0:
            tag_page +=1

        if e_page_tag > tag_page : 
            e_page_tag = tag_page

        page_info_tag = range(s_page, e_page)
        tag_list = tag[start:end]
        context ={
            'search':search, 'tag':tag,'tag_list' : tag_list,
            'page_info_tag' : page_info_tag,
            'tag_page' : tag_page,
            'e_page_tag' : e_page_tag,
            'page_tag':page_tag,
        }
        return render(request, 'board_moim/search.html', context)
    elif csb == 'category_title':
        if page > category_page: #카테고리
            page = category_page
            end = page * 5
            start = end -5
        
        if category_count % 5 !=0:
            category_page +=1

        if e_page > category_page : 
            e_page = category_page

        page_info = range(s_page, e_page)
        category_list = category[start:end]
        context = {
            'search':search, 'category':category,'total_list' : category_list,
            'page_info' : page_info,
            'total_page' : category_page,
            'e_page' : e_page,
            'page':page,
        }
        return render(request, 'board_moim/search.html', context)
            
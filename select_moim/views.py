from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from all_info.models import GroupInfo, Info
from make_moim.models import Make_Moim
from select_moim.models import Select_Moim
from write.models import Good

# Create your views here.
def make_good(request):
    if request.method == 'POST':
        comment = request.POST.get('comment') #댓글
        
        make_moim = Make_Moim.objects.get(pk=id)
        g = Good(content=comment, make_moim=make_moim)
        g.save()
        return redirect('/select_moim/detail/%s/' % g.good_id)

def select_moim(request):
    #페이지
    info_id=request.session['info_id']
    id = Info.objects.get(info_id=info_id)
    groupinfo=GroupInfo.objects.filter(info=id).order_by('info') 
    #a유저-a모임.a유저-b모임,a유저-c모임 ...

    
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    # moim_lists = Make_Moim.objects.all().order_by('-make_id')
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = GroupInfo.objects.filter(info=id).count()
    total_page = total_count//5 +1
    # if page > total_page:
    #     page = total_page
    #     end = page * 5
    #     start = end -5
    
    # if total_count % 10 !=0:
    #     total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page+1)
    groupinfo = groupinfo[start:end]

    context = {
    'groupinfo' : groupinfo,
    'page_info' : page_info,
    'total_page' : total_page,
    'e_page' : e_page,
    'page':page
    # 'posts' : posts
    }   

    return render(request, 'select_moim/select_moim.html',context)


    

# class Select_DetailView(DetailView):

def make_update(request, id):
    make_moim=Make_Moim.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        commend = request.POST.get('commend')
        location = request.POST.get('location')
        imgfile = request.POST.get('imgfile')
        max_people = request.POST.get('max_people')
        
        try : 
            make_moim.name = name
            make_moim.commend = commend
            make_moim.location = location
            make_moim.imgfile = imgfile
            make_moim.max_people = max_people
            make_moim.save()
            return render(request,'make_moim/detail.html')
        except:
            return redirect('/select_moim')

def delete(request, id):
    try :
        make_moim=Make_Moim.objects.get(id=id)
        make_moim.delete()
        return render(request,'make_moim/detail.html')
    except:
        return redirect('/select_moim')

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
    print(total_page)
    # if page > total_page:
    #     page = total_page
    #     end = page * 5
    #     start = end -5
    
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
        
def make_detail(request, id):
    try :
        make_moim= Make_Moim.objects.get(make_id=id)
        goods=Good.objects.filter(make_moim=make_moim)

        context = {
            'make_moim' : make_moim,
            'goods' : goods
            
        }
    except Make_Moim.DoesNotExist:
        raise Http404('해당 게시물을 찾을 수 없습니다.')
    return render(request, 'make_moim/make_detail.html', context)


def select_moim_id(request, moim_id):
    make_moim = Make_Moim.objects.get(make_id=moim_id)
    groupinfo = GroupInfo.objects.filter(make_moim=make_moim)
    comments = Good.objects.filter(make_moim=make_moim)
    try :
        id = request.session['info_id']
        GroupInfo.objects.get(info=id,make_moim=make_moim)
        context ={
            'make_moim':make_moim, 'comments':comments, 'groupinfo':groupinfo
        }
        return render(request, 'select_moim/detail.html', context)

    except Exception as e :
        print(e)
        return render(request, 'select_moim/no_signmoim.html', {'make_moim':make_moim})

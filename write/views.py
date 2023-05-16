import time, os
from django.urls import reverse #이거 쓰나?
from django.shortcuts import  get_object_or_404,render, redirect

from config import settings
from make_moim.models import Make_Moim
from .forms import BoardWriteForm, GoodForm
from .models import Free, Gallery, Join ,Good, ManyImg
from all_info.models import Info
from django.views.generic import ListView, DetailView, CreateView #이것도 쓰나?
from django.http import HttpResponseRedirect , HttpResponse
from django.core.paginator import Paginator #얘 쓰나?
from django.core.files.storage import FileSystemStorage #얘도 쓰나?
# from django.view.decorators.http import require_http_methods

# def test(request):
#     board_list = Free.objects.all() #models.py Free 클래스의 모든 객체를 board_list에 담음
#     # board_list 페이징 처리
#     page = request.GET.get('page', '1') #GET 방식으로 정보를 받아오는 데이터
#     paginator = Paginator(board_list, '5') #Paginator(분할될 객체, 페이지 당 담길 객체수)
#     page_obj = paginator.page(page) #페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
#     return render(request, 'template_name', {'page_obj':page_obj}) 


def text_delete(request,free_id, pk):#글삭
    login_session = request.session.get('info_id','')
    
    board = get_object_or_404(Free, free_id=pk)
    make_moim = Make_Moim.objects.get(make_id=free_id)

    if board.info.info_id == login_session:
        board.delete()
        return redirect('write:free', free_id)
    else:
        return redirect('write:free', free_id)

def text_modify(request,free_id, pk):#수정
    login_session = request.session.get('info_id','')
    make_moim = Make_Moim.objects.get(make_id=free_id)

    context = {'login_session' : login_session}

    board = get_object_or_404(Free, free_id=pk)
    context['board'] = board
    context['make_moim'] = make_moim

    if request.method == 'GET' :
        return render(request, 'write/modify.html', context)
    
    elif request.method =='POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        board.title=title
        board.text=text

        board.save()

        
        return redirect('write:free', free_id)


def view_text(request,free_id,pk): #게시물 보기
    free=Free.objects.get(free_id=pk)
    make_moim = Make_Moim.objects.get(make_id=free_id)
    return render(request, 'write/vt_free.html',{'free':free,'make_moim':make_moim })

def freeboard_index(request, free_id): #자유게인덱스
    all_boards = Free.objects.all().order_by("-write_dttm") # 모든 데이터 조회, 내림차순(-표시) 조회
    make_moim=Make_Moim.objects.get(make_moim=free_id)
    return render(request, 'write/freeindex.html', {'title':'Board List', 'board_list':all_boards})

def board_list(request):
    login_session = request.session.get('login_session','')
    context = {'login_session' : login_session}
    return render(request, 'base.html', context)

def board_free_write(request, free_id):#작성 
    login_session = request.session.get('info_id','')
    context = {'login_session' : login_session}

    make_moim = Make_Moim.objects.get(make_id=free_id)
    free=Free.objects.filter(make_moim=make_moim) #어떤 모임에서 써진 글들

    if request.method == 'GET' :
        write_form = BoardWriteForm
        context['forms'] = write_form
        context['make_moim']=make_moim
        return render(request, 'write/board_free_write.html', context)
    elif request.method =='POST':
        write_form = BoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            writer = Info.objects.get(info_id=login_session)
            board = Free(
                title=write_form.title,
                text=write_form.text,
                info=writer,
                imgfile=write_form.imgfile,
                make_moim=make_moim
                # comment=write_form.info
            )
            board.save()
            return redirect('write:free',free_id=free_id)
        
        else:
            context['forms'] = write_form
            context['make_moim']=make_moim
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'write/board_free_write.html',context)

    return render(request, 'write/board_free_write.html', context)

def free(request, free_id):
    
    make_moim=Make_Moim.objects.get(make_id=free_id)
    free_id = Free.objects.all().order_by('-pk')
    all_boards = Free.objects.all().order_by("-write_dttm")

    #페이징
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 10
    start = end - 10
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Free.objects.all().count()
    total_page = total_count//10 +1
    if page > total_page:
        page = total_page
        end = page * 10
        start = end -10
    
    if total_count % 10 !=0:
        total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page)
    all_boards = all_boards[start:end]

    context = {
        'all_boards' : all_boards,
        'page_info' : page_info,
        'total_page' : total_page,
        'e_page' : e_page,
        'page':page,
        'make_moim':make_moim,
        'free': free_id, 'board_list':all_boards,
        # 'posts' : posts
    }

    return render(
        request,
        'write/free.html',
        context
    )

def join(request):
    join_id = Join.objects.all().order_by('-pk')
    
    return render(
        request,
        'write/join.html',
        {'join': join_id}
    )

def new_face(request):
    new_face_id = Join.objects.all().order_by('-pk')
    
    return render(
        request,
        'write/new_face.html',
        {'new_face': new_face_id}
    )
def gallery(request, pk):
    make_moim=Make_Moim.objects.get(make_id=pk)
    gallery_list = Gallery.objects.all().order_by('-gallery_id')

    #페이징
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Gallery.objects.all().count()
    total_page = total_count//5 +1
    if page > total_page:
        page = total_page
        end = page * 5
        start = end -5
    
    if total_count % 5 !=0:
        total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page)
    gallery_list = gallery_list[start:end]

    context = {
        'gallery_list' : gallery_list,
        'page_info' : page_info,
        'total_page' : total_page,
        'e_page' : e_page,
        'page':page,
        'make_moim':make_moim,
        # 'posts' : posts
    }

    return render(
        request,
        'write/gallery_list.html',
        context
    )

def gallery_makeit(request, pk):
    make_moim=Make_Moim.objects.get(make_id=pk)        
    if request.method == 'GET':
            return render(request, 'write/gallery_makeit.html',{'make_moim':make_moim})
    else :
        try:
            info_id=request.session['info_id']
            id=Info.objects.get(info_id=info_id)

            # writer=request.POST.get('id')
            # Gallery.objects.filter(info=writer)

            # comments = Good.objects.filter(gallery=make_moim)#댓글임
            
            
            title = request.POST.get('title')
            comment = request.POST.get('contents')
            imgfiles = request.FILES.getlist('imgfiles')
            make_moim = request.POST.get('make_moim')


            gallery=Gallery(title=title, comment=comment , info=id, make_moim=Make_Moim.objects.get(pk=make_moim), )
            gallery.save()

            for upload_file in imgfiles:
                name = upload_file.name
                name=name.replace('.',f'{int(time.time())}.')
        
                # a.jpg -> (중복) a_unixtime.jpg
                #                a_167375584983.jpg
                with open('media/gallery/'+name, 'wb') as file:
                    
                    for chunk in upload_file.chunks():
                        # manyimg=ManyImg.objects.filter(gallery=(int(last_gallery)+1))
                        #게시글 최신->이미지1,이미지2,이미지3....
            

                        file.write(chunk)
                manyimg=ManyImg.objects.create(imgfile=name, gallery=gallery)
                manyimg.save()
            #multiple도 get으로 받나?
            #info-프라이머리키라서 어차피 1개->writer로 직접 저장 가능
        
        except Exception as e:
            print(e)
            return redirect('/login/')
    return redirect('write:gallery' ,pk)

def gallery_make(request): #이게머지???/
    gallery = Gallery.objects.all().order_by('-pk')

    if request.method == 'POST':
        #회원정보 조회
        files = request.POST.get('files')
        text = request.POST.get('text')
        title = request.POST.get('title')
        
        
        try:
            info = request.session['info']
            info_id=Info.objects.get(info_id=info)
            new_gallery = Gallery()
            new_gallery.comment =text
            new_gallery.title = title
            new_gallery.imgfile = files
            new_gallery.save()
            return HttpResponseRedirect('write:gallery')
        except:
            return render(request, 'login_fail.html')
    return render(request, 'gallery_makeit.html')

def gallery_single(request, pk, gg): #FBV로 싱글갤러리 만들기
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    manyimg=ManyImg.objects.filter(gallery=gallery_singles)

    return render(request, 'write/single_gallery.html', {'single_gallery':gallery_singles, 'make_moim':make_moim, 'manyimg':manyimg})

def gallery_delete(request, pk, gg): #FBV로 싱글갤러리 만들기
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    writer=request.POST.get('writer')
    id=request.session['info_id']
    if id==writer:
        gallery=Gallery.objects.get(gallery_id=gallery_singles.gallery_id, make_moim=make_moim)
        gallery.delete()
        return redirect('write:gallery', pk)
    else : 
        return render(request, 'write/not_authority_gallery.html',{'make_moim':make_moim})
    
def gallery_modify(request, pk, gg): #FBV로 싱글갤러리 만들기
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    writer=request.POST.get('writer')
    id=request.session['info_id']
    print(id, writer)
    if id==writer:     
        context={
            'make_moim':make_moim,'single_gallery':gallery_singles
        }
        return render(request,'write/gallery_modify.html', context)
    else : 
        return render(request, 'write/not_authority_gallery.html',{'make_moim':make_moim})

def gallery_modify2(request, pk, gg): #FBV로 싱글갤러리 만들기
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    writer=request.POST.get('writer')
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    id=request.session['info_id']
    imgfiles = request.FILES.getlist('imgfiles')
    print(imgfiles)
    if id==writer:
        gallery=Gallery.objects.get(gallery_id=gallery_singles.gallery_id,)
        gallery.comment = comment
        gallery.title = title
        gallery.save()
        # manyimgs=ManyImg.objects.filter(gallery=gallery_singles.gallery_id)
        # manyimgs.delete()
        for upload_file in imgfiles:
            name = upload_file.name
            name=name.replace('.',f'{int(time.time())}.')
    
            # a.jpg -> (중복) a_unixtime.jpg
            #                a_167375584983.jpg
            with open('media/gallery/'+name, 'wb') as file:
                
                for chunk in upload_file.chunks():
                    # manyimg=ManyImg.objects.filter(gallery=(int(last_gallery)+1))
                    #게시글 최신->이미지1,이미지2,이미지3....
        

                    file.write(chunk)
            manyimg=ManyImg.objects.create(imgfile=name, gallery=gallery)
            manyimg.save()
        
        return redirect('write:gallery',pk)
    else : 
        return render(request, 'write/not_authority_gallery.html',{'make_moim':make_moim})

def gallery_img_delete(request, pk, gg): #이미지 수정에서 이미지 삭제할때
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    manyimg_id = request.POST.get('manyimg_id')
    print(manyimg_id)
    manyimgs=ManyImg.objects.get(manyimg_id=manyimg_id)
    manyimgs.delete()
    context={
            'make_moim':make_moim,'single_gallery':gallery_singles
        }
    return render(request,'write/gallery_modify.html', context)

def gallery_modify3(request,pk,gg):
    gallery_singles = Gallery.objects.get(gallery_id=gg)
    make_moim = Make_Moim.objects.get(make_id=pk)
    context = {
        'make_moim':make_moim,'single_gallery':gallery_singles
    }
    return render(request, 'write/gallery_modify_img.html', context)

# def GalleryCreate(CreateView):
#     model = Gallery
#     field = ['title', 'comment','imgfile','info']

def download(request):
    manyimg_id = request.POST.get('manyimg_id')
    uploadFile = ManyImg.objects.get(manyimg_id=manyimg_id)
    filepath = str(settings.BASE_DIR) + (f'/media/gallery/{uploadFile.imgfile}')
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def gallery_free_write(request):
    login_session = request.session.get('login_session','')
    context = {'login_session' : login_session}
    if request.method == 'GET' :
        write_form = BoardWriteForm
        context['forms'] = write_form
        return render(request, 'write/gallery_free_write.html', context)
    
    elif request.method =='POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = Info.objects.get(user_id=login_session)
            board = Free(
                title=write_form.title,
                texts=write_form.text,
                writer=writer,
                board_name=write_form.info
            )
            board.save()
            return redirect('/gallery_write')
        
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'write/gallery_free_write.html',context)

    return render(request, 'write/gallery_free_write.html', context)

def product_create(request):
    if request.method == 'POST':
        form = BoardWriteForm(request.POST, request.FILES) # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.detailfunc = product.detailfunc.replace("'", "").replace("[", "").replace("]", "")
            product.save()
            return redirect('sales:index')
    else:
        form = BoardWriteForm() # request.method 가 'GET'인 경우
    context = {'form':form}
    return render(request, 'sales/product_form.html', context)

# @require_POST
def comments_create(request, pk, gg):
    if request.user.is_authenticated:
        free_text = get_object_or_404(Free, pk=pk)
        comment_form = GoodForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.free = free_text
            comment.free_id = request.free_id
            comment.save()
        return redirect('write:detail', free.pk)
    return redirect('accounts:login')


# @require_POST
def comments_delete(request, join_pk, comment_pk):
    if request.free_id.is_authenticated:
        comment = get_object_or_404(Good, pk=comment_pk)
        if request.free_id == comment.free_id:
            comment.delete()
    return redirect('write:detail', join_pk)

# @require_POST
def likes(request, join_pk):
    if request.free_id.is_authenticated:
        join = get_object_or_404(Free, pk=join_pk)

        if join.like_users.filter(pk=request.free_id.pk).exists():
            join.like_users.remove(request.free_id)
        else:
            join.like_users.add(request.free_id)
        return redirect('join:index')
    return redirect('accouts:login')


def get_absolute_url(self):        
    return f'/write/gallery/{self.pk}/'

#join
def join_detail(request, make_id):
    make_moim=Make_Moim.objects.get(make_id=make_id)
    join_list = Join.objects.all().order_by('-join_id')
    
#페이징
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Join.objects.all().count()
    total_page = total_count//5 +1
    if page > total_page:
        page = total_page
        end = page * 5
        start = end -5
    
    if total_count % 5 !=0:
        total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page)
    join_list = join_list[start:end]


    if request.method == 'GET':
        print('작동')
        context = {
            'join_list' : join_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }

        return render(request, 'write/join_detail.html',context)
    else:
        try:
            info_id=request.session['info_id']
            info=Info.objects.get(info_id=info_id)

            comment=request.POST.get('comment')
            title=request.POST.get('title')

            join = Join(title=title, comment=comment,info=info, make_moim=make_moim)
            join.save()
        except:
            return redirect('login')
    return redirect('write:join_detail', make_id)

def join_delete(request,make_id):#글삭
    make_moim = Make_Moim.objects.get(make_id=make_id)
    login_session = request.session['info_id']

    join_id=request.POST.get('join_id')
    writer=request.POST.get('writer')
    if login_session ==  writer:
        join=Join.objects.get(make_moim=make_moim,join_id=join_id)
        print(join)
        join.delete()
        return redirect('write:join_detail', make_id)
    else:
        return redirect('write:join_detail', make_id)

def join_modify(request,make_id):#수정
    make_moim = Make_Moim.objects.get(make_id=make_id)
    writer=request.POST.get('writer')
    join_id=request.POST.get('join_id')
    join=Join.objects.get(make_moim=make_moim,join_id=join_id)
    try: 
        id = request.session['info_id']
        if writer==id:
            context = {
                'join':join,
                'make_moim':make_moim,
                'writer':writer
            }
            return render(request, 'write/join_modify.html', context)
    except:
        return render(request, 'write/not_authority.html',{'make_moim':make_moim})

def join_modify2(request,make_id):#수정저장
    make_moim = Make_Moim.objects.get(make_id=make_id)
    writer=request.POST.get('writer')
    join_id=request.POST.get('join_id')
    title=request.POST.get('title')
    comment=request.POST.get('comment')
    id = request.session['info_id']
    if writer==id:
        make_moim = Make_Moim.objects.get(make_id=make_id)
        join=Join.objects.get(make_moim=make_moim,join_id=join_id)
        join.title=title
        join.comment=comment
        join.save()
        return redirect('write:join_detail', make_id) 
    return render(request, 'write/not_authority.html',{'make_moim':make_moim})

    
    

def join_comment(request, make_id):
    make_moim=Make_Moim.objects.get(make_id=make_id)
    join_id = request.POST.get('join_id')
    content=request.POST.get('reply_comment')
    join=Join.objects.get(join_id=join_id)
    # last_comment=request.POST.get('last_comment')
    # last_join=Join.objects.all().order_by('-join_id')[0]
    # print(last_comment,last_join.comment)
    # if last_join.comment != last_comment:
    if content is None:        
        info_id=request.session['info_id']
        info=Info.objects.get(info_id=info_id)
        
        good = Good(content=content, info=info, make_moim=make_moim,join=join)
        # good.save()
        goods = Good.objects.filter(join=join)
        # newgood=Good.objects.all().order_by('-good_id')[0]
        # newgood.delete()
        context = {
            'goods':goods,
            'make_moim':make_moim
        }
        return render(request,'write/join_comment.html',context)

    try :
        info_id=request.session['info_id']
        info=Info.objects.get(info_id=info_id)
        
        good = Good(content=content, info=info, make_moim=make_moim,join=join)
        good.save()
        goods = Good.objects.filter(join=join)
        context = {
            'goods':goods,
            'make_moim':make_moim
        }
        return render(request,'write/join_comment.html',context)
    except:
        return redirect('login')
    # return redirect('write:join_detail', make_id)

def join_comment_u(request, make_id):
    make_moim=Make_Moim.objects.get(make_id=make_id)
    good_id = request.POST.get('good_id')
    content = request.POST.get('content')
    writer = request.POST.get('writer')
    info_id=request.session['info_id']
    info=Info.objects.get(info_id=info_id)
    print(info, content, writer, good_id)
    if info.info_id == writer:
        good = Good.objects.get(good_id=good_id)
        good.content=content
        good.save()
        return redirect('write:join_detail', make_id)
    return redirect('login')

def join_comment_d(request, make_id):
    make_moim=Make_Moim.objects.get(make_id=make_id)
    good_id = request.POST.get('good_id')
    writer = request.POST.get('writer')
    info_id=request.session['info_id']
    if info_id == writer:
        good = Good.objects.get(good_id=good_id)
        print()
        good.delete()
        return redirect('write:join_detail', make_id)
    return redirect('login')


def gallery_search(request,pk):
    csb=request.POST.get('change_search_bar')
    search = request.POST.get('search')
    make_moim=Make_Moim.objects.get(make_id=pk)
    gallery_list = Gallery.objects.all().order_by('-gallery_id')
    make_moim_id = request.POST.get('make_moim')

    #페이징
    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 5
    start = end - 5
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Gallery.objects.all().count()
    total_page = total_count//5 +1
    if page > total_page:
        page = total_page
        end = page * 5
        start = end -5
    
    if total_count % 5 !=0:
        total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page)
    
    if csb == 'all':
        gallery_list = Gallery.objects.filter(title__contains=search) | Gallery.objects.filter(comment__contains=search)       
        gallery_list = gallery_list.order_by('-gallery_id')
        gallery_list = gallery_list[start:end]
        context ={
            'search':search, 'make_moim':make_moim,
            'gallery_list' : gallery_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/gallery_list.html', context)
    elif csb == 'search_title':
        gallery_list = Gallery.objects.filter(title__contains=search)
        gallery_list = gallery_list[start:end]
        context ={
            'search':search, 'make_moim':make_moim,
            'gallery_list' : gallery_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/gallery_list.html', context)       
    else :
        gallery_list =Gallery.objects.filter(comment__contains=search)
        gallery_list = gallery_list[start:end]

        context ={
            'search':search, 'make_moim':make_moim,
            'gallery_list' : gallery_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/gallery_list.html', context)
    
def free_search(request,pk):
    csb=request.POST.get('change_search_bar')
    search = request.POST.get('search')
    make_moim=Make_Moim.objects.get(make_id=pk)
    free_list = Free.objects.all().order_by('-free_id')

    page = int(request.GET.get('page',1))
    # if not page : page = '1'
    # page=int(page)
    end = page * 10
    start = end - 10
    s_page = (page-1)//10*10 + 1
    e_page = s_page +9

    #페이지 구분
    total_count = Free.objects.all().count()
    total_page = total_count//10 +1
    if page > total_page:
        page = total_page
        end = page * 10
        start = end -10
    
    if total_count % 10 !=0:
        total_page +=1

    if e_page > total_page : 
        e_page = total_page

    page_info = range(s_page, e_page)
    


    
    if csb == 'all':
        free_list = Free.objects.filter(title__contains=search) | Free.objects.filter(text__contains=search)       
        free_list = free_list.order_by('-free_id')
        free_list = free_list[start:end]
        context ={
            'search':search, 'make_moim':make_moim,
            'board_list' : free_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/free.html', context)
    elif csb == 'search_title':
        free_list = Free.objects.filter(title__contains=search)
        free_list = free_list.order_by('-free_id')
        free_list = free_list[start:end]
        context ={
            'search':search, 'make_moim':make_moim,
            'board_list' : free_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/free.html', context)       
    else :
        free_list =Free.objects.filter(text__contains=search)
        free_list = free_list.order_by('-free_id')
        free_list = free_list[start:end]

        context ={
            'search':search, 'make_moim':make_moim,
            'board_list' : free_list,
            'page_info' : page_info,
            'total_page' : total_page,
            'e_page' : e_page,
            'page':page,
            'make_moim':make_moim,
            # 'posts' : posts
        }
        return render(request, 'write/free.html', context)

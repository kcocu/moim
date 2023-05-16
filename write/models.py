from django.conf import settings
from django.db import models

from all_info import models as models2
from make_moim.models import Make_Moim
from select_moim.models import Select_Moim  # 좋아요-import setting


# Create your models here. 
class Join(models.Model):
    join_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    comment = models.CharField(max_length=200, null=True)
    info = models.ForeignKey(models2.Info, on_delete=models.CASCADE,db_column='info_id', null=True)
    write_dttm = models.DateTimeField(auto_now_add=True, null=True)
    update_dttm = models.DateTimeField(auto_now=True, null=True)
    new_face = models.TextField(verbose_name='가입인사', null=True)
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='moim_id', null=True)
    def __str__(self):
        return f'[{self.pk}][{self.title}]'

class Free(models.Model): #
    free_id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name='글 내용', null=True)
    comment = models.CharField(max_length=200, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles') #좋아요 추가
    info = models.ForeignKey(models2.Info, on_delete=models.CASCADE,db_column='info_id', null=True)
    title = models.CharField(max_length=64, verbose_name='글 제목', default='')
    write_dttm = models.DateTimeField(auto_now_add=True, null=True)
    update_dttm = models.DateTimeField(auto_now=True, null=True)
    hits=models.PositiveIntegerField(default=0)
    imgfile = models.ImageField(null=True, upload_to="", blank=True) # 이미지 컬럼 추가
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='moim_id', null=True)
    # make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='moim_id', null=True)
    # select_moim = models.ForeignKey(Select_Moim, on_delete=models.CASCADE,db_column='select_id', null=True)
    def __str__(self):
        return f'[{self.pk}][{self.title}]'

class Gallery(models.Model): #FBV로 만듬
    gallery_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='글 제목', default='')
    comment = models.CharField(max_length=200, null=True)
    picture = models.CharField(max_length=200, null=True)
    write_dttm = models.DateTimeField(auto_now_add=True, null=True)
    update_dttm = models.DateTimeField(auto_now=True, null=True)
    info = models.ForeignKey(models2.Info, on_delete=models.CASCADE,db_column='info_id', null=True)
    imgfile = models.ImageField(null=True, upload_to="gallery/%Y%m%d", blank=True) # 이미지 컬럼 추가
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='moim_id', null=True)
    select_moim = models.ForeignKey(Select_Moim, on_delete=models.CASCADE,db_column='select_id', null=True)
    
    def __str__(self):
        return f'[{self.pk}][{self.title}]'

class Good(models.Model):#댓글 연결
    good_id = models.AutoField(primary_key=True)
    free = models.ForeignKey(Free, on_delete=models.CASCADE,db_column='free_id', null=True)
    info = models.ForeignKey(models2.Info, on_delete=models.CASCADE,db_column='info_id', null=True)
    join = models.ForeignKey(Join, on_delete=models.CASCADE,db_column='join_id', null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE,db_column='gallery_id', null=True)
    select_moim = models.ForeignKey(Select_Moim, on_delete=models.CASCADE,db_column='select_id', null=True)
    content = models.CharField(max_length=200, null=True) #댓글
    # title = models.CharField(max_length=200, null=True) #제목
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.content

class ManyImg(models.Model): #이미지 여러개 업로드할려면?
    manyimg_id = models.AutoField(primary_key=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE,db_column='gallery_id', null=True)
    save_path = models.CharField(max_length=50, null=True)
    save_name = models.CharField(max_length=50, null=True)
    imgfile = models.ImageField(null=True, upload_to="gallery/%Y%m%d", blank=True) # 이미지 컬럼 추가
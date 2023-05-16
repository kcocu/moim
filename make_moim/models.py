from django.db import models




class Make_Moim(models.Model):#댓글 연결
    make_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    commend = models.TextField(verbose_name='모임소개', null=True) #소개
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    location = models.CharField(max_length=200, null=True)
    max_people = models.IntegerField(default=0)
    now_people = models.IntegerField(default=0)
    category = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return self.name




    
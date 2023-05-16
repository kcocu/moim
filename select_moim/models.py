from django.db import models

from make_moim.models import Make_Moim

# Create your models here.
class Select_Moim(models.Model):#댓글 연결
    select_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    # commend = models.CharField(max_length=200, null=True)
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='make_id', null=True)
    
    def __str__(self):
        return self.content

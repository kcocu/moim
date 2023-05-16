from django.db import models

from make_moim.models import Make_Moim

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)


    
class TagMoim(models.Model):
    tag_moim_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,db_column='tag', null=True)
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='make_id', null=True)
    apply_date = models.CharField(max_length = 20)
    join_date = models.CharField(max_length = 20)
from django.db import models

from make_moim.models import Make_Moim



class Info(models.Model):
    info_id = models.CharField(max_length = 20, primary_key=True)
    pw = models.CharField(max_length = 20, null=True)
    name = models.CharField(max_length = 20)
    region = models.CharField(max_length = 20)
    sex = models.CharField(max_length = 10)
    preference = models.CharField(max_length = 20)
    age = models.IntegerField(default=0)

class Category(models.Model):
    category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length = 20)
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length = 20, null=True)


# 김- 등산, 낚시. 책// 이 - 등산, 바둑  ...
class GroupInfo(models.Model):
    make_moim_info_id = models.AutoField(primary_key=True)
    info = models.ForeignKey(Info, on_delete=models.CASCADE,db_column='info_id', null=True)
    make_moim = models.ForeignKey(Make_Moim, on_delete=models.CASCADE,db_column='make_id', null=True)
    y_n = models.CharField(max_length = 1)
    admin = models.IntegerField(default=0)
    apply_date = models.CharField(max_length = 20)
    join_date = models.CharField(max_length = 20)
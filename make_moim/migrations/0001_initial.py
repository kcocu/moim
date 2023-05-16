# Generated by Django 4.1 on 2023-01-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tag", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Make_Moim",
            fields=[
                ("make_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, null=True)),
                ("commend", models.TextField(null=True, verbose_name="모임소개")),
                ("imgfile", models.ImageField(blank=True, null=True, upload_to="")),
                ("location", models.CharField(max_length=200, null=True)),
                ("max_people", models.IntegerField(default=0)),
                ("tags", models.ManyToManyField(blank=True, to="tag.tag")),
            ],
        ),
    ]
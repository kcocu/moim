from django.contrib import admin
from .models import Free
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
@admin.register(Free)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'free_id',
        'title',
        'comment',
        'info',
        'text',
        'write_dttm',
        'update_dttm',
        'hits',
    )
    list_display_links = list_display
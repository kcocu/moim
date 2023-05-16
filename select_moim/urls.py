from django.urls import path
from . import views  




app_name = 'select_moim'

urlpatterns = [
    path('', views.select_moim, name='select_moim'),
    path('<int:moim_id>/', views.select_moim_id, name='select_moim_id'),
    
    path('good/', views.make_good, name='make_good'),
    path('detail/<int:id>', views.make_detail, name='make_detail'),
    # path('update/<int:id>', views.make_update, name='make_update'),
]
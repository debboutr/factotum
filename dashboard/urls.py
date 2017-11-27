from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .views.dashboard import indexView
from .views.data_source import DS_List_View, DS_View

urlpatterns = [
	url(r'^$', login_required(indexView.as_view()), name='index'),
	url(r'^datasources/$', login_required(DS_List_View.as_view()), name='data_source_list'),
	url(r'^datasource/(?P<pk>\d+)$', login_required(DS_View.as_view()), name='data_source_detail'),
	url(r'^datasource/new$', views.data_source_create, name='data_source_new'),
	url(r'^datasource/edit/(?P<pk>\d+)$', views.data_source_update, name='data_source_edit'),
	url(r'^datasource/delete/(?P<pk>\d+)$', views.data_source_delete, name='data_source_delete'),
	url(r'^datagroup/new$', views.data_group_create, name='data_group_new'),
	url(r'^datagroup/(?P<pk>\d+)$', views.data_group_detail, name='data_group_detail'),
	url(r'^datagroup/edit/(?P<pk>\d+)$', views.data_group_update, name='data_group_edit'),
	url(r'^datagroup/delete/(?P<pk>\d+)$', views.data_group_delete, name='data_group_delete'),

]

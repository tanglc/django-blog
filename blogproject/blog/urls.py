from django.conf.urls import url
from . import views
app_name = 'blog'
urlpatterns = [
        #因为在视图中写的是类视图，所以在这需要点上一个as_view()把它变成一个函数
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # url(r'^search/$',views.search,name='search'),
]
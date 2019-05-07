from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	path('', views.DIYArticleListView.as_view(), name='index'),
	path('list/', views.DIYArticleListView.as_view(), name='diy_list'),
	path('create/', views.create, name='create'),
    path('article/<int:article_id>/', views.article_details, name='article-detail'),
	path('articles/<int:article_id>/', views.DIYArticleDetailView.as_view(), name='article-details'),
	path('add/<int:article_id>/', views.add_to_cart, name='add_to_cart'),          
	path('remove/<int:article_id>/', views.remove_from_cart, name='remove_from_cart'),
	path('cart/', views.cart, name='cart'),
    path('checkout/<str:processor>', views.checkout, name='checkout'),
    path('process/<str:processor>', views.process_order, name='process_order'),
    path('complete_order/<str:processor>', views.complete_order, name='complete_order'),
    path('order_error/', views.order_error, name='order_error'),
]

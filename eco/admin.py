from django.contrib import admin

from .models import Article, Author, ArticleOrder, Cart

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author','diy_package','package_quantity')

class AuthorAdmin(admin.ModelAdmin):
    list_display= ('last_name', 'first_name')
    
class ArticleOrderAdmin(admin.ModelAdmin):
    list_display= ('article', 'cart','quantity')

class CartAdmin(admin.ModelAdmin):
    list_display= ('user', 'active','order_date')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(ArticleOrder, ArticleOrderAdmin)
admin.site.register(Cart, CartAdmin)

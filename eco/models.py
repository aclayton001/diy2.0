from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from datetime import datetime



class Article(models.Model):
        author = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='User', null=True
        )
        title = models.CharField(max_length=256)
        date = models.DateTimeField(default=datetime.now)
        body = models.TextField()
        likes = models.IntegerField(default=0)
        diy_package = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
        package_quantity = models.IntegerField(default=0)
        diy_files = models.FileField(blank=False, null=False, default='kit.jpg', upload_to="kit/%Y/%m/%D")

        def _str_(self):
                return self.title

class Author(models.Model):
        last_name = models.CharField(max_length=256)
        first_name = models.CharField(max_length=256)
        def _str_(self):
                return self.author

class Cart(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        active = models.BooleanField(default=True)
        order_date = models.DateField(null=True)
        payment_type = models.CharField(max_length=100, null=True)   
        payment_id = models.CharField(max_length=100, null=True)     
    
        def add_to_cart(self,article_id):
            article = Article.objects.get(pk=article_id)
            try:
                preexisting_order = ArticleOrder.objects.get(article=article, cart=self)
                preexisting_order.quantity +=1
                preexisting_order.save()
            except ArticleOrder.DoesNotExist:
                new_order = ArticleOrder.objects.create(
                   article=article,
                   cart=self,
                   quantity=1
                )
                new_order.save()
    
        def remove_from_cart(self,article_id):
            article= Article.objects.get(pk=article_id)
            try:
                preexisting_order = ArticleOrder.objects.get(article=article, cart=self)
                if preexisting_order.quantity > 1:
                    preexisting_order.quantity -=1
                    preexisting_order.save()
                else:
                    preexisting_order.delete()
            except ArticleOrder.DoesNotExist:
               pass
    
class ArticleOrder(models.Model):
        article= models.ForeignKey(Article, on_delete=models.CASCADE)
        cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
        quantity= models.IntegerField(null=True)
        payment_type=models.CharField(max_length=100, null=True)   
        payment_id=models.CharField(max_length=100, null=True)

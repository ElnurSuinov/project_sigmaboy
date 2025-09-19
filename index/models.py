from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=32)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Категории'


class Product(models.Model):
    product_name = models.CharField(max_length=128)
    product_des = models.TextField()
    product_count = models.IntegerField()
    product_price = models.FloatField()
    product_photo = models.ImageField(upload_to='media')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Продукты'

class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_pr_amount = models.IntegerField()

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name_plural = 'Корзина'

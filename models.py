from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')

    def __str__(self):
        return self.name


class Recept(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='recepts')
    price = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f"{self.product.name} ({self.price})"


class OrderRecept(models.Model):
    recept = models.ForeignKey(Recept,
                               on_delete=models.CASCADE,
                               related_name='orders')
    order = models.OneToOneField('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order Recept for {self.recept.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        """Класс управления статусами заказов."""
        ON_WAY = 'ONW', 'В пути'
        ARRIVER = 'AR', 'Прибыл'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_shipped = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.ON_WAY)

    def __str__(self):
        return f"Order Receipt for {self.user.username}"




class ReceptDetails(models.Model):
    recept = models.OneToOneField(Recept, on_delete=models.CASCADE)
    ingredients = models.ForeignKey('Ingredient', on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.recept} - {self.ingredients}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Marker(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Storage(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    datetime_received = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
    datetime_expired = models.DateTimeField(auto_now=True)
    marker = models.ManyToManyField(Marker, blank=True)

    def __str__(self):
        ingredients_list = [str(ingredient) for ingredient in self.ingredients.all()]
        return ', '.join(ingredients_list)


class IngredientSuplier(models.Model):
    ingredient = models.ManyToManyField(Ingredient)
    suplier = models.ManyToManyField('Suplier')

    def __str__(self):
        ingredients_list = [str(ingredient) for ingredient in self.ingredient.all()]
        suppliers_list = [suplier.legacy_name for suplier in self.suplier.all()]
        return ', '.join(ingredients_list + suppliers_list)


class Suplier(models.Model):
    legacy_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200)
    phone = models.IntegerField()

    def __str__(self):
        return self.legacy_name



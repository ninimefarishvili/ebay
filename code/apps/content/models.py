from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=False)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name}".strip() or self.email

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"


class Category(models.Model):
    title = models.CharField(max_length=20, verbose_name="დასახელება")

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE)
    img_url = models.URLField(blank=True, null=True)  # Ensure this field is defined like this

    def __str__(self):
        return self.title

    listing_date = models.DateField(null=False, blank=False, default=timezone.now())
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("listing_date",)
        verbose_name = "პროდუქტი"
        verbose_name_plural = "პროდუქტები"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self) -> str:
        return f"{self.customer} - {self.created_at}"
    
    def add_to_cart(self, product, quantity=1):
        if product.quantity - quantity < 0:
            raise ValidationError("ნამეტანი ბევრი მოგივიდა, ძმა")
        
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=self,
            defaults={"quantity": quantity}
        )

        product.quantity -= quantity

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return cart_item
    
    def get_total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, 
        blank=True, 
        null=False, 
        related_name="items",
        on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        Cart,
        null=False,
        blank=False,
        related_name="cart_items",
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} - {self.cart}"
    
    def total_price(self):
        return self.quantity * self.product.price

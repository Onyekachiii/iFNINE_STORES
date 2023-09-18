from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★✩✩✩✩"),
    (2, "★★✩✩✩"),
    (3, "★★★✩✩"),
    (4, "★★★★✩"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.

# for categories
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Category Title")
    image = models.ImageField(upload_to="category", default="category.png")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

# for vendors 
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Vendor Title")
    image = models.ImageField(upload_to = user_directory_path, default="vendor.png")
    cover_image = models.ImageField(upload_to = user_directory_path, default="vendor.png")
    # description = models.TextField(null=True, blank=True, default="This is a vendor description")
    description = RichTextUploadingField(null=True, blank=True, default="This is a vendor description")
        
    contact = models.CharField(max_length=30, default = "+123 (456) 789")
    address = models.CharField(max_length=255, default="123 main street, Lagos, Nigeria")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    chat_resp_time = models.CharField(max_length=30, default="100", null=True, blank=True)
    shipping_on_time = models.CharField(max_length=30, default="100", null=True, blank=True)
    authentic_rating = models.CharField(max_length=30, default="100", null=True, blank=True)
    warranty_period = models.CharField(max_length=30, default="100", null=True, blank=True)
    
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title

# for products 
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prd", alphabet="abcdefgh12345")
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="vendor")
    
    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to = user_directory_path, default="product.png")
    # description = models.TextField(null=True, blank=True, default="This is a product description")
    description = RichTextUploadingField(null=True, blank=True, default="This is a product description")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=2.99)
    
    # specifications = models.TextField(null=True, blank=True, default="This is a product specification")
    specifications = RichTextUploadingField(null=True, blank=True, default="This is a product specification")
    stock_count = models.CharField(max_length=100, default="10")
    mfd_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    tags = TaggableManager (blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=5, max_length=20, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.old_price - self.price) / self.old_price * 100
        return new_price
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.SET_NULL, null=True)
    images = models.ImageField(upload_to = "product-images", default="product.png")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
    
####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################


class CartOrder(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"
        

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))
    
    
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################


class ProductReview(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    rating = models.IntegerField(choices=RATING, default=None)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
    
class WishList(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "WishLists"
    
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=150, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Address"
    
    
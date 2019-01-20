from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class ActiveCategoryManager(models.Manager):
    """ Manager class to return only those categories where each instance is active """
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=200,blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveCategoryManager()
 
    class Meta:
        # db_table = 'categories'
        ordering = ('-created',)
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_category',args=[self.slug])

class ActiveProductManager(models.Manager):
    """ Manager class to return only those products where each instance is active """
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(available=True)
    
class FeaturedProductManager(models.Manager):
    """ Manager class to return only those products where each instance is featured """
    def get_query_set(self):
        return super(FeaturedProductManager, self).get_query_set().filter(available=True).filter(is_featured=True)
        
class Product(models.Model):
    """ model class containing information about a product; instances of this class are what the user
    adds to their shopping cart and can subsequently purchase
    
    """
    name = models.CharField(max_length=190, db_index=True)
    slug = models.SlugField(max_length=190, db_index=True)
    sku = models.CharField(max_length=50, default='')
    brand = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)

    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)


    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()

   
    tags = TaggableManager()


    class Meta:
        # db_table = 'products'
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])
        #return ('catalog_product', (), { 'product_slug': self.slug }
    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

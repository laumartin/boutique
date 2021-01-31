from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    # create a string method which takes in the category model itself.
    # and just returns self.name
    def __str__(self):
        return self.name

    # model method here is the same thing as the string method except
    # this one is going to return the friendly name if we want it.
    def get_friendly_name(self):
        return self.friendly_name


# The first field is a foreign key to the category model.We'll allow this to
# be null in db and blank in forms and if a category is deleted we'll set any
# products that use it to have null this field rather than deleting product.
class Product(models.Model):
    # each product requires a name, a description, and a price.
    # But everything else is optional by adding the nulls and blanks =true
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

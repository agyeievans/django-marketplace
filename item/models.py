from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    # create model name and show categories name
    class Meta:
        # order by name
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
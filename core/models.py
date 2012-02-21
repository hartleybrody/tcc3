from django.db import models

# Create your models here.

# class Account(models.Model):
    # first_name =        models.CharField(max_length=30)
    # last_name =         models.CharField(max_length=40)
    # email =             models.EmailField() # validate on client side that it's .edu
    # password = 
    # location =          models.CharField(max_length=128)
    
# NOTE: the above models might be better suited by django admin app. we'll see


class Visitor(models.Model):
    first_visit         = models.DateTimeField(auto_now_add=True)
    # last_visit        = models.DateTimeField(auto_now_add=True)
    # current_visit     = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return str(self.first_visit)

class Post(models.Model):
    site           = models.CharField(max_length=5)
    url            = models.URLField(unique=True)
    title          = models.CharField(max_length=255)
    img_url        = models.URLField()
    published      = models.DateTimeField()
    
    def __unicode__(self):
        return self.title
    
class Post_Access(models.Model):
    date            = models.DateTimeField(auto_now_add=True)
    site            = models.CharField(max_length=5)
    rating          = models.SmallIntegerField()
    type_of_access  = models.CharField(max_length=12)
    post            = models.ForeignKey(Post)
    visitor         = models.ForeignKey(Visitor)
    
    def __unicode__(self):
        return self.date      
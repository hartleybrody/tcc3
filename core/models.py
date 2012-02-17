from django.db import models

# Create your models here.

# class User(models.Model):
    # location =          models.CharField(max_length=128)
    
    ## might want to put some of this in cookies/localStorage
    # first_visit =       models.DateTimeField(auto_now_add=True)
    # last_visit =        models.DateTimeField(auto_now_add=True)
    # current_visit =     models.DateTimeField(auto_now_add=True)

# class Account(models.Model):
    # first_name =        models.CharField(max_length=30)
    # last_name =         models.CharField(max_length=40)
    # email =             models.EmailField() # validate on client side that it's .edu
    # password = 
    
# NOTE: the above models might be better suited by django admin app. we'll see

class Post(models.Model):
    site           = models.CharField(max_length=5)
    url            = models.URLField()
    title          = models.CharField(max_length=255)
    img_URL        = models.URLField()
    published      = models.DateTimeField()
    
    def __unicode__(self):
        return self.title
        
    # class Meta:
        # ordering = ['published']
    
class Post_Access(models.Model):
    date            = models.DateTimeField(auto_now_add=True)
    site            = models.CharField(max_length=5)
    rating          = models.SmallIntegerField()
    type_of_access  = models.CharField(max_length=12)
    post            = models.ForeignKey(Post)
    #user            = models.ForeignKey(User)
    
    def __unicode__(self):
        #return u"visited %s on %s" % (self.site, str(self.date)
        return self.date
        
    # class Meta:
        # ordering = ['date']
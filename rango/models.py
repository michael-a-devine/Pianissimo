from django.db import models

from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime
	
class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        class Meta:
                verbose_name_plural = 'categories'

        def __str__(self): # For Python 2, use __unicode__ too
                return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

class Piece(models.Model):
	title = models.CharField(max_length=128)
	artist = models.CharField(max_length=50)
	uploader = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	rating = models.IntegerField(default=5)
	description = models.CharField(max_length=300)
	imgfile = models.ImageField(default='')
	date = models.DateTimeField(default=datetime.now())
	
class Comment(models.Model):
        song = models.ForeignKey(Piece)
        name = models.ForeignKey(User)
        image = models.ImageField(default='')
        comment = models.CharField(max_length=300)
        score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
	
    # The additional attributes we wish to include.
    website = models.URLField()
    bio = models.CharField(default = " ", max_length=500)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username

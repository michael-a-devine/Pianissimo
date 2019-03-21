from django.db import models

from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

from django.db.models import Avg
	
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
	
	title = models.CharField(max_length=128, primary_key=True)
	artist = models.CharField(max_length=50)
	uploader = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	score = models.FloatField(default=5)
	
	def rate(self):
		rec = Comment.objects.values('song').annotate(Avg('score'))
		
		for song in rec:
			if song['song'] == self.title:
				mod = Piece.objects.get(title = song['song'])
				mod.score = song['score__avg']
				mod.save()
				return song['score__avg']
			
		return 5.0
		
			
	rating = property(rate)	
	
	
	
	
	description = models.CharField(max_length=300)
	imgfile = models.ImageField(default='',upload_to='sheets')
	date = models.DateTimeField(default=datetime.now())
	def __str__(self):
		return self.title

	
class Comment(models.Model):
	song = models.ForeignKey(Piece)
	name = models.ForeignKey(User)
	#image = models.ImageField(default='',upload_to='profile_images')
	comment = models.CharField(max_length=300)
	score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	def __str__(self):
		return str(self.song) + " - " + str(self.name)

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

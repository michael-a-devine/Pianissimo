
from django.contrib import admin
from rango.models import Category, Page, Piece, Comment
from rango.models import UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.

class PieceAdmin(admin.ModelAdmin):
	list_display =('title','category','uploader','rating')
	prepopulated_fields = {'slug':('title',)}
	
class CommentAdmin(admin.ModelAdmin):
	list_display=('song','name','score')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)

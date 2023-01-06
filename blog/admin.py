from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post) #connect to the Tables Post from .models
class PostAdmin(SummernoteModelAdmin):
	#  This is the way to display the content on admin 
	list_display = ('title', 'slug', 'status', 'created_on') 
	#. This add a searching bar and will look on title and content
	search_fields = ['title', 'content']
	# When something typed into title fields it will reflect on slug fields also
	prepopulated_fields = {'slug': ('title',)}
	# This will create a summernote pad for the bloc of text content for editing
	summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

	list_display = ('name', 'body', 'post', 'created_on', 'approved')
	list_filter = ('approved', 'created_on')
	search_fields = ('name', 'emai', 'body')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(approved=True)
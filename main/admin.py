from django.contrib import admin
from  .models import Post
# Register your models here.

@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    #actions_on_bottom=True
    empty_value_display='-empty-'
    #fields=[]                           #list of fields which will be displayed in admin site
    fieldsets = (
      
        ('qolgani', {
            "fields": ('title','content','image',('width','height'),
                
            ),
        }),

    )
    list_display=('title','slug','id','timestamp',)
    list_editable=['title']
    list_display_links=['timestamp']
    list_filter=('content','title')
    #list_display_links=None




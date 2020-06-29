from django.contrib import admin
from  .models import Post
from django.contrib.contenttypes.models import ContentType
# Register your models here.

@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    #actions_on_bottom=True
    empty_value_display='-empty-'
    #fields=[]                           #list of fields which will be displayed in admin site
    fieldsets = (
      
        ('qolgani', {
            "fields": ('title','content','image',('width','height'),'drafts'
                
            ),
        }),

    )
    list_display=('title','drafts','slug','id','timestamp',)
    list_editable=['title','drafts']
    list_display_links=['timestamp']
    list_filter=('content','title')
    #list_display_links=None



admin.site.register(ContentType)
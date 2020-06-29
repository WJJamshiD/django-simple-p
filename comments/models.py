from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class CommentManager(models.Manager):
    def all(self):
        qs=super(CommentManager,self).filter(parent=None)
        return qs

    def filter_by_instance(self,instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        obj_id=instance.id
        qs=super().filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content=models.TextField()
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=CommentManager()

    class Meta:
        ordering=['-timestamp']

    def __str__(self):
        return str(self.object_id)

    def children(self):
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse("comment_thread", kwargs={"id": self.id})
   
    def get_delete_url(self):
        return reverse("comment_delete", kwargs={"id": self.id})

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

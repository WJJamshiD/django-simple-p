from django.db import models
from django.urls import reverse
from django.utils.text import slugify 
import itertools
from django.db.models.signals import pre_save
from django.conf import settings
from markdown_deux import markdown
from django.utils.html import mark_safe
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time
# Create your models here.




class PostManager(models.Manager):
	def all(self,*args,**kwargs):
		return super(PostManager,self).filter(drafts=False)



def upload_path(instan,file):
	return '{0}/{1}'.format(instan.title,file)
		

class Post(models.Model):
	title=models.CharField(max_length=50)
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	update=models.DateTimeField(auto_now_add=False,auto_now=True)
	image=models.ImageField(upload_to=upload_path,height_field='height',width_field='width')
	height=models.IntegerField(default=0)
	width=models.IntegerField(default=0)
	slug=models.SlugField(unique=True)
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	drafts=models.BooleanField(default=True)
	read_time=models.IntegerField(default=2)

	objects=PostManager()

	def __str__(self):
		return self.title

	def get_markdown(self):
		content=markdown(self.content)
		return mark_safe(content)
   
	def get_absolute_url(self):
		return reverse("post_detail", kwargs={"slug": self.slug})

	@property
	def comments(self):
		instance=self
		qs=Comment.objects.filter_by_instance(instance=instance)
		return qs
	
	@property
	def content_type(self):
		instance=self
		c_type=ContentType.objects.get_for_model(model=instance.__class__)
		return c_type.model
	
	#              creating unique slug (1)
	# def generate_slug(self):
	# 	max_length = self._meta.get_field('slug').max_length
	# 	value = self.title
	# 	slug_candidate = slug_original = slugify(value, allow_unicode=True)
	# 	for i in itertools.count(1):
	# 		if not Post.objects.filter(slug=slug_candidate).exists():
	# 			break
	# 		slug_candidate = '{}-{}'.format(slug_original, i)

	# 	self.slug = slug_candidate

	# def save(self, *args, **kwargs):
	# 	if not self.pk:
	# 		self.generate_slug()

	# 	super().save(*args, **kwargs)



	class Meta:
		ordering=['-timestamp']




#             creating unique slug (2)
def create_myslug(instan,new_slug=None):
	slug=slugify(instan.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	if qs.exists():
		new_slug='{}-{}'.format(slug,qs.first().id)
		return create_myslug(instan,new_slug=new_slug)
	return slug

		
def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_myslug(instance)
	if instance.content:
		read_time=get_read_time(instance.get_markdown())
		instance.read_time=read_time
		

pre_save.connect(pre_save_post_receiver,Post)
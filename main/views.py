from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Post
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import PostForm
from django.contrib import messages 
from django.db.models import Q
from .utils import get_read_time
# Create your views here.

def post_list(request):
    if request.method=='GET':
        posts=Post.objects.all()
        keyword=request.GET.get('qqq')
        if keyword:
            query=posts.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword))
            posts=query
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form=PostForm()
        context={
            'posts':posts,
            'form':form,
            'page_obj':page_obj,
            'kw':keyword,
            
        }
        return render(request,'index.html',context)
    
        

def post_detail(request,slug=None):
    obj=get_object_or_404(Post,slug=slug)
    initial_data={
        "content_type":obj.content_type,
        "object_id":obj.id
    }
    form=CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type=form.cleaned_data['content_type']
        obj_id=form.cleaned_data['object_id']
        content=form.cleaned_data['content']
        #parent_id=form.cleaned_data['parent_id']
        content_type=ContentType.objects.get( model=c_type)
        parent_obj=None
        try:
            parent_id=int(request.POST.get('parent_id'))
        except:
            parent_id=None
        if parent_id:
            parent_qs=Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj=parent_qs.first()
        new_comment,created=Comment.objects.get_or_create(content_type=content_type,
                                                        object_id=obj_id,
                                                        content=content,
                                                        user=request.user,
                                                        parent=parent_obj)
        return HttpResponseRedirect(obj.get_absolute_url())                                
    else:
        print(form.errors)
    comments=obj.comments
    context={
        'post':obj,
        'comments':comments,
        'form':form,
    }
    return render(request,'detail.html',context)


def post_delete(request,abc=None):
    if request.method=='GET':
        if not request.user.is_staff and not request.user.is_superuser:
            raise Http404
        obj=get_object_or_404(Post,slug=slug)
        #obj=Post.objects.get(slug=slug)
        obj.delete()
        messages.info(request,'Message deleted!')
        return redirect('post_list')   

def post_edit(request,slug=None):
    post=get_object_or_404(Post,slug=slug)
    form=PostForm(request.POST or None,request.FILES or None,instance=post)
    if request.method=='GET':
        context={
            'form':form,
        }
        return render(request,'post_form.html',context)
    if request.method=='POST':
        
        if form.is_valid():
            data=form.save(commit=False)
            data.save()
            messages.success(request,'Succesfully edited!')
            return HttpResponseRedirect(data.get_absolute_url())
        else: 
            messages.error(request,'Smth went wrong, try again!')
            context={'form':form,
                    }
            return render(request, 'post_form.html',context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('post_list')
    if request.method=='GET':
        form=PostForm()
        context={
            'form':form,
        }
        return render(request,'post_form.html',context)
    if request.method=='POST':
        form=PostForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Succesfully creted!')
            return HttpResponseRedirect(data.get_absolute_url())
        else: 
            messages.error(request,'Smth went wrong, try again!')
            context={'form':form,
                    }
            return render(request, 'post_form.html',context)


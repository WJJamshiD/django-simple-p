from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,Http404,HttpResponse
from .models import Comment
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
# Create your views here.

def comment_thread(request,id):
    #obj=get_object_or_404(Comment,id=id)
    try:
        obj=Comment.objects.get(id=id)
    except:
        raise Http404
    if not obj.is_parent:
        obj=obj.parent
    initial_data={
        "content_type":obj.content_type.id,
        "object_id":obj.id
    }
    form=CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type=form.cleaned_data['content_type']
        obj_id=form.cleaned_data['object_id']
        content=form.cleaned_data['content']
        #parent_id=form.cleaned_data['parent_id']
        content_type=ContentType.objects.get( id=c_type)
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
    context={
        'comment':obj,
        'form':form,
    }

    return render(request,'comment_thread.html',context)


@login_required
def comment_delete(request,id):
    #obj=get_object_or_404(Comment,id=id)
    try:
        obj=Comment.objects.get(id=id)
    except:
        raise Http404
    if obj.user!=request.user:
        response=HttpResponse("You do not have permission to do this.")
        response.status_code=403
        return response

    parent_url=obj.content_object.get_absolute_url()
    if request.method=='POST':
        obj.delete()
        messages.add_message(request,messages.INFO,'Comment deleted!')
        return HttpResponseRedirect(parent_url)
    context={
        'comment':obj,
        'parent_url':parent_url
    }
    return render(request,'comment_delete.html',context)
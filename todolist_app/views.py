from django.shortcuts import render ,redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method =="POST":
        form=Taskform(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.manage=request.user
            instance.save()
            messages.success(request,('New Task Added successfully'))
        return redirect('todolist')
    else:       
        all_tasks=Tasklist.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})
    
@login_required
def delete_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    if task.manage==request.user:
        task.delete()
        messages.success(request,('Task Deleted successfully'))
        
    else:
        messages.error(request,'Access Denied')
    return redirect('todolist')


@login_required
def edit_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    form =Taskform(request.POST or None,instance=task)
    if form.is_valid():
            form.save()
    if request.method =="POST":
        messages.success(request,('Task Edited successfully'))
        return redirect('todolist')
    else:       
        tasks_obj =Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'tasks_obj':tasks_obj})
    
@login_required  
def complete_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    if task.manage==request.user:
        task.done=True
        task.save()
        messages.success(request,(' Task is changed to Completed'))
        
    else:
        messages.error(request,'Access Denied')
    return redirect('todolist')
   

@login_required
def pending_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    task.done=False
    task.save()
    
    messages.success(request,(' Task is changed to Pending'))
    return redirect('todolist')

def index(request):
    context ={
        'index_text' : 'welcome to the Index page'
        }
    return render(request,'index.html',context)

def contact(request):
    context ={
        'contact_text' : 'welcome to the contact us page,User!!'
        }
    return render(request,'contact.html',context)

def about(request):
    context ={
        'about_text' : 'welcome to the about us page,User!!'
        }
    return render(request,'about.html',context)
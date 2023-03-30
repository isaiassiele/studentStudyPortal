from django.shortcuts import render,redirect
from . models import Notes
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/home.html')


############################# NOTES ##################################################################################################################################



# To redirect to notes and list all belonging to the current user and if form is submitted proccess the info to the database 
@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user= request.user,title =request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added by {request.user.username} Sucessfully  ")
    else:
            form = NotesForm()
    # form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes":notes, 'form': form}
    return render(request,'dashboard/notes.html',context)


# To delete the note using the primary key of the note database
@login_required
def delete_note(request, pk =None ):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


#Create generic view to show a detailed info ,using built-in detail view
class NotesDetailsView(generic.DetailView):
    model = Notes   


######################### HOMEWORK ########################## HOMEWORK ########################### HOMEWORK #########################
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished= request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(user= request.user,
            subject =request.POST['subject'],
            title =request.POST['title'],
            description = request.POST['description'],
            due = request.POST['due'],
            is_finished= finished)
            homeworks.save()
        messages.success(request,f"Homework added by {request.user.username} Sucessfully  ")
    else:
            form = HomeworkForm()
    
    homework= Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context= {'homeworks':homework,'homework_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)
login_required
def update_homework(request,pk=None):
    homework= Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk =None ):
    Homework.objects.get(id=pk).delete()
    return redirect("homework") 


######################### Youtube ##############################################################################################

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video= VideosSearch(text,limit= 10)
        result_list = []
        for i in video.result()['result']:
            result_dict={
'input':text,
'title':i['title'],
'duration':i['duration'],
'thumbnail':i['thumbnails'][0]['url'],
'channel':i['channel']['name'],
'link':i['link'],
'views':i['viewCount']['short'],
'published':i['publishedTime'],

            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results':result_list
            }


    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/youtube.html',context)
     

######################### TO-DO ###############################
@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished= True
                else:
                    finished = False
            except: 
                finished =False
           
            todos = Todo(
                user= request.user,
                title =request.POST['title'], 
                is_finished = finished
                )
            todos.save()
        messages.success(request,f"Todo added by {request.user.username} Sucessfully  ")
    else:
            form = TodoForm()
    
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos': todo,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html', context)

@login_required	
def update_todo(request,pk=None):
    todo= Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk =None ):
    Todo.objects.get(id=pk).delete()
    return redirect("todo") 
######################### BOOKS ##############################################################################################

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict={

        'title':answer['items'][i]['volumeInfo']['title'],
        'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
        'description':answer['items'][i]['volumeInfo'].get('description'),
        'count':answer['items'][i]['volumeInfo'].get('pageCount'),
        'categories':answer['items'][i]['volumeInfo'].get('categories'),
        'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
        'preview':answer['items'][i]['volumeInfo'].get('previewLink'),


            }
            if (answer['items'][i]['volumeInfo'].get('imageLinks')):
                result_dict['thumbnail']=answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail')


           
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results':result_list
            }


    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/books.html',context)
    
######################### DICTIONARY ###############################
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_us/"+text
        r = requests.get(url)
        answer = r.json()
        print(text)
        print(answer)
        result_list = []
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context= {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio': audio,
                'definition':definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
             'input':''
                 
            }



    else:
        form = DashboardForm()
        context = {'form':form}
   
    return render(request,'dashboard/dictionary.html',context)


######################### WIKI ###############################
def wiki(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        search = wikipedia.page(text,auto_suggest=False)
        
        if (search.title):
            context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details': search.summary
        }
    else:

        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/wiki.html',context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
    
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for  {username} Sucessfully!!!  ")
        return redirect("login")
    else:
        form = UserRegistrationForm()
    context= {
        'form': form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished= False,user=request.user)
    todos = Todo.objects.filter(is_finished= False,user=request.user)
    if len(homeworks)==0:
        homework_done = True
    else:
        homework_done= False
    if len(todos)==0:
        todos_done = True
    else:
        todos_done= False

    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }

    return render(request,'dashboard/profile.html',context)
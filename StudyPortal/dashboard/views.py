from django.shortcuts import render, redirect
from .models import Notes, Homework
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user, title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request, f"Notes Added Successfully By {request.user.username}")
        return redirect('notes')
        
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes' : notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)


def notes_delete(request, pk = None):
    Notes.objects.get(id = pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes
    
    
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST) 
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
                
            homework = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homework.save()
            messages.success(request, f'Homework added form {request.user.username}!!')
        return redirect('homework')
            
    else:
        form = HomeworkForm()
    homeworks =  Homework.objects.filter()
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homework' : homeworks, 'homework_done' : homework_done, "form": form}
    return render(request, 'dashboard/homework.html', context)
    
    
def update_homework(request, pk):
    homework = Homework.objects.get(id = pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request, id):
    homework = Homework.objects.get(id = id).delete()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit = 10)
        result_list = []
        
        for i in video.result()['result']:
            
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
            'form': form,
            'results' : result_list
        }
        return render(request, 'dashboard/youtube.html', context)
    
    else:
        form = DashboardForm()
    context = {'form' : form}
    return render(request, 'dashboard/youtube.html', context)


def todo(request):
    todo = Todo.objects.filter(user = request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
                
            todo = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todo.save()
            messages.success(request, f'To do added successfully from {request.user}')
        return redirect('todo')
    else:
        form = TodoForm()
    context = {'todos' : todo, 'form' : form}
    return render(request, 'dashboard/todo.html', context)

def update_todo(request, id):
    todo = Todo.objects.get(id = id)
    if todo.is_finished:
        todo.is_finished = False
    else:
         todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request, id):
    Todo.objects.get(id = id).delete()
    return redirect('todo')

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        r.raise_for_status()
        answer = r.json()
        
        result_list = []

        
    
        for i in range(10):    
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                #'subtitle' : answer['items'][i]['volumeInfo']['subtitle'],
                'description' : answer['items'][i]['volumeInfo']['description'],
                'count' : answer['items'][i]['volumeInfo']['pageCount'],
                'categories' : answer['items'][i]['volumeInfo']['categories'],
                #'rating' : answer['items'][i]['volumeInfo']['averageRating'],
                'thumbnail' : answer['items'][i]['volumeInfo']['imageLinks']['thumbnail'],
                'preview' : answer['items'][i]['volumeInfo']['previewLink'],
                
                
            }
            result_list.append(result_dict)
        
        context = {
            'form': form,
            'results' : result_list
        }
        return render(request, 'dashboard/books.html', context)
    
    else:
        form = DashboardForm()
    context = {'form' : form}
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        r.raise_for_status()
        answer = r.json()
        print('first line------------------->\n',answer[0]['phonetics'])
        print()
        print('second line------------------->\n', answer[0]['meanings'][1])
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            difinition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][1]['definitions'][1]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            
            context = {
                'form': form,
                'phonetics' : phonetics,
                'audio' : audio,
                'definition' : difinition,
                'example' : example,
                'synosyms' : synonyms,
                'input' : text,
            }
        except:
            context = {
                'form' : form,
                'input' : text,
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
    context = {'form' : form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        print('------------------------------------------------------------------>')
        print(search.summary)
        print('--------------------------------------------------------------->')
        context = {
            'form' : form,
            'title' : search.title,
            'link' : search.link,
            'details' : search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    form = DashboardForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/wiki.html', context)
from django.shortcuts import render, redirect
from .models import Notes, Homework
from .forms import NotesForm
from django.contrib import messages
from django.views import generic

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
    homeworks =  Homework.objects.filter()
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homework' : homeworks, 'homework_done' : homework_done}
    return render(request, 'dashboard/homework.html', context)
    
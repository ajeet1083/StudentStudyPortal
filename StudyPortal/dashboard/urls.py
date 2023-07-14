from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name = 'home'),
    path('notes', views.notes, name = 'notes'),
    path('notes_delete/<int:pk>/', views.notes_delete, name='notes_delete'),
    path('note_detail/<int:pk>/', views.NotesDetailView.as_view(), name='note_detail'),
    path('homework', views.homework, name= 'homework'),
    path('update-homework/<int:pk>/', views.update_homework, name= 'update_homework'),
    path('delete-homework/<int:id>/', views.delete_homework, name= 'delete_homework'),
    path('youtube', views.youtube, name='youtube'),
    path('todo', views.todo, name='todo'),
    path('update_todo/<int:id>/', views.update_todo, name= 'update_todo'),
    path('delete_todo/<int:id>/', views.delete_todo, name= 'delete_todo'),
    path('books', views.books, name='books'),
    path('dictionary', views.dictionary, name='dictionary'),
    path('wiki', views.wiki, name='wiki'),
    path('conversion', views.conversion, name='conversion'),
    
    
    
    
]
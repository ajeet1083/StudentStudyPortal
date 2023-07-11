from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name = 'home'),
    path('notes', views.notes, name = 'notes'),
    path('notes_delete/<int:pk>/', views.notes_delete, name='notes_delete'),
    path('note_detail/<int:pk>/', views.NotesDetailView.as_view(), name='note_detail'),
    path('homework', views.homework, name= 'homework')
    
    
    
]
from django.urls import path,include
from . import views

urlpatterns = [
    # path('categories', views.GetCategories.as_view()),
    # path('regions', views.GetRegions.as_view()),
    path('projects', views.GetProjects.as_view()),
    path('project', views.GetProject.as_view()),
    path('add_project', views.AddProject.as_view()),
    path('add_sintez', views.AddSintez.as_view()),
    path('sintez', views.GetSintez.as_view()),

]

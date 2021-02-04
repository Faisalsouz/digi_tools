from django.urls import path
from tp_scraper import views

urlpatterns=[path('',views.show_db,name='main'),
             path('scraper',views.scraper_main,name='scraper_main'),
             path('instructions',views.how_to,name='how'),
             path('new_run',views.output,name='new_run'),
             path('old_run',views.output,name='old_run'),
             path('zip_files', views.download_zip, name='getzip'),
             ] #you need to give name of functionpath("<int:pk>/", views.project_detail, name="project_detail")

from core import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('permissions_list/', views.PermissionsListCreate.as_view()),
    path('add_applications/', views.ModuleListCreate.as_view()),
    path('applications_list/', views.ModuleList.as_view()),
    path('edit_applications/<pk>/', views.EditModuleById.as_view()),
    path('add_role/', views.RoleListCreate.as_view()), #add role and list of role
    path('edit_role/<pk>/', views.RoleRetrieveUpdateAPIView.as_view()), #add role and list of role

]
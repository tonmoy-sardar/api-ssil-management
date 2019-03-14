from django.shortcuts import render
from rest_framework import generics
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import Permission
# from django.contrib.auth.models import *
from core.serializers import *
from rest_framework.response import Response
from rest_framework import filters
# permission checking
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
#get_current_site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

class PermissionsListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    queryset =TCorePermissions.objects.all()
    serializer_class = TCorePermissionsSerializer
    filter_backends = (filters.SearchFilter,)
    def get_queryset(self):
        queryset = TCorePermissions.objects.all()
        cp_u = self.request.query_params.get('cp_u', None)
        cp_g = self.request.query_params.get('cp_g', None)
        cp_o = self.request.query_params.get('cp_o', None)
        print("cp_u: {}, cp_g: {}, cp_o: {}".format(cp_u, cp_g, cp_o))

        if cp_u and cp_g and cp_o:
            queryset = TCorePermissions.objects.filter(cp_u = cp_u, cp_g = cp_g, cp_o = cp_o)
        return queryset


class ModuleListCreate(generics.ListCreateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset =TCoreModule.objects.filter(cm_is_deleted=False)
    serializer_class = TCoreModuleSerializer



    # def list(self, request, *args, **kwargs):
    #     response = super(ModuleListCreate, self).list(request, args, kwargs)
    #     response_dict = response.data
    #     for data in response_dict:
    #         data['cm_icon'] = "http://"+get_current_site(request).domain+ settings.MEDIA_URL + data['cm_icon']
    #         print(data['cm_icon'])
    #     print("response_dict: ", type(response_dict))
    #     return response



class ModuleList(generics.ListAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset =TCoreModule.objects.all()
    serializer_class = TCoreModuleListSerializer

    # def list(self, request, *args, **kwargs):
    #     response = super(ModuleListCreate, self).list(request, args, kwargs)
    #     response_dict = response.data
    #     for data in response_dict:
    #         data['cm_icon'] = "http://"+get_current_site(request).domain+ settings.MEDIA_URL + data['cm_icon']
    #         print(data['cm_icon'])
    #     print("response_dict: ", type(response_dict))
    #     return response

class EditModuleById(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreModule.objects.all()
    serializer_class =TCoreModuleSerializer


class RoleListCreate(generics.ListCreateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreRole.objects.all()
    serializer_class =TCoreRoleSerializer
        


class RoleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """docstring for ClassName"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = TCoreRole.objects.all()
    serializer_class =TCoreRoleSerializer
# from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import Permission
from django.contrib.auth.models import *
from master.models import *
from core.models import *
# from users.serializers import *
from master.serializers import *
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
# pagination
from pagination import CSLimitOffestpagination,CSPageNumberPagination
# numpy.py
import numpy as np
# collections 
import collections
from django.db import transaction
from rest_framework.views import APIView
from threading import Thread          #for threading
from django.db.models import Q




class UserModuleRoleListCreate(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    queryset =TMasterModuleRole.objects.filter(mmr_user__isnull=False).order_by('-id')
    serializer_class = UserListSerializer

class ModuleRoleCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    queryset =TMasterModuleRole.objects.all()
    serializer_class = ModuleRoleSerializer

class ModuleRoleRelationMapping(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    serializer_class = ModuleRoleSerializer
    lookup_fields = ('mmr_module_id',)
    def get_queryset(self):
        try:
            mmr_module_id = self.kwargs['mmr_module_id']
            return TMasterModuleRole.objects.filter(mmr_module_id=mmr_module_id, mmr_role__cr_parent_id=0).order_by('-mmr_role__cr_parent_id')
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e, 'error': e})
            
    def get_child_list(self, role_id:int)->list:
        try:
            childlist = []
            childlist_data = TCoreRole.objects.filter(cr_parent_id = role_id)

            for child in childlist_data:
                data_dict = collections.OrderedDict()
                # print('child::',child)
                data_dict['id'] = child.id
                data_dict['cr_name'] = child.cr_name
                data_dict['cr_parent_id'] = child.cr_parent_id
                data_dict['child'] = self.get_child_list(role_id=child.id)
                # print('data_dict:: ', data_dict)
                childlist.append(data_dict)
            return childlist

        except Exception as e:
            raise e
    def list(self, request, *args, **kwargs):
        try:
            response = super(ModuleRoleRelationMapping, self).list(request, args, kwargs)
            results = response.data
            data_list = []

            for mmr_data in results:

                mmr_id = mmr_data['id']
                mmr_module = mmr_data['mmr_module']
                
                role_id = mmr_data['mmr_role']['id']
                role_parent_id= mmr_data['mmr_role']['cr_parent_id']

                if role_parent_id:
                    data = mmr_data['mmr_role']
                    data['mmr_id'] = mmr_id
                    data['mmr_module'] = mmr_module
                
                mmr_role_dict = mmr_data['mmr_role']
                mmr_role_dict['mmr_id'] = mmr_id
                mmr_role_dict['mmr_module'] = mmr_module
                   
                mmr_role_dict['child'] = self.get_child_list(role_id=role_id)
                data_list.append(mmr_role_dict)
                
                

            result_dict = collections.OrderedDict()
            result_dict['relation_list'] = data_list
            response.data = [result_dict]
            return response
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e, 'error': e})



class FreeModuleRoleList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # pagination_class =CSPageNumberPagination
    # queryset =TMasterModuleRole.objects.all()
    serializer_class = ModuleRoleSerializer
    def get_queryset(self):
        mmr_module_id = self.kwargs['mmr_module_id']
        return TMasterModuleRole.objects.filter(mmr_module_id=mmr_module_id, mmr_user__isnull=True).order_by('-mmr_role__cr_parent_id')



class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset =TMasterModuleRole.objects.filter(mmr_user__isnull=False).order_by('-id')
    serializer_class = UserListSerializer
    pagination_class =CSPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('mmr_user__username', )

    def get_queryset(self):
        mmr_module_id = self.kwargs['mmr_module_id']
        queryset = self.queryset.filter(mmr_module_id=mmr_module_id)
        return queryset.filter(~Q(mmr_user_id=self.request.user.id))


    def list(self, request, *args, **kwargs):
        try:
            temp_user_id = 0
            response = super(UserList, self).list(request, args, kwargs)
            response_dict = response.data['results']
            user_ids = list(set([each_data["mmr_user"]["id"] for each_data in response_dict]))
            result_list = list()
            for u_id in user_ids:
                result_dict = collections.OrderedDict()
                applications = list()
                mmr_user = list()
                for item in response_dict:
                    if item["mmr_user"]["id"] == u_id:
                        # print(u_id)
                        mmr_user = item["mmr_user"]
                        # user_details = item["user_details"]
                        data_dict = collections.OrderedDict()
                        data_dict['mmr_module'] = item['mmr_module']
                        data_dict['mmr_module']['mmr_permissions'] = item['mmr_permissions']
                        data_dict['mmr_module']['mmr_role'] = item['mmr_role']
                        applications.append(data_dict)
                    if mmr_user and applications:
                        result_dict['mmr_user'] = mmr_user
                        user_details_data = TCoreUserDetail.objects.get(cu_user_id=mmr_user["id"])
                        result_dict['mmr_user']['user_details'] = {"id":user_details_data.id,
                                                                   "cu_emp_code": user_details_data.cu_emp_code,
                                                                   "cu_phone_no": user_details_data.cu_phone_no,
                                                                   "cu_super_set": user_details_data.cu_super_set
                                                                   }
                        result_dict['mmr_user']['applications'] = applications
                # print(result_dict)
                result_list.append(result_dict)

            response.data['results'] = result_list
            return response
        except Exception as e:
            raise e
            

class CloneModuleRole(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        """Clone Roles from given Module to given Module
        like as (clone_module-roles/module id ,where from clone/module id ,where to clone/)
        1. Raplicate module must be blank
        2. clone only Role
        3.transaction is avilable
        4.Thread is avilable
        """
        try:
            clone_from_id = kwargs['clone_from']
            clone_to_id = kwargs['clone_to']
            with transaction.atomic():
                clone_from_data = TMasterModuleRole.objects.filter(mmr_module_id = clone_from_id, mmr_role__cr_parent_id=0)
                clone_to_data_count = TMasterModuleRole.objects.filter(mmr_module_id = clone_to_id).count()

                if clone_to_data_count:
                    raise APIException("{} roles is exiest on the Module delete them first ..".format(clone_to_data_count))
                for data in clone_from_data:
                    role_id = data.mmr_role.id
                    role_name = data.mmr_role.cr_name
                    parent_id = data.mmr_role.cr_parent_id
                    clone_thread = Thread(target=self.clone_child, args=(role_id, clone_to_id, role_name, parent_id))
                    clone_thread.start()
                    # self.get_child_list(role_id=role_id,role_name=role_name, module_id = clone_to_id, parent_id=parent_id)
                    # print("*"*100)

            return Response({'request_status': 1, 'msg': "Clone is Done"})
        except Exception as e:
            # raise e
            print(e)
            raise APIException({'request_status': 0, 'msg': e})

    def clone_child(self, role_id: int, module_id: int, role_name: str, parent_id: int):
        """This is a Recursive Functions.
        call using parent role and it will be call self
        and insert the role data using
        own parameters """
        try:
            with transaction.atomic():
                # app_details = TCoreModule.objects.get(pk=module_id)
                # app_name = app_details.cm_name
                # clone_data = {"cr_name":role_name + "({})".format(app_name),
                #         "cr_parent_id":parent_id,
                #         "cr_created_by":self.request.user}

                clone_data = {"cr_name": role_name,
                              "cr_parent_id": parent_id,
                              "cr_created_by": self.request.user}
                print("clone_data: ", clone_data)
                added_role_id = self.clone_role_add(role_data=clone_data, module_id=module_id)
                childlist_data = TCoreRole.objects.filter(cr_parent_id=role_id)
                for child in childlist_data:
                    self.clone_child(role_id=child.id, module_id=module_id, role_name=child.cr_name, parent_id=added_role_id)
            return True

        except Exception as e:
            raise e

    def clone_role_add(self, role_data: dict, module_id: int):
        """Insert into TCoreRole and TMasterModuleRole"""
        try:
            with transaction.atomic():
                clone_role_add = TCoreRole.objects.create(**role_data)
                clone_role_module_add = TMasterModuleRole.objects.create(mmr_module_id=module_id,
                                                                         mmr_role=clone_role_add)
                print('clone_role_add: ', clone_role_add)
                print('clone_role_module_add: ', clone_role_module_add)
                return clone_role_add.pk
        except Exception as e:
            raise e



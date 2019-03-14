from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import *
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings
# from rest_framework.validators import *

from drf_extra_fields.fields import Base64ImageField # for image base 64


class TCorePermissionsSerializer(serializers.ModelSerializer):
    cp_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TCorePermissions
        fields = ('id','cp_u','cp_g', 'cp_o','cp_created_by')

    # def create(self, validated_data):
    #     permissions = super(TCorePermissionsSerializer, self).create(validated_data)
    #     permissions.save()
    #     return permissions

class TCoreModuleSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    # cm_icon = Base64ImageField()
    cm_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # cm_name = serializers.CharField(required=True)
    # cm_url = serializers.CharField(required=True)
    class Meta:
        model = TCoreModule
        fields = ('id','cm_name', 'cm_icon','cm_desc','cm_url','cm_permissions', 'cm_created_by', 'cm_is_editable')




class TCoreModuleListSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    # cm_icon = Base64ImageField()    
    cm_permissions = TCorePermissionsSerializer()
    class Meta:
        model = TCoreModule
        fields = ('id','cm_name', 'cm_icon','cm_desc','cm_url','cm_permissions')


        
class TCoreRoleSerializer(serializers.ModelSerializer):
    """docstring for ClassName"""
    cr_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TCoreRole
        fields = ('id','cr_name', 'cr_parent_id', 'cr_created_by')

    # def update(self, instance, validated_data):
    #     instance.cr_updated_by = 1
        
        

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from master.models import *
from core.models import *
from core.serializers import *
from users.serializers import *
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings


class UserListSerializer(serializers.ModelSerializer):
    mmr_role = TCoreRoleSerializer()
    mmr_module = TCoreModuleSerializer()
    mmr_permissions = TCorePermissionsSerializer()
    mmr_user = UserSerializer()
    # mmr_user = UserDetailsSerializer(many=True, read_only=True)


    class Meta:
        model = TMasterModuleRole        
        # fields = ('id','mmr_module', 'mmr_permissions','mmr_role','mmr_user', 'user_details')
        fields = ('id', 'mmr_module', 'mmr_permissions', 'mmr_role', 'mmr_user')


class ModuleRoleSerializer(serializers.ModelSerializer):
    mmr_role = TCoreRoleSerializer()
    class Meta:
        model = TMasterModuleRole        
        fields = ('id','mmr_module', 'mmr_role')
    def create(self, validated_data):
        try:
            data = {}
            logdin_user_id = self.context['request'].user.id
            role_dict = validated_data.pop('mmr_role')

            # print('validated_data: ', validated_data['mmr_module'])
            role = TCoreRole.objects.create(**role_dict, cr_created_by_id=logdin_user_id)
            if role:
                module_role_data = TMasterModuleRole.objects.create(mmr_module = validated_data['mmr_module'], mmr_role=role)
                data['id'] = module_role_data.pk
                data['mmr_module'] = module_role_data.mmr_module
                data['mmr_role'] = module_role_data.mmr_role            

            return data
        except Exception as e:
            # raise e
            raise serializers.ValidationError({'request_status': 0, 'msg': 'error', 'error': e})


            

 
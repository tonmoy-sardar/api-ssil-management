from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from pms.models import *
from django.contrib.auth.models import *
import time
from django.db import transaction, IntegrityError
from drf_extra_fields.fields import Base64ImageField
import os
from rest_framework.exceptions import APIException

#:::::::::: TENDER AND TENDER DOCUMENTS  ::::::::#
class TenderEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenders
        fields = ('id','updated_by','tender_final_date',
                  'tender_opened_on','tender_added_by','tender_received_on',
                  'tender_aasigned_to')
class TenderDocumentAddSerializer(serializers.ModelSerializer):
    tender_document = serializers.FileField(required=False)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    tender_documents = serializers.ListField(required=False)
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderDocuments
        fields = ('id','tender','document_name','tender_document',
                  'created_by','owned_by','status','tender_documents')
class TenderDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenders
        fields = ("id",'updated_by','status','is_deleted')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.updated_by = validated_data.get('updated_by')
                instance.is_deleted = True
                instance.status = False
                instance.save()
                pmsTenderDocuments = PmsTenderDocuments.objects.get(tender=instance.id)
                pmsTenderDocuments.status = False
                pmsTenderDocuments.is_deleted = True
                pmsTenderDocuments.save()
                return instance
        except Exception as e:
            raise e
class TenderDocsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderDocuments
        fields = ('id','document_name','updated_by')
class TenderDocumentDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderDocuments
        fields = ("id",'updated_by','status','is_deleted')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.updated_by = validated_data.get('updated_by')
                instance.is_deleted = True
                instance.status = False
                instance.save()
                return instance
        except Exception as e:
            raise e
class TendersAddSerializer(serializers.ModelSerializer):
    tender_g_id = serializers.CharField(required=False)
    #tender_documents = TenderDocumentAddSerializer(many=True)
    created_by=serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by=serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenders
        fields = ('id','tender_g_id',"tender_final_date","tender_opened_on",
                  "tender_added_by",'tender_received_on','tender_aasigned_to',
                  'created_by','owned_by','status')
    def create(self, validated_data):
        try:
            tender_id = "T" + str(int(time.time()))
            #print('tender_id', tender_id)
            created_by = validated_data.get('created_by')
            #print('created_by',created_by)
            owned_by = validated_data.get('owned_by')
            with transaction.atomic():
                tender_save_id = PmsTenders.objects.create(
                        tender_g_id=tender_id,
                        tender_final_date=validated_data.get('tender_final_date'),
                        tender_opened_on=validated_data.get('tender_opened_on'),
                        tender_added_by=validated_data.get('tender_added_by'),
                        tender_received_on=validated_data.get('tender_received_on'),
                        tender_aasigned_to=validated_data.get('tender_aasigned_to'),
                        created_by=created_by,
                        owned_by=owned_by
                       )
                response_data={
                    'id':tender_save_id.id,
                    'tender_g_id':tender_save_id.tender_g_id,
                    'tender_final_date': tender_save_id.tender_final_date,
                    'tender_opened_on': tender_save_id.tender_opened_on,
                    'tender_added_by': tender_save_id.tender_added_by,
                    'tender_received_on': tender_save_id.tender_received_on,
                    'tender_aasigned_to': tender_save_id.tender_aasigned_to,
                    'created_by':tender_save_id.created_by,
                    'owned_by':tender_save_id.owned_by,
                    }
                return response_data

        except Exception as e:
            raise e

#:::::::::: TENDER  BIDDER TYPE :::::::::::::::#
class VendorsAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderVendors
        fields='__all__'
class VendorsMappingSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tender_bidder_type = serializers.CharField(required=False)
    status = serializers.HiddenField(default=1)
    tender_vendor = VendorsAddSerializer()
    class Meta:
        model=PmsTenderBidderTypeVendorMapping
        fields=('id','tender_bidder_type','tender_vendor',
                'status','created_by','owned_by')
class TendorBidderTypeAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    vendors = serializers.ListField(required=False)
    type_of_partner = serializers.IntegerField(required=False)
    class Meta:
        model=PmsTenderBidderType
        fields=('id','tender','bidder_type','type_of_partner','responsibility',
                'profit_sharing_ratio_actual_amount',
                'profit_sharing_ratio_tender_specific_amount','created_by',
                'owned_by','vendors','status')
    def create(self, validated_data):
        try:
            tender_bidder_type_vendor_mapping_list=[]
            with transaction.atomic():
                if validated_data.get('bidder_type') == 'individual':
                    tender_bidder_type = PmsTenderBidderType.objects.create(tender=validated_data.get('tender'),
                                                                            bidder_type=validated_data.get(
                                                                                'bidder_type'),
                                                                            responsibility=validated_data.get(
                                                                                'responsibility'),
                                                                            status=validated_data.get('status'),
                                                                            created_by=validated_data.get('created_by'),
                                                                            owned_by=validated_data.get('owned_by')

                                                                            )
                    response = {
                        'id': tender_bidder_type.id,
                        'tender': tender_bidder_type.tender,
                        'bidder_type': tender_bidder_type.bidder_type,
                        'created_by': tender_bidder_type.created_by,
                        'owned_by': tender_bidder_type.owned_by,
                    }
                    return response
                else:
                    tender_bidder_type=PmsTenderBidderType.objects.create(
                        tender=validated_data.get('tender'),
                        bidder_type=validated_data.get('bidder_type'),
                        type_of_partner=validated_data.get('type_of_partner'),
                        responsibility=validated_data.get('responsibility'),
                        profit_sharing_ratio_actual_amount=validated_data.get('profit_sharing_ratio_actual_amount'),
                        profit_sharing_ratio_tender_specific_amount=validated_data.get('profit_sharing_ratio_tender_specific_amount'),
                        status = validated_data.get('status'),
                        created_by=validated_data.get('created_by'),
                        owned_by=validated_data.get('owned_by'))

                    for vendor in validated_data.get('vendors'):
                        print('vendor',vendor)
                        request_dict = {
                                    "tender_bidder_type_id": str(tender_bidder_type),
                                    "tender_vendor_id": int(vendor),
                                    "status": True,
                                    "created_by": validated_data.get('created_by'),
                                    "owned_by": validated_data.get('owned_by')
                                   }
                        tender_bidder_type_vendor_m, created=PmsTenderBidderTypeVendorMapping.objects.get_or_create(**request_dict)
                        tender_bidder_type_vendor_mapping_list.append({
                                "id" : tender_bidder_type_vendor_m.tender_vendor.id,
                                "name": tender_bidder_type_vendor_m.tender_vendor.name
                            })
                    #print('tender_bidder_type_vendor_mapping_list',tender_bidder_type_vendor_mapping_list)
                    response={
                        'id':tender_bidder_type.id,
                        'tender':tender_bidder_type.tender,
                        'bidder_type':tender_bidder_type.bidder_type,
                        'type_of_partner':tender_bidder_type.type_of_partner,
                        'responsibility':tender_bidder_type.responsibility,
                        'profit_sharing_ratio_actual_amount':tender_bidder_type.profit_sharing_ratio_actual_amount,
                        'profit_sharing_ratio_tender_specific_amount':tender_bidder_type.profit_sharing_ratio_tender_specific_amount,
                        'created_by':tender_bidder_type.created_by,
                        'owned_by':tender_bidder_type.owned_by,
                        'vendors':validated_data.get('vendors')

                    }
                    return response
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TendorBidderTypeEditSerializer(serializers.ModelSerializer):
    updated_by=serializers.CharField(default=serializers.CurrentUserDefault())
    vendors = serializers.ListField(required=True)
    class Meta:
        model=PmsTenderBidderType
        fields = ( 'id', 'bidder_type','type_of_partner', 'responsibility',
                   'profit_sharing_ratio_actual_amount',
                   'profit_sharing_ratio_tender_specific_amount', 'updated_by','vendors')

    def update(self, instance, validated_data):
        try:
            tender_bidder_type_vendor_mapping_list = []
            with transaction.atomic():
                instance.bidder_type = validated_data.get('bidder_type', instance.bidder_type)
                instance.type_of_partner=validated_data.get('type_of_partner',instance.type_of_partner)
                print('instance.type_of_partner',instance.type_of_partner)
                instance.responsibility=validated_data.get('responsibility',instance.responsibility)
                instance.profit_sharing_ratio_actual_amount=validated_data.get('profit_sharing_ratio_actual_amount',instance.profit_sharing_ratio_actual_amount)
                instance.profit_sharing_ratio_tender_specific_amount=validated_data.get('profit_sharing_ratio_tender_specific_amount',instance.profit_sharing_ratio_tender_specific_amount)
                instance.updated_by=validated_data.get('updated_by',instance.updated_by)
                instance.save()

                xyz=PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=instance.id).delete()
                print('xyz',xyz)

                for vendor in validated_data.get('vendors'):
                    request_dict = {
                        "tender_bidder_type_id": str(instance.id),
                        "tender_vendor_id": vendor['tender_vendor_id'],
                        "status": True,
                        "created_by": validated_data.get('created_by'),
                        "owned_by": validated_data.get('owned_by')
                    }
                    tender_bidder_type_vendor_m, created = PmsTenderBidderTypeVendorMapping.objects.get_or_create(
                        **request_dict)
                    tender_bidder_type_vendor_mapping_list.append({
                        "id": tender_bidder_type_vendor_m.tender_vendor.id,
                        "name": tender_bidder_type_vendor_m.tender_vendor.name
                    })

                response = {
                    'id': instance.id,
                    'tender': instance.tender,
                    'bidder_type': instance.bidder_type,
                    'type_of_partner':  instance.type_of_partner,
                    'responsibility': instance.responsibility,
                    'profit_sharing_ratio_actual_amount':  instance.profit_sharing_ratio_actual_amount,
                    'profit_sharing_ratio_tender_specific_amount':  instance.profit_sharing_ratio_tender_specific_amount,
                    'updated_by': instance.updated_by,
                    'vendors': tender_bidder_type_vendor_mapping_list

                }
                return response
        except Exception as e:
            raise e
class TendorBidderTypeDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderBidderType
        fields=('id','type_of_partner', 'responsibility', 'profit_sharing_ratio_actual_amount',
        'profit_sharing_ratio_tender_specific_amount','status','is_deleted','updated_by','created_by','owned_by')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.status=False
            instance.is_deleted=True
            instance.save()

            PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=instance.id).update(status=False,is_deleted=True)

            response_data={ 'id':instance.id,
                            'tender': instance.tender,
                            'bidder_type': instance.bidder_type,
                            'type_of_partner': instance.type_of_partner,
                            'responsibility': instance.responsibility,
                            'profit_sharing_ratio_actual_amount': instance.profit_sharing_ratio_actual_amount,
                            'profit_sharing_ratio_tender_specific_amount': instance.profit_sharing_ratio_tender_specific_amount,
                            'created_by':instance.created_by,
                            'updated_by': instance.updated_by,
                            'owned_by': instance.owned_by,
                            'status':instance.status,
                            'is_deleted':instance.is_deleted
            }

            return  response_data


#:::::::::: TENDER  ELIGIBILITY :::::::::::::::#
class PmsTenderEligibilityAddSerializer(serializers.ModelSerializer):
    """Eligibility is added with the required parameters,
     using 2 table 'PmsTenderEligibility' and 'PmsTenderEligibilityFieldsByType'
     uniquely added on 'PmsTenderEligibility',
     transaction is exist,
     APIException is used. """
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    eligibility_type = serializers.CharField(required=True)
    eligibility_status = serializers.BooleanField(required=False)
    eligibility_fields = serializers.ListField(required=True)
    tender_id = serializers.IntegerField(required=True)
    class Meta:
        model = PmsTenderEligibility
        fields = ('id', 'tender_id', 'eligibility_type', 'eligibility_status', 'eligibility_fields', 'created_by')

    def create(self, validated_data):
        self.eligibility_status = True
        try:
            fields_result_list = list()
            current_user = validated_data.get('created_by')
            tender_id = validated_data.pop('tender_id') if "tender_id" in validated_data else 0
            eligibility_type = validated_data.pop('eligibility_type') if "eligibility_type" in validated_data else ""
            ineligibility_reason = validated_data.pop(
                'ineligibility_reason') if "ineligibility_reason" in validated_data else ""
            eligibility_fields = validated_data.pop('eligibility_fields')
            with transaction.atomic():
                if tender_id:
                    tender_eligibility_dict = {}
                    tender_eligibility_dict['tender_id'] = tender_id
                    tender_eligibility_dict['type'] = eligibility_type
                    tender_eligibility_dict['created_by'] = current_user
                    tender_eligibility_dict['owned_by'] = current_user

                    add_tender_eligibility,  created= PmsTenderEligibility.objects.get_or_create(**tender_eligibility_dict)
                    PmsTenderEligibilityFieldsByType.objects.filter(tender_id=tender_id,
                                                                    tender_eligibility_id=add_tender_eligibility.id).delete()
                    for fields_data in eligibility_fields:
                        print("fields_data: ", fields_data)
                        fields_data['tender_id'] = tender_id
                        fields_data['tender_eligibility'] = add_tender_eligibility
                        fields_data['created_by'] = current_user
                        fields_data['owned_by'] = current_user
                        print("eligibility_status: ", self.eligibility_status)
                        if not fields_data['eligible']:
                            self.eligibility_status = False



                        add_tender_eligibilityfields_by_type = PmsTenderEligibilityFieldsByType.objects.create(**fields_data)
                        added_fields = {"id": add_tender_eligibilityfields_by_type.id,
                                        "tender_id": add_tender_eligibilityfields_by_type.tender_id,
                                        "tender_eligibility_id": add_tender_eligibilityfields_by_type.tender_eligibility_id,
                                        "field_label": add_tender_eligibilityfields_by_type.field_label,
                                        "field_value": add_tender_eligibilityfields_by_type.field_value,
                                        "eligible": add_tender_eligibilityfields_by_type.eligible
                                        }
                        fields_result_list.append(added_fields)
                    if not self.eligibility_status:
                        PmsTenderEligibility.objects.filter(pk=add_tender_eligibility.id).update(
                            eligibility_status=False)
                    else:
                        PmsTenderEligibility.objects.filter(pk=add_tender_eligibility.id).update(
                            eligibility_status=True)
                    result_dict = {
                        "id": add_tender_eligibility.id,
                       "tender_id": add_tender_eligibility.tender.id,
                        "eligibility_type": add_tender_eligibility.type,
                        "eligibility_status": self.eligibility_status,
                       "eligibility_fields": fields_result_list
                                   }
            return result_dict
        except Exception as e:
            print("error: ", e)
            raise APIException({'request_status': 0, 'msg': e})
class PmsTenderEligibilityFieldsByTypeEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderEligibilityFieldsByType
        fields = ("id", "tender", "tender_eligibility", "field_label", "field_value", "eligible", "updated_by")
class PmsTenderNotEligibilityReasonAddSerializer(serializers.ModelSerializer):
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderEligibility
        fields = ("id", "tender", "ineligibility_reason",
                  "eligibility_status", "updated_by")

    def update(self, instance, validated_data):
        instance.ineligibility_reason = validated_data.get("ineligibility_reason",instance.ineligibility_reason)
        instance.save()
        return instance

#::::::::::::::: TENDER SURVEY SITE PHOTOS:::::::::::::::#
class TenderSurveySitePhotosAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveySitePhotos
        fields=('id','tender','latitude','longitude','address','additional_notes',
                'document','document_name','status','created_by','owned_by')
    def create(self, validated_data):
        try:
            survey_site_photos=PmsTenderSurveySitePhotos.objects.create(**validated_data)
            response_data={
                'id':survey_site_photos.id,
                'tender':survey_site_photos.tender,
                'latitude':survey_site_photos.latitude,
                'longitude':survey_site_photos.longitude,
                'address':survey_site_photos.address,
                'additional_notes':survey_site_photos.additional_notes,
                'document':survey_site_photos.document,
                'document_name': survey_site_photos.document_name,
                'status':survey_site_photos.status,
                'created_by':survey_site_photos.created_by,
                'owned_by':survey_site_photos.owned_by

            }
            return response_data
        except Exception as e:
            raise e
class TenderSurveySitePhotosEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveySitePhotos
        fields=('id','tender','latitude','longitude','address','additional_notes',
                'document','document_name','updated_by')
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.latitude=validated_data.get('latitude',instance.latitude)
                instance.longitude=validated_data.get('longitude',instance.longitude)
                instance.address=validated_data.get('address',instance.address)
                instance.additional_notes=validated_data.get('additional_notes',instance.additional_notes)
                instance.updated_by=validated_data.get('updated_by',instance.updated_by)
                instance.document_name=validated_data.get('document_name',instance.document_name)
                existing_image='./media/' + str(instance.document)
                if validated_data.get('document'):
                    if os.path.isfile(existing_image):
                        os.remove(existing_image)
                    instance.document = validated_data.get('document', instance.document)
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveySitePhotosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveySitePhotos
        fields = '__all__'
class TenderSurveySitePhotosDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveySitePhotos
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

#::::::::::::::: TENDER SURVEY COORDINATE :::::::::::::::#
class TenderSurveyLocationAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveyCoordinatesSiteCoordinate
        fields=('id','tender','name','latitude','longitude','address','status','created_by','owned_by')
    def create(self, validated_data):
        try:
            location_request=PmsTenderSurveyCoordinatesSiteCoordinate.objects.create(**validated_data)
            response_data={
                'id':location_request.id,
                'tender':location_request.tender,
                'name': location_request.name,
                'latitude':location_request.latitude,
                'longitude':location_request.longitude,
                'address':location_request.address,
                'status':location_request.status,
                'created_by':location_request.created_by,
                'owned_by':location_request.owned_by
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveyLocationEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyCoordinatesSiteCoordinate
        fields=('id','tender','name','latitude','longitude','address','updated_by')
class TenderSurveyLocationDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyCoordinatesSiteCoordinate
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                response_data = {'id': instance.id,
                                 'tender': instance.tender,
                                 'name':instance.name,
                                 'latitude': instance.latitude,
                                 'longitude': instance.longitude,
                                 'address': instance.address,
                                 'created_by': instance.created_by,
                                 'updated_by': instance.updated_by,
                                 'owned_by': instance.owned_by,
                                 'status': instance.status,
                                 'is_deleted': instance.is_deleted
                                 }
                return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderSurveyCOSupplierAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model=PmsTenderSurveyCoordinatesSuppliers
        fields=('id','tender','type','tender_survey_material','supplier_name','contact',
                'latitude','longitude','address','document','document_name','status',
                'created_by','owned_by')
class TenderSurveyCOSupplierEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyCoordinatesSuppliers
        fields=('id','tender','type','tender_survey_material','supplier_name','contact',
                'latitude','longitude','address','document','document_name','status',
                'created_by','owned_by','updated_by')
class TenderSurveyCOSupplierDeleteSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyCoordinatesSuppliers
        fields = '__all__'
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.status = False
                instance.is_deleted = True
                instance.save()
                return instance
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

#::::::::::: TENDER SURVEY RESOURCE ::::::::::::::::::::#
class TenderSurveyMaterialsAddSerializer(serializers.ModelSerializer):
    status=serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyMaterials
        fields=('id','name','unit','status','created_by','owned_by')
class TenderSurveyMaterialsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyMaterials
        fields=('id','name','unit','updated_by')
class TenderSurveyMaterialsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=PmsTenderSurveyMaterials
        fields='__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        response_data = {'id': instance.id,
                         'name': instance.name,
                         'unit': instance.unit,
                         'created_by': instance.created_by,
                         'updated_by': instance.updated_by,
                         'owned_by': instance.owned_by,
                         'status': instance.status,
                         'is_deleted': instance.is_deleted
                         }

        return response_data
class TenderSurveyMaterialsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyMaterials
        fields = '__all__'

#::::::::::: TENDER SURVEY RESOURCE METERIAL ::::::::::::::::::::#
class TenderSurveyResourceMaterialAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = ('id','tender','tender_survey_material','supplier_name','contact','latitude','longitude',
                  'address','document_name','document','status','created_by','owned_by')
class TenderSurveyResourceMaterialEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = ('id','supplier_name','contact','latitude','longitude',
                  'address','document_name','document','updated_by')
    def update(self, instance, validated_data):
        try:
            instance.supplier_name=validated_data.get('supplier_name')
            instance.contact=validated_data.get('contact')
            instance.latitude=validated_data.get('latitude')
            instance.longitude=validated_data.get('longitude')
            instance.address=validated_data.get('address')
            instance.document_name=validated_data.get('document_name',instance.document_name)
            instance.updated_by=validated_data.get('updated_by',instance.updated_by)
            existing_image='./media/' + str(instance.document)
            if validated_data.get('document'):
                if os.path.isfile(existing_image):
                    os.remove(existing_image)
                instance.document = validated_data.get('document', instance.document)
            instance.save()
            return instance

        except Exception as e:
            raise APIException({'request_status': 0,'msg':e})
class TenderSurveyResourceMaterialDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance
class TenderSurveyResourceMaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceMaterial
        fields = '__all__'

#:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
class TenderSurveyResourceHydrologicalAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = ("id", 'tender', "name", 'details', 'latitude', 'longitude', 'address', "created_by",
                  "owned_by", 'status')
class TenderSurveyResourceHydrologicalEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = ("id","name", 'details', 'latitude', 'longitude', 'address', "updated_by"
                  )
class TenderSurveyResourceHydrologicalDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceHydrological
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceHydrologicalDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document", "created_by", "owned_by",'status')

    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                      model_class="PmsTenderSurveyResourceHydrological")
        return survey_document_data
class TenderSurveyResourceHydrologicalDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document", "updated_by")

    def update(self, instance, validated_data):
        instance.module_id = validated_data.get('module_id')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceHydrologicalDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
class TenderSurveyResourceContractorsOVendorsContractorAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = ('id', 'tender','name','details','latitude','longitude','address', 'status', 'created_by','owned_by')
class TenderSurveyResourceContractorsOVendorsContractorEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = ('id','name','details','latitude','longitude','address','updated_by')
class TenderSurveyResourceContractorsOVendorsContractorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsContractor
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance
class TenderSurveyResourceContractorsOVendorsContractorDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document", "created_by", "owned_by")

    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                      model_class="PmsTenderSurveyResourceContractorsOVendorsContractor")
        return survey_document_data
class TenderSurveyResourceContractorsOVendorsContractorDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document","updated_by")
    def update(self, instance, validated_data):
        instance.module_id=validated_data.get('module_id')
        instance.document_name=validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorModelMasterAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster
        fields = ("id", "name", "created_by", "owned_by", 'status')
class TenderSurveyResourceContractorsOVendorsVendorAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = (
        "id", 'tender', "name", 'model', 'hire', 'khoraki', 'latitude', 'longitude', 'address', "created_by",
        "owned_by", 'status')
class TenderSurveyResourceContractorsOVendorsVendorEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = ("id", "name", 'model', 'hire', 'khoraki', 'latitude', 'longitude', 'address', "updated_by")
class TenderSurveyResourceContractorsOVendorsVendorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContractorsOVendorsVendor
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorDocumentAddSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "tender", "module_id", "document_name", "document", "created_by", "owned_by")

    def create(self, validated_data):
        survey_document_data = PmsTenderSurveyDocument.objects.create(**validated_data,
                                                                      model_class="PmsTenderSurveyResourceContractorsOVendorsVendor")
        return survey_document_data
class TenderSurveyResourceContractorsOVendorsVendorDocumentEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyDocument
        fields = ("id", "module_id", "document_name", "document", "updated_by")

    def update(self, instance, validated_data):
        instance.module_id = validated_data.get('module_id')
        instance.document_name = validated_data.get('document_name')
        instance.updated_by = validated_data.get('updated_by')
        existing_image = './media/' + str(instance.document)
        if validated_data.get('document'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.document = validated_data.get('document')
        instance.save()
        return instance
class TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyDocument
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()
        return instance

#:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
class TenderSurveyResourceContactDesignationAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsTenderSurveyResourceContactDesignation
        fields=('id','tender','name','status','created_by','owned_by')
class TenderSurveyResourceContactDetailsAddSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = ('id', 'designation', 'field_label', 'field_value', 'status', 'created_by', 'owned_by')
class TenderSurveyResourceContactDetailsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = ('id', 'designation', 'field_label', 'field_value',
                  'updated_by')
class TenderSurveyResourceContactDetailsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsTenderSurveyResourceContactDetails
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = False
        instance.is_deleted = True
        instance.save()

        return instance

#::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
class TenderInitialCostingUploadFileSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(required=False)
    field_value = serializers.CharField(required=False)
    class Meta:
        model=PmsTenderInitialCosting
        fields=('id','tender','document')
    def create(self, validated_data):
        try:
            #tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
            import pandas as pd
            import xlrd
            df = pd.read_excel(validated_data.get('document'))
            print("Column headings:")
            print(df.columns)
            for j in df.columns:
                print(df[j])
                # tender_initial_costing_label = PmsTenderInitialCostingExcelFieldLabel.\
                #     objects.create(
                #     tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                #     field_label=j
                #
                # )
                for i in df.index:
                    # tender_initial_costing_field = PmsTenderInitialCostingExcelFieldValue. \
                    #     objects.create(
                    #     tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                    #     initial_costing_field_label=tender_initial_costing_label,
                    #     field_value=df[j][i]
                    #
                    # )
                    print(df[j][i])

            response_data={
                'id':tender_initial_costing.id,
                'tender':tender_initial_costing.tender,
                'field_label':df.columns,
                'field_value':'',
                'document': tender_initial_costing.document,
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})
class TenderInitialCostingAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    #tender_initial_costing = serializers.CharField(required=False)
    #field_label = serializers.CharField(required=False)
    #field_value = serializers.CharField(required=False)
    #initial_costing_field_label = serializers.CharField(required=False)
    field_label_value = serializers.ListField(required=False)
    class Meta:
        model=PmsTenderInitialCosting
        fields=('id','tender','client','tender_notice_no_bid_id_no','name_of_work',
                'is_approved','received_estimate','quoted_rate','difference_in_budget',
                'document','status','created_by','owned_by','field_label_value')
    def create(self, validated_data):
        try:
            #print('validated_data',validated_data)
            field_label_value = validated_data.pop('field_label_value')
            tender_existing_data = PmsTenderInitialCosting.objects.get(tender=validated_data['tender'])
            print('tender_existing_data',tender_existing_data)
            if tender_existing_data:
                print('tender_existing_data11111', tender_existing_data.id)
                tender_existing_field_label = PmsTenderInitialCostingExcelFieldLabel.objects.filter(
                    tender_initial_costing=tender_existing_data.id).delete()

                tender_existing_field_value = PmsTenderInitialCostingExcelFieldValue.objects.filter(
                    tender_initial_costing=tender_existing_data.id).delete()



            else:
                print('tender_not_exist')
                tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
                for each_field_label_value in field_label_value:
                    #print('each_field_label_value',each_field_label_value['field_label'])
                    tender_initial_costing_label = PmsTenderInitialCostingExcelFieldLabel.\
                        objects.create(
                        tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                        field_label=each_field_label_value['field_label']
                    )
                    for field_value in each_field_label_value['field_value']:
                        tender_initial_costing_field = PmsTenderInitialCostingExcelFieldValue. \
                            objects.create(
                            tender_initial_costing=PmsTenderInitialCosting.objects.get(pk=1),
                            initial_costing_field_label=tender_initial_costing_label,
                            field_value=field_value

                        )
                    #print(df[j][i])

            response_data={
                'id':tender_initial_costing.id,
                'tender':tender_initial_costing.tender,
                'client': tender_initial_costing.client,
                'tender_notice_no_bid_id_no':tender_initial_costing.tender_notice_no_bid_id_no,
                'name_of_work':tender_initial_costing.name_of_work,
                'is_approved':tender_initial_costing.is_approved,
                'received_estimate': tender_initial_costing.received_estimate,
                'quoted_rate': tender_initial_costing.quoted_rate,
                'difference_in_budget': tender_initial_costing.difference_in_budget,
                'document': tender_initial_costing.document,
                'status':tender_initial_costing.status,
                'created_by':tender_initial_costing.created_by,
                'owned_by':tender_initial_costing.owned_by,
                'field_label_value':field_label_value
            }
            return response_data
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

#:::::::::::: PMS PROJECTS ::::::::::::::::::::::::::::#
class ProjectsAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = PmsProjects
        fields = ('id', 'name', 'tender', 'latitude',
                  'longitude', 'address', 'created_by', 'owned_by', 'status')
class ProjectsEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsProjects
        fields = ('id', 'name','latitude', 'longitude', 'address', 'updated_by')
class ProjectsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsProjects
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.status=False
        instance.is_deleted=True
        instance.save()
        return instance

#:::  ATTENDENCE ::::#
class AttendanceAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsAttendance
        fields = ('id', 'type', 'employee','date', 'login_time', 'login_latitude','login_longitude','login_address' ,
                  'logout_time','logout_latitude',
                  'logout_longitude','logout_address','justification',
                  'created_by', 'owned_by','approved_status')
class AttendanceEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsAttendance
        fields = ('id', 'type', 'employee', 'date', 'login_time', 'login_latitude', 'login_longitude', 'login_address',
                  'logout_time', 'logout_latitude', 'logout_longitude',
                  'logout_address', 'justification', 'updated_by','approved_status')
class AttandanceLogAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=PmsAttandanceLog
        fields=('id','attandance','time','latitude','longitude','address','created_by','owned_by')

#:::::::::::::::::  MECHINE WORKING CATEGORY :::::::::::#
class MachineriesWorkingCategoryAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = ('id', 'name', 'created_by', 'owned_by')
class MachineriesWorkingCategoryEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = ('id', 'name', 'updated_by')
class MachineriesWorkingCategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsMachineriesWorkingCategory
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.save()
        return instance

#:::::::::::::::::  MECHINARY MASTER :::::::::::::::#
class MachineriesAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PmsMachineries
        fields = ('id', 'equipment_name', 'equipment_category',
                  'equipment_type', 'owner_type','equipment_make',
                  'equipment_model_no', 'equipment_registration_no',
                  'equipment_power', 'measurement_by', 'measurement_quantity',
                  'equipment_price', 'equipment_purchase_date','equipment_last_pm_date',
                 'equipment_next_pm_schedule','remarks' 'created_by', 'owned_by')
class MachineriesEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PmsMachineries
        fields = ('id', 'equipment_name', 'equipment_category',
                  'equipment_type', 'owner_type','equipment_make','equipment_model_no', 'equipment_registration_no',
                  'equipment_power', 'measurement_by', 'measurement_quantity', 'equipment_price', 'equipment_purchase_date','equipment_last_pm_date',
                 'equipment_next_pm_schedule','remarks', 'updated_by')
class MachineriesDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsMachineries
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.is_deleted=True
        instance.save()
        return instance

#:::::::::::::::::  PMS External Users ::::::::::::::::::::#
class ExternalUsersTypeAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    type_name = serializers.CharField(required=True)

    class Meta:
        model = PmsExternalUsersType
        fields = ('id', 'type_name', 'type_desc', 'created_by', 'owned_by')
class ExternalUsersTypeEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = PmsExternalUsersType
        fields = ('id', 'type_name', 'type_desc', 'updated_by')
class ExternalUsersTypeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsExternalUsersType
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.save()
        return instance

#:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
class ExternalUsersAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    name=serializers.CharField(required=True)
    #user_type=serializers.CharField(required=True)
    contact_no=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    address=serializers.CharField(required=True)
    class Meta:
        model = PmsExternalUsers
        fields = ('id', 'name', 'user_type','organisation_name', 'contact_no',
                  'email', 'address', 'docfile_name',  'docfile',
                  'created_by', 'owned_by')
class ExternalUsersEditSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(required=True)
    #user_type = serializers.CharField(required=True)
    contact_no = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    class Meta:
        model = PmsExternalUsers
        fields = ('id', 'name', 'user_type', 'organisation_name', 'contact_no', 'email', 'address', 'docfile_name', 'docfile',
        'updated_by')
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name')
        print('instance.name',instance.name)
        instance.user_type=validated_data.get('user_type')
        instance.organisation_name=validated_data.get('organisation_name')
        instance.contact_no=validated_data.get('contact_no')
        instance.email=validated_data.get('email')
        instance.address=validated_data.get('address')
        instance.docfile_name=validated_data.get('docfile_name')
        existing_image='./media/'+str(instance.docfile)
        print('existing_image',existing_image)
        if validated_data.get('docfile'):
            if os.path.isfile(existing_image):
                os.remove(existing_image)
            instance.docfile=validated_data.get('docfile')
        instance.updated_by=validated_data.get('updated_by')
        instance.save()
        return instance
class ExternalUsersDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=PmsExternalUsers
        fields='__all__'
    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.save()
        return instance



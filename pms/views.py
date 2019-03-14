from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from pms.models import *
from pms.serializers import *
import time
from multiplelookupfields import MultipleFieldLookupMixin
from rest_framework.views import APIView
from django.conf import settings

#::::::::::::::: TENDER AND TENDER DOCUMENTS :::::::::::::::#
class TendersAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TendersAddSerializer
class TenderDocsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderDocumentAddSerializer
class TenderDocsByTenderIdView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderDocumentAddSerializer
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        if tender_id:
            queryset = PmsTenderDocuments.objects.filter(tender_id=tender_id).order_by('-created_at')
            return queryset
class TenderEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenders.objects.all()
    serializer_class = TenderEditSerializer
class TenderDocsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDocsEditSerializer
class TenderDeleteByIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDeleteSerializer
class TenderDocsDeleteByIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderDocuments.objects.all()
    serializer_class = TenderDocumentDeleteSerializer

#::::::::::::::: TENDER  BIDDER TYPE :::::::::::::::#
class VendorsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = VendorsAddSerializer
    queryset = PmsTenderVendors.objects.all()
class TendorBidderTypeAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TendorBidderTypeAddSerializer
class TendorBidderTypeByTenderIdView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #serializer_class = TendorBidderTypeByTenderIdSerializer
    def get(self, request, *args, **kwargs):
        print('self',self)
        tender_id = self.kwargs['tender_id']
        if tender_id:
            tender_bidder_data = PmsTenderBidderType.objects.filter(tender=tender_id)
            if tender_bidder_data:
                for each_tender_bidder_data in tender_bidder_data:
                    vendors = []
                    vendors_m_details = PmsTenderBidderTypeVendorMapping.objects.\
                        filter(tender_bidder_type=each_tender_bidder_data.id)
                    #print('vendors_m_details',vendors_m_details)
                    if vendors_m_details:
                        for e_vendors_m_details in vendors_m_details:
                            vendor_d = {
                                "tendor_vendor_id":e_vendors_m_details.tender_vendor.id
                            }
                            vendors.append(e_vendors_m_details.tender_vendor.id)
                    if each_tender_bidder_data.updated_by:
                        updated_by = each_tender_bidder_data.updated_by.id
                    else:
                        updated_by = ''

                    response = {
                        "id":each_tender_bidder_data.id,
                        "bidder_type":each_tender_bidder_data.bidder_type,
                        "type_of_partner": each_tender_bidder_data.type_of_partner,
                        "responsibility": each_tender_bidder_data.responsibility,
                        "profit_sharing_ratio_actual_amount": each_tender_bidder_data.profit_sharing_ratio_actual_amount,
                        "profit_sharing_ratio_tender_specific_amount": each_tender_bidder_data.profit_sharing_ratio_tender_specific_amount,
                        "updated_by":updated_by,
                        "vendors":vendors
                    }
                    return Response(response)
            else:
                return Response()
    def update(self, request, *args, **kwargs):
        tender_id = self.kwargs['tender_id']
        print('request',request.data['bidder_type'])
        try:
            if tender_id:
                tender_bidder_type_vendor_mapping_list = []
                tender_bidder_data = PmsTenderBidderType.objects.get(tender=tender_id)
                print('tender_bidder_data',type(tender_bidder_data))
                with transaction.atomic():
                    if request.data['bidder_type'] == "joint_venture":
                        tender_bidder_data.bidder_type = request.data['bidder_type']
                        tender_bidder_data.type_of_partner=request.data['type_of_partner']
                        tender_bidder_data.responsibility=request.data['responsibility']
                        tender_bidder_data.profit_sharing_ratio_actual_amount=request.data['profit_sharing_ratio_actual_amount']
                        tender_bidder_data.profit_sharing_ratio_tender_specific_amount=request.data['profit_sharing_ratio_tender_specific_amount']
                        tender_bidder_data.updated_by=self.request.user
                        tender_bidder_data.save()
                        xyz=PmsTenderBidderTypeVendorMapping.objects.filter(tender_bidder_type_id=tender_bidder_data.id).delete()
                        print('xyz',xyz)
                        for vendor in request.data['vendors']:
                            print('vendor',vendor)
                            request_dict = {
                                "tender_bidder_type_id": str(tender_bidder_data.id),
                                "tender_vendor_id": int(vendor),
                                "status": True,
                                "created_by": self.request.user,
                                "owned_by": self.request.user
                            }
                            tender_bidder_type_vendor_m = PmsTenderBidderTypeVendorMapping.objects.create(
                                **request_dict)
                        response = {
                            'id': tender_bidder_data.id,
                            'tender': tender_bidder_data.tender.id,
                            'bidder_type': tender_bidder_data.bidder_type,
                            'type_of_partner':  tender_bidder_data.type_of_partner,
                            'responsibility': tender_bidder_data.responsibility,
                            'profit_sharing_ratio_actual_amount':  tender_bidder_data.profit_sharing_ratio_actual_amount,
                            'profit_sharing_ratio_tender_specific_amount':  tender_bidder_data.profit_sharing_ratio_tender_specific_amount,
                            'vendors': request.data['vendors']
                        }
                        return Response(response)
                    else:
                        tender_bidder_data.bidder_type = request.data['bidder_type']
                        tender_bidder_data.responsibility = request.data['responsibility']
                        tender_bidder_data.updated_by = self.request.user
                        tender_bidder_data.save()
                        response = {
                            'id': tender_bidder_data.id,
                            'tender': tender_bidder_data.tender.id,
                            'bidder_type': tender_bidder_data.bidder_type,
                            'responsibility': tender_bidder_data.responsibility,
                        }
                        return Response(response)

        except Exception as e:
            raise e
class TendorBidderTypeEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderBidderType.objects.all()
    serializer_class = TendorBidderTypeEditSerializer
class TendorBidderTypeDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderBidderType.objects.all()
    serializer_class = TendorBidderTypeDeleteSerializer

#::::::::::::::: TENDER  ELIGIBILITY :::::::::::::::#
class PmsTenderEligibilityFieldsByTypeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityFieldsByTypeEditSerializer
    queryset = PmsTenderEligibilityFieldsByType.objects.all()
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        eligibility_type = self.kwargs['eligibility_type']
        return self.queryset.filter(tender_id=tender_id, tender_eligibility__type=eligibility_type,
                                    status=True, is_deleted=False)
class PmsTenderEligibilityAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityAddSerializer
    queryset = PmsTenderEligibility.objects.all()
class PmsTenderEligibilityFieldsByTypeEdit(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderEligibilityFieldsByTypeEditSerializer
    queryset = PmsTenderEligibilityFieldsByType.objects.all()
class PmsTenderNotEligibilityReasonAdd(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PmsTenderNotEligibilityReasonAddSerializer
    queryset = PmsTenderEligibility.objects.filter(status=True, is_deleted=False)
    lookup_fields = ("tender_id", "type")

#::::::::::::::: TENDER SURVEY SITE PHOTOS:::::::::::::::#
class TenderSurveySitePhotosAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosAddSerializer
class TenderSurveySitePhotosEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosEditSerializer
class TenderSurveySitePhotosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosListSerializer
    def get_queryset(self):
        tender_id = self.kwargs['tender_id']
        queryset = PmsTenderSurveySitePhotos.objects.filter(tender_id=tender_id, status=True)
        return queryset

class TenderSurveySitePhotosDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveySitePhotos.objects.all()
    serializer_class =TenderSurveySitePhotosDeleteSerializer

#::::::::::::::: TENDER SURVEY COORDINATE :::::::::::::::#
class TenderSurveyLocationAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationAddSerializer
class TenderSurveyLocationEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationEditSerializer
class TenderSurveyLocationDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSiteCoordinate.objects.all()
    serializer_class =TenderSurveyLocationDeleteSerializer
class TenderSurveyCOSupplierAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierAddSerializer
class TenderSurveyCOSupplierEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierEditSerializer
class TenderSurveyCOSupplierDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyCoordinatesSuppliers.objects.all()
    serializer_class =TenderSurveyCOSupplierDeleteSerializer

#::::::::::: TENDER SURVEY METERIAL ::::::::::::::::::::#
class TenderSurveyMaterialsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class=TenderSurveyMaterialsAddSerializer
class TenderSurveyMaterialsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class=TenderSurveyMaterialsEditSerializer
class TenderSurveyMaterialsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.all()
    serializer_class = TenderSurveyMaterialsDeleteSerializer
class TenderSurveyMaterialsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyMaterials.objects.filter(status=True)
    serializer_class = TenderSurveyMaterialsListSerializer

#::::::::::: TENDER SURVEY RESOURCE METERIAL ::::::::::::::::::::#
class TenderSurveyResourceMaterialAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialAddSerializer
class TenderSurveyResourceMaterialEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialEditSerializer
class TenderSurveyResourceMaterialDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.all()
    serializer_class= TenderSurveyResourceMaterialDeleteSerializer
class TenderSurveyResourceMaterialListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceMaterial.objects.filter(status=True)
    serializer_class = TenderSurveyResourceMaterialListSerializer

#:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
class TenderSurveyResourceHydrologicalAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalAddSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceHydrologicalEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalEditSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceHydrologicalDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDeleteSerializer
    queryset = PmsTenderSurveyResourceHydrological.objects.all()
class TenderSurveyResourceHydrologicalDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.all()
class TenderSurveyResourceHydrologicalDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceHydrologicalDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceHydrologicalDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.all()

#:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
class TenderSurveyResourceContractorsOVendorsContractorAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorAddSerializer
class TenderSurveyResourceContractorsOVendorsContractorEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class = TenderSurveyResourceContractorsOVendorsContractorEditSerializer
class TenderSurveyResourceContractorsOVendorsContractorDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContractorsOVendorsContractor.objects.all()
    serializer_class = TenderSurveyResourceContractorsOVendorsContractorDeleteSerializer
class TenderSurveyResourceContractorsOVendorsContractorDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsContractorDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorModelMasterAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class =TenderSurveyResourceContractorsOVendorsVendorModelMasterAddSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorAddSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorEditSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDeleteSerializer
    queryset = PmsTenderSurveyResourceContractorsOVendorsVendor.objects.all()
class TenderSurveyResourceContractorsOVendorsVendorDocumentAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentAddSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDocumentEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentEditSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)
class TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteSerializer
    queryset = PmsTenderSurveyDocument.objects.filter(status=True, is_deleted=False)

#:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
class TenderSurveyResourceContactDesignationAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDesignation.objects.filter(status=True)
    serializer_class = TenderSurveyResourceContactDesignationAddSerializer
class TenderSurveyResourceContactDetailsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsAddSerializer
class TenderSurveyResourceContactDetailsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsEditSerializer
class TenderSurveyResourceContactDetailsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderSurveyResourceContactDetails.objects.all()
    serializer_class =TenderSurveyResourceContactDetailsDeleteSerializer

#::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
class TenderInitialCostingUploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, format=None):
        try:
            field_label_value = []
            #tender_initial_costing=PmsTenderInitialCosting.objects.create(**validated_data)
            import numpy as np
            import pandas as pd
            import xlrd
            df1 = pd.read_excel(request.data['document']) #read excel
            df2 = df1.replace(np.nan,'',regex=True) # for replace blank value with nan
            df =df2.loc[:, ~df2.columns.str.contains('^Unnamed')] # for elmeminate the blank index
            #print("Column headings:")
            #print(df.columns)
            for j in df.columns:
                #print(df[j])
                field_value = []
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
                    field_value.append(df[j][i])
                field_label_val_dict = {
                        "field_label":j,
                        "field_value":field_value

                }
                    #print(df[j][i])
                field_label_value.append(field_label_val_dict)
            #print('field_label_value',field_label_value)
            response_data={
                "tender":request.data['tender'],
                "field_label_value":field_label_value
            }
            return Response(response_data)
        except Exception as e:
            raise APIException({'request_status': 0, 'msg': e})

class TenderInitialCostingAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsTenderInitialCosting.objects.all()
    serializer_class =TenderInitialCostingAddSerializer

#:::::::::::: ATTENDENCE ::::::::::::::::::::::::::::#
class AttendanceAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.all()
    serializer_class = AttendanceAddSerializer
    def list(self, request, *args, **kwargs):
        response = super(AttendanceAddView, self).list(request,args,kwargs)
        print('response: ', response.data)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class AttendanceEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttendance.objects.filter(is_deleted=False)
    serializer_class = AttendanceEditSerializer

    def put(self, request, *args, **kwargs):
        response = super(AttendanceEditView, self).put(request, args, kwargs)
        print('request: ', request.data)
        data_dict = {}
        data_dict['result'] = request.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        # elif len(response.data) == 0:
        #     data_dict['request_status'] = 1
        #     data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
class AttandanceLogAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsAttandanceLog.objects.all()
    serializer_class = AttandanceLogAddSerializer

#:::::::::::: PMS PROJECTS ::::::::::::::::::::::::::::#
class ProjectsAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class=ProjectsAddSerializer
class ProjectsEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class = ProjectsEditSerializer
class ProjectsDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsProjects.objects.all()
    serializer_class = ProjectsDeleteSerializer

#:::::::::::::::::  MECHINARY WORKING CATEGORY :::::::::::::::#
class MachineriesAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.all()
    serializer_class = MachineriesAddSerializer
class MachineriesEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.all()
    serializer_class = MachineriesEditSerializer
class MachineriesDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineries.objects.all()
    serializer_class = MachineriesDeleteSerializer

#:::::::::::::::::  MECHINARY MASTER :::::::::::::::#
class MachineriesWorkingCategoryAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.filter(is_deleted=False).order_by('-id')
    serializer_class= MachineriesWorkingCategoryAddSerializer
class MachineriesWorkingCategoryEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.all()
    serializer_class = MachineriesWorkingCategoryEditSerializer
class MachineriesWorkingCategoryDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsMachineriesWorkingCategory.objects.all()
    serializer_class = MachineriesWorkingCategoryDeleteSerializer

#:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
class ExternalUsersTypeAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalUsersTypeAddSerializer
class ExternalUsersTypeEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.all()
    serializer_class = ExternalUsersTypeEditSerializer
class ExternalUsersTypeDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsersType.objects.all()
    serializer_class = ExternalUsersTypeDeleteSerializer

#:::::::::::::::::  PmsExternalUsers ::::::::::::::::::::#
class ExternalUsersAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalUsersAddSerializer
class ExternalUsersEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.all()
    serializer_class = ExternalUsersEditSerializer
class ExternalUsersDeleteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PmsExternalUsers.objects.all()
    serializer_class =  ExternalUsersDeleteSerializer
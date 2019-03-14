from pms import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    #:::::::::: TENDER AND TENDER DOCUMENTS  ::::::::#
    path('tenders_add/', views.TendersAddView.as_view()),
    path('tenders_edit/<pk>/', views.TenderEditView.as_view()),
    path('tenders_delete/<pk>/', views.TenderDeleteByIdView.as_view()),
    path('tender_doc_by_tender_id/<tender_id>/', views.TenderDocsByTenderIdView.as_view()),
    path('tenders_doc_add/', views.TenderDocsAddView.as_view()),
    path('tenders_doc_edit/<pk>/', views.TenderDocsEditView.as_view()),
    path('tenders_doc_delete/<pk>/', views.TenderDocsDeleteByIdView.as_view()),

    #::::::::::::::: TENDER  BIDDER TYPE :::::::::::::::#
    path('vendors_add/', views.VendorsAddView.as_view()),
    path('tender_bidder_details_by_tender_id/<tender_id>/', views.TendorBidderTypeByTenderIdView.as_view()),
    path('tender_bidder_type_add/', views.TendorBidderTypeAddView.as_view()),
    path('tender_bidder_type_edit/<pk>/', views.TendorBidderTypeEditView.as_view()),
    path('tender_bidder_type_delete/<pk>/', views.TendorBidderTypeDeleteView.as_view()),

    #::::::::::::::: TENDER  ELIGIBILITY :::::::::::::::#
    path('tender_eligibility_fields_list/<tender_id>/<eligibility_type>/',
         views.PmsTenderEligibilityFieldsByTypeListView.as_view()),
    path('tender_eligibility_fields_add/', views.PmsTenderEligibilityAdd.as_view()),
    path('tender_eligibility_fields_edit_by_id/<pk>/', views.PmsTenderEligibilityFieldsByTypeEdit.as_view()),
    path('tender_not_eligibility_reason_add/<tender_id>/<type>/', views.PmsTenderNotEligibilityReasonAdd.as_view()),

    #::::::::::::::: TENDER SURVEY SITE PHOTOS :::::::::::::::#
    path('tender_survey_site_photos_add/', views.TenderSurveySitePhotosAddView.as_view()),
    path('tender_survey_site_photos_edit/<pk>/', views.TenderSurveySitePhotosEditView.as_view()),
    path('tender_survey_site_photos_list/<tender_id>/', views.TenderSurveySitePhotosListView.as_view()),
    path('tender_survey_site_photos_delete/<pk>/', views.TenderSurveySitePhotosDeleteView.as_view()),

    #::::::::::: TENDER SURVEY COORDINATES ::::::::::::::::::::#
    path('tender_survey_location_add/', views.TenderSurveyLocationAddView.as_view()),
    path('tender_survey_location_edit/<pk>/', views.TenderSurveyLocationEditView.as_view()),
    path('tender_survey_location_delete/<pk>/', views.TenderSurveyLocationDeleteView.as_view()),
    path('tender_survey_co_supplier_add/', views.TenderSurveyCOSupplierAddView.as_view()),
    path('tender_survey_co_supplier_edit/<pk>/', views.TenderSurveyCOSupplierEditView.as_view()),
    path('tender_survey_co_supplier_delete/<pk>/', views.TenderSurveyCOSupplierDeleteView.as_view()),

    #::::::::::: TENDER SURVEY METERIAL ::::::::::::::::::::#
    path('tender_survey_materials_add/', views.TenderSurveyMaterialsAddView.as_view()),
    path('tender_survey_materials_edit/<pk>/', views.TenderSurveyMaterialsEditView.as_view()),
    path('tender_survey_materials_delete/<pk>/', views.TenderSurveyMaterialsDeleteView.as_view()),
    path('tender_survey_materials_list/', views.TenderSurveyMaterialsListView.as_view()),

    #::::::::::: TENDER SURVEY RESOURCE METERIAL ::::::::::::#
    path('tender_survey_resource_material_add/', views.TenderSurveyResourceMaterialAddView.as_view()),
    path('tender_survey_resource_material_edit/<pk>/',views.TenderSurveyResourceMaterialEditView.as_view()),
    path('tender_survey_resource_material_delete/<pk>/',views.TenderSurveyResourceMaterialDeleteView.as_view()),
    path('tender_survey_resource_material_list/',views.TenderSurveyResourceMaterialListView.as_view()),

    #:::: TENDER SURVEY RESOURCE HYDROLOGICAL :::::::#
    path('tender_survey_resource_hydrological_add/',views.TenderSurveyResourceHydrologicalAddView.as_view()),
    path('tender_survey_resource_hydrological_edit/<pk>/',views.TenderSurveyResourceHydrologicalEditView.as_view()),
    path('tender_survey_resource_hydrological_delete/<pk>/',views.TenderSurveyResourceHydrologicalDeleteView.as_view()),
    path('tender_survey_resource_hydrological_document_add/',views.TenderSurveyResourceHydrologicalDocumentAddView.as_view()),
    path('tender_survey_resource_hydrological_document_edit/<pk>/',views.TenderSurveyResourceHydrologicalDocumentEditView.as_view()),
    path('tender_survey_resource_hydrological_document_delete/<pk>/',views.TenderSurveyResourceHydrologicalDocumentDeleteView.as_view()),

    #:::: TENDER SURVEY RESOURCE CONTRACTORS / VENDORS :::::::#
    path('tender_survey_resource_contractors_o_vendors_contarctor_add/',views.TenderSurveyResourceContractorsOVendorsContractorAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_add/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_contarctor_document_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsContractorDocumentDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_model_master_add/',views.TenderSurveyResourceContractorsOVendorsVendorModelMasterAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_add/',views.TenderSurveyResourceContractorsOVendorsVendorAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_edit/<pk>/',views.TenderSurveyResourceContractorsOVendorsVendorEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_delete/<pk>/',views.TenderSurveyResourceContractorsOVendorsVendorDeleteView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_add/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentAddView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_edit/<pk>/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentEditView.as_view()),
    path('tender_survey_resource_contractors_o_vendors_vendor_document_delete/<pk>/', views.TenderSurveyResourceContractorsOVendorsVendorDocumentDeleteView.as_view()),

    #:::: TENDER SURVEY RESOURCE CONTACT DETAILS AND DESIGNATION :::::::#
    path('tender_survey_resource_contact_designation_add/',views.TenderSurveyResourceContactDesignationAddView.as_view()),
    path('tender_survey_resource_contact_details_add/',views.TenderSurveyResourceContactDetailsAddView.as_view()),
    path('tender_survey_resource_contact_details_edit/<pk>/',views.TenderSurveyResourceContactDetailsEditView.as_view()),
    path('tender_survey_resource_contact_details_delete/<pk>/',views.TenderSurveyResourceContactDetailsDeleteView.as_view()),

    #::::::::::: TENDER INITIAL COSTING ::::::::::::::::::::#
    path('tender_initial_costing_upload_file/', views.TenderInitialCostingUploadFileView.as_view()),
    path('tender_initial_costing_add/', views.TenderInitialCostingAddView.as_view()),

    #::::::::::::::: PMS PROJECTS ::::::::::::::::::::::::::::#
    path('projects_add/', views.ProjectsAddView.as_view()),
    path('projects_edit/<pk>/', views.ProjectsEditView.as_view()),
    path('projects_delete/<pk>/', views.ProjectsDeleteView.as_view()),

    #:::::::::::::::::  ATTENDENCE ::::::::::::::::::::#
    path('attandance_add/', views.AttendanceAddView.as_view()),
    path('attandance_edit/<pk>/', views.AttendanceEditView.as_view()),
    path('attandance_log_add/', views.AttandanceLogAddView.as_view()),

    #:::::::::::::::::  MECHINARY WORKING CATEGORY ::::::::::::::::::::#
    path('machineries_working_category_add/', views.MachineriesWorkingCategoryAddView.as_view()),
    path('machineries_working_category_edit/<pk>/', views.MachineriesWorkingCategoryEditView.as_view()),
    path('machineries_working_category_delete/<pk>/', views.MachineriesWorkingCategoryDeleteView.as_view()),

    #:::::::::::::::::  MECHINARY ::::::::::::::::::::#
    path('machineries_add/', views.MachineriesAddView.as_view()),
    path('machineries_edit/<pk>/', views.MachineriesEditView.as_view()),
    path('machineries_delete/<pk>/', views.MachineriesDeleteView.as_view()),

    #:::::::::::::::::  PMS External Users Type ::::::::::::::::::::#
    path('external_users_type_add/', views.ExternalUsersTypeAddView.as_view()),
    path('external_users_type_edit/<pk>/', views.ExternalUsersTypeEditView.as_view()),
    path('external_users_type_delete/<pk>/', views.ExternalUsersTypeDeleteView.as_view()),

    #:::::::::::::::::  PmsExternalUsers ::::::::::::::::::::#
    path('external_users_add/', views.ExternalUsersAddView.as_view()),
    path('external_users_edit/<pk>/', views.ExternalUsersEditView.as_view()),
    path('external_users_delete/<pk>/', views.ExternalUsersDeleteView.as_view()),
]
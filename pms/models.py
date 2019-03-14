from django.db import models
from django.contrib.auth.models import User
from dynamic_media import get_directory_path
from django_mysql.models import EnumField
from validators import validate_file_extension
from core.models import TCoreUnit
import datetime

#:::::::::: LOG TABLE ::::::::#

class PmsLog(models.Model):
    module_id = models.BigIntegerField()
    module_table_name = models.TextField(blank=True, null=True)
    action_type = EnumField(choices=['add', 'edit', 'delete'])
    current_module_data = models.TextField(blank=True, null=True)
    updated_module_data = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_log'

#:::::::::: ADD NEW TENDER TABLE ::::::::#

class PmsTenders(models.Model):
    tender_g_id = models.CharField(max_length=50,unique=True)
    tender_final_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_opened_on = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_added_by = models.CharField(max_length=100, blank=True, null=True)
    tender_received_on = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    tender_aasigned_to = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tenders'

#:::::::::: TENDER DOCUMENT TABLE ::::::::#

class PmsTenderDocuments(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_d_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,null=True)
    document_name = models.CharField(max_length=200,blank=True,null=True)
    tender_document = models.FileField(upload_to=get_directory_path,
                                        default=None,
                                        blank=True, null=True,
                                        validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_documents'

#:::::::::: TENDER  ELIGIBILITY  TABLE ::::::::#

class PmsTenderEligibility(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_e_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    type = EnumField(choices=['technical', 'financial', 'special'])
    ineligibility_reason = models.TextField(blank=True, null=True)
    eligibility_status = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_e_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_e_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_e_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_eligibility'
        unique_together = ('type', 'tender')

#:::::::::: TENDER  ELIGIBILITY FIELDS BY TYPE TABLE ::::::::#

class PmsTenderEligibilityFieldsByType(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_e_f_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    tender_eligibility = models.ForeignKey(PmsTenderEligibility,
                                  related_name='eligibility_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    field_label = models.TextField(blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    eligible = models.BooleanField(default=True)
    # document = models.FileField(upload_to=get_directory_path,
    #                             default=None,
    #                             blank=True, null=True,
    #                             validators=[validate_file_extension]
    #                             )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_e_f_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_e_f_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_e_f_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_eligibility_fields_by_type'

#:::::::::: TENDER VENDORS TABLE ::::::::#

class PmsTenderVendors(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_v_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    name = models.CharField(max_length=80,blank=True,null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_v_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='t_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_tender_vendors'

#:::::::::: TENDER  BIDDER TYPE TABLE ::::::::#

class PmsTenderBidderType(models.Model):
    type_of_partner = (
        (1, 'lead_partner'),
        (2, 'other_partner')
    )
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_b_t_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    bidder_type = EnumField(choices=['joint_venture', 'individual'])
    type_of_partner = models.IntegerField(choices=type_of_partner,null=True,blank=True)
    responsibility = EnumField(choices=['technical', 'financial','technical_and_financial'],null=True,
                                                                    blank=True,)
    profit_sharing_ratio_actual_amount = models.FloatField(null=True, blank=True, default=None)
    profit_sharing_ratio_tender_specific_amount = models.FloatField(null=True,
                                                                    blank=True,
                                                                    default=None)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_b_t_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_b_t_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_b_t_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_bidder_type'

#:::::::::: TENDER  BIDDER TYPE TABLE ::::::::#

class PmsTenderBidderTypeVendorMapping(models.Model):
    tender_bidder_type = models.ForeignKey(PmsTenderBidderType,on_delete=models.CASCADE,
                                  blank=True,null=True)
    tender_vendor = models.ForeignKey(PmsTenderVendors,on_delete=models.CASCADE,
                                  blank=True,null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_b_t_v_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_b_t_v_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_bidder_type_vendor_mapping'

##################################################################################
########################### SURVEY TAB SECTION ###################################
##################################################################################

#:::::::::: TENDER SURVEY SITE PHOTOS ::::::::#

class PmsTenderSurveySitePhotos(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_s_p_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )

    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_s_p_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_s_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_s_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_site_photos'

#::: TENDER SURVEY COORDINATES SITE COORDINATE ::::#

class PmsTenderSurveyCoordinatesSiteCoordinate(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_c_s_c_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_c_s_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_c_s_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_c_s_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_coordinates_site_coordinate'

#::: TENDER SURVEY MATERIALS ::::#
#[this table Common for resource->material,coordinates]

class PmsTenderSurveyMaterials(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    unit = models.ForeignKey(TCoreUnit,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                            )

    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_materials'

#::: TENDER SURVEY COORDINATES SUPPLIERS ::::#

class PmsTenderSurveyCoordinatesSuppliers(models.Model):
    Type_of_materials = (
        (1, 'raw_materials'),
        (2, 'crusher')
    )
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_c_s_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    type = models.IntegerField(choices=Type_of_materials, null=True, blank=True)
    tender_survey_material = models.ForeignKey(PmsTenderSurveyMaterials,
                                  related_name='t_s_c_s_material_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_c_s_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_c_s_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_c_s_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_coordinates_suppliers'

#::: TENDER SURVEY RESOURCE MATERIAL ::::#

class PmsTenderSurveyResourceMaterial(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_m_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    tender_survey_material = models.ForeignKey(PmsTenderSurveyMaterials,
                                               related_name='t_s_r_m_material_id',
                                               on_delete=models.CASCADE,
                                               blank=True,
                                               null=True
                                               )
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    document_name = models.CharField(max_length=100,blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                             default=None,
                             blank=True, null=True,
                             validators=[validate_file_extension]
                             )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_m_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_m_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_m_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_resource_material'

#::: TENDER SURVEY RESOURCE ESTABLISHMENT ::::#

class PmsTenderSurveyResourceEstablishment(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_e_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_e_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_e_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_e_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_resource_establishment'

#::: TENDER SURVEY DOCUMENT COMMON FOR THEREE TAB
# establishment,hydrological data,contractors/vendors ::::#

class PmsTenderSurveyDocument(models.Model):
    model_class = models.CharField(max_length=100, blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    document_name = models.CharField(max_length=100,blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_survey_document'

#::: TENDER SURVEY RESOURCE HYDROLOGICAL ::::#

class PmsTenderSurveyResourceHydrological(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_h_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_h_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_h_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_h_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_hydrological'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS CONTRACTOR ::::#

class PmsTenderSurveyResourceContractorsOVendorsContractor(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_o_v_c_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contractors_o_vendors_contractor'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS VENDOR MODEL MASTER ::::#

class PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster(models.Model):
        name = models.CharField(max_length=100, blank=True, null=True)
        status = models.BooleanField(default=True)
        is_deleted = models.BooleanField(default=False)
        created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_created_by',
                                       on_delete=models.CASCADE, blank=True, null=True)
        owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_owned_by',
                                     on_delete=models.CASCADE, blank=True, null=True)
        updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_v_m_updated_by',
                                       on_delete=models.CASCADE, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return str(self.id)

        class Meta:
            db_table = 'pms_tender_resource_contractors_o_vendors_vendor_model_master'

#::: TENDER SURVEY RESOURCE CONTRACTORS OR VENDORS VENDORS ::::#

class PmsTenderSurveyResourceContractorsOVendorsVendor(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_o_v_v_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    model = models.ForeignKey(PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    hire = models.TextField(blank=True, null=True)
    khoraki = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_o_v_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contractors_o_vendors_vendor'

#::: TENDER SURVEY RESOURCE CONTACT DESIGNATION ::::#

class PmsTenderSurveyResourceContactDesignation(models.Model):
    tender = models.ForeignKey(PmsTenders,
                                  related_name='t_s_r_c_d_tender_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    name = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contact_designation'

#::: TENDER SURVEY RESOURCE CONTACT DETAILS ::::#

class PmsTenderSurveyResourceContactDetails(models.Model):
    designation = models.ForeignKey(PmsTenderSurveyResourceContactDesignation,
                                  related_name='t_s_r_c_d_designation_id',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True
                                  )
    field_label = models.TextField(blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_s_r_c_de_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_s_r_c_de_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_s_r_c_de_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_resource_contact_details'

#::: TENDER INITIAL COSTING ::::#

class PmsTenderInitialCosting(models.Model):
    tender = models.ForeignKey(PmsTenders,
                               related_name='t_i_c_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    client = models.CharField(max_length=100,blank=True, null=True)
    tender_notice_no_bid_id_no = models.CharField(max_length=100,
                                                  blank=True, null=True)
    name_of_work = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    received_estimate = models.FloatField(blank=True, null=True)
    quoted_rate = models.FloatField(blank=True, null=True)
    difference_in_budget = models.FloatField(blank=True, null=True)
    document = models.FileField(upload_to=get_directory_path,default=None,
                                blank=True, null=True,
                                validators=[validate_file_extension]
                               )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing'

#::: TENDER INITIAL COSTING EXCEL FIELD LABEL ::::#

class PmsTenderInitialCostingExcelFieldLabel(models.Model):
    tender_initial_costing = models.ForeignKey(PmsTenderInitialCosting,
                               related_name='t_i_c_e_f_l_costing_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    field_label = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_e_f_l_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing_excel_field_label'

#::: TENDER INITIAL COSTING EXCEL FIELD VALUE ::::#

class PmsTenderInitialCostingExcelFieldValue(models.Model):
    tender_initial_costing = models.ForeignKey(PmsTenderInitialCosting,
                               related_name='t_i_c_e_f_v_costing_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    initial_costing_field_label = models.ForeignKey(PmsTenderInitialCostingExcelFieldLabel,
                               related_name='t_i_c_e_f_l_label_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    field_value = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_i_c_e_f_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_initial_costing_excel_field_value'

#::: TENDER TAB DOCUMENTS ::::#

class PmsTenderTabDocuments(models.Model):
    tender= models.ForeignKey(PmsTenders,
                               related_name='t_t_d_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    tender_eligibility = models.ForeignKey(PmsTenderEligibility,
                               related_name='t_t_d_eligibility_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    document_date_o_s = models.DateField(blank=True,null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    tab_document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    is_upload_document = models.BooleanField(default=False)
    reason_for_no_documentation=models.TextField(null=True,blank=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_t_d_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_t_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_t_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_tab_documents'

#::: TENDER TAB DOCUMENTS PRICE ::::#

class PmsTenderTabDocumentsPrice(models.Model):
    tender= models.ForeignKey(PmsTenders,
                               related_name='t_t_d_p_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    document_date_o_s = models.DateField(blank=True,null=True)
    document_name = models.CharField(max_length=200, blank=True, null=True)
    tab_document = models.FileField(upload_to=get_directory_path,
                                       default=None,
                                       blank=True, null=True,
                                       validators=[validate_file_extension]
                                       )
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='t_t_d_p_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='t_t_d_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='t_t_d_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_tender_tab_documents_price'

#:::  PROJECTS ::::#
class PmsProjects(models.Model):
    name= models.CharField(max_length=200,blank=True,null=True)
    tender=models.ForeignKey(PmsTenders,
                               related_name='p_tender_id',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True
                               )
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='p_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_projects'

#:::  ATTENDENCE ::::#
class PmsAttendance(models.Model):
    Type_of_attandance= (
        (1, 'individual'),
        (2, ' labours under individual')
    )
    Type_of_approved = (
        (1, 'pending'),
        (2, 'approved'),
        (3, 'reject'),
    )
    type = models.IntegerField(choices=Type_of_attandance, null=True, blank=True)
    employee=models.ForeignKey(User, related_name='attandance_employee_id',
                                   on_delete=models.CASCADE,blank=True,null=True)
    date= models.DateField(auto_now_add=False,blank=True, null=True)
    login_time=models.TimeField(auto_now_add=False,blank=True, null=True)
    login_latitude = models.CharField(max_length=200, blank=True, null=True)
    login_longitude= models.CharField(max_length=200, blank=True, null=True)
    login_address=models.TextField(blank=True, null=True)
    logout_time=models.TimeField(auto_now_add=False,blank=True, null=True)
    logout_latitude = models.CharField(max_length=200, blank=True, null=True)
    logout_longitude = models.CharField(max_length=200, blank=True, null=True)
    logout_address = models.TextField(blank=True, null=True)
    approved_status = models.IntegerField(choices=Type_of_approved,
                                          null=True, blank=True)
    justification=models.TextField(blank=True, null=True)
    is_deleted= models.BooleanField(default=False)
    created_by =models.ForeignKey(User, related_name='attandance_created_by',
                                   on_delete=models.CASCADE,blank=True,null=True)
    owned_by = models.ForeignKey(User, related_name='attandance_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='attandance_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_attandance'

#::: ATTENDENCE LOG ::::#
class PmsAttandanceLog(models.Model):
    attandance=models.ForeignKey(PmsAttendance,related_name='a_l_attandance_id',
                                   on_delete=models.CASCADE,blank=True,null=True)
    time=models.TimeField(auto_now_add=False,blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='a_l_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='a_l_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_attandance_log'

# ::: PMS Machineries Working Category ::::::::::::::::::#
class PmsMachineriesWorkingCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machineries_working_category_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machineries_working_category_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machineries_working_category_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries_working_category'

# ::: PMS Machineries ::::::::::::::::::#
class PmsMachineries(models.Model):
    Type_of_machineries = (
    (1, 'heavy_machinery'),
    (2, 'light_machinery')
    )

    Type_of_owner = (
    (1, 'rental'),
    (2, 'own')
    )
    Type_of_measurement = (
    (1, 'distance'),
    (2, 'time')
    )
    equipment_name = models.CharField(max_length=200, blank=True, null=True)
    equipment_category = models.ForeignKey(PmsMachineriesWorkingCategory,related_name='equipment_working_category',
    on_delete=models.CASCADE,blank=True,null=True)
    equipment_type = models.IntegerField(choices=Type_of_machineries, null=True, blank=True)
    owner_type = models.IntegerField(choices=Type_of_owner, null=True, blank=True)
    equipment_make = models.CharField(max_length=200, blank=True, null=True)
    equipment_model_no = models.CharField(max_length=200, blank=True, null=True)
    equipment_registration_no = models.CharField(max_length=200, blank=True, null=True)
    equipment_power = models.CharField(max_length=200, blank=True, null=True)
    measurement_by = models.IntegerField(choices=Type_of_measurement, null=True, blank=True)
    measurement_quantity = models.CharField(max_length=200, blank=True, null=True)
    equipment_price = models.FloatField(blank=True, null=True)
    equipment_purchase_date = models.DateField(default=datetime.date.today, blank=True, null=True)
    equipment_last_pm_date = models.DateField(blank=True, null=True)
    equipment_next_pm_schedule = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='machinery_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='machinery_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='machinery_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_machineries'

# ::: PMS External Users Type ::::::::::::::::::#
class PmsExternalUsersType(models.Model):
    type_name = models.CharField(max_length=200, blank=True, null=True)
    type_desc = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='external_users_type_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='external_users_type_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='external_users_type_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pms_external_users_type'

# ::: PMS External Users ::::::::::::::::::#
class PmsExternalUsers(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.ForeignKey(PmsExternalUsersType,related_name='external_users_type',
    on_delete=models.CASCADE,blank=True,null=True)
    organisation_name = models.CharField(max_length=200, blank=True, null=True)
    contact_no = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    address = models.TextField(blank=True, null=True)
    docfile_name = models.CharField(max_length=200, blank=True, null=True)
    docfile = models.FileField(upload_to=get_directory_path,default=None,blank=True,
                               null=True,
    validators=[validate_file_extension])
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='external_users_created_by',
    on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='external_users_owned_by',
    on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='external_users_updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'pms_external_userso'

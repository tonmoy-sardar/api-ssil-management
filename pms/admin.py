from django.contrib import admin
from pms.models import *

# Register your models here.
@admin.register(PmsLog)
class PmsLog(admin.ModelAdmin):
    list_display = [field.name for field in PmsLog._meta.fields]

@admin.register(PmsTenders)
class PmsTenders(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenders._meta.fields]

@admin.register(PmsTenderDocuments)
class PmsTenderDocuments(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderDocuments._meta.fields]

@admin.register(PmsTenderEligibility)
class PmsTenderEligibility(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderEligibility._meta.fields]

@admin.register(PmsTenderEligibilityFieldsByType)
class PmsTenderEligibilityFieldsByType(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderEligibilityFieldsByType._meta.fields]

@admin.register(PmsTenderVendors)
class PmsTenderVendors(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderVendors._meta.fields]

@admin.register(PmsTenderBidderType)
class PmsTenderBidderType(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderBidderType._meta.fields]

@admin.register(PmsTenderBidderTypeVendorMapping)
class PmsTenderBidderTypeVendorMapping(admin.ModelAdmin):
    list_display = [field.name for field in PmsTenderBidderTypeVendorMapping._meta.fields]

@admin.register(PmsMachineriesWorkingCategory)
class PmsMachineriesWorkingCategory(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachineriesWorkingCategory._meta.fields]

@admin.register(PmsMachineries)
class PmsMachineries(admin.ModelAdmin):
    list_display = [field.name for field in PmsMachineries._meta.fields]

@admin.register(PmsExternalUsersType)
class PmsExternalUsersType(admin.ModelAdmin):
    list_display = [field.name for field in PmsExternalUsersType._meta.fields]

@admin.register(PmsExternalUsers)
class PmsExternalUsers(admin.ModelAdmin):
    list_display = [field.name for field in PmsExternalUsers._meta.fields]
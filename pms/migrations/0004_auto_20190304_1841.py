# Generated by Django 2.0.13 on 2019-03-04 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models
import dynamic_media
import validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pms', '0003_pmstendersurveysitephotos'),
    ]

    operations = [
        migrations.CreateModel(
            name='PmsTenderSurveyCoordinatesSiteCoordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_c_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_c_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_c_tender_id', to='pms.PmsTenders')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_c_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_survey_coordinates_site_coordinate',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyCoordinatesSuppliers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', django_mysql.models.EnumField(choices=[('raw_materials', 'raw_materials'), ('crusher', 'crusher')])),
                ('supplier_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=30, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document', models.FileField(blank=True, default=None, null=True, upload_to=dynamic_media.get_directory_path, validators=[validators.validate_file_extension])),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_tender_id', to='pms.PmsTenders')),
            ],
            options={
                'db_table': 'pms_tender_survey_coordinates_suppliers',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_class', models.CharField(blank=True, max_length=100, null=True)),
                ('module_id', models.IntegerField(blank=True, null=True)),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document', models.FileField(blank=True, default=None, null=True, upload_to=dynamic_media.get_directory_path, validators=[validators.validate_file_extension])),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_d_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_d_owned_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_d_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_survey_document',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_m_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_m_owned_by', to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_m_tender_id', to='pms.PmsTenders')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_m_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_survey_materials',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceContactDesignation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_d_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_d_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_d_tender_id', to='pms.PmsTenders')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_d_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_contact_designation',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceContactDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_label', models.TextField(blank=True, null=True)),
                ('field_value', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_de_created_by', to=settings.AUTH_USER_MODEL)),
                ('designation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_d_designation_id', to='pms.PmsTenderSurveyResourceContactDesignation')),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_de_owned_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_de_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_contact_details',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceContractorsOVendorsContractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_c_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_c_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_c_tender_id', to='pms.PmsTenders')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_c_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_contractors_o_vendors_contractor',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceContractorsOVendorsVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('hire', models.TextField(blank=True, null=True)),
                ('khoraki', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_contractors_o_vendors_vendor',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_v_m_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_v_m_owned_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_v_m_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_contractors_o_vendors_vendor_model_master',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceEstablishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_survey_resource_establishment',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceEstablishmentMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_m_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_m_owned_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_m_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_establishment_master',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceHydrological',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_h_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_h_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_h_tender_id', to='pms.PmsTenders')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_h_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_resource_hydrological',
            },
        ),
        migrations.CreateModel(
            name='PmsTenderSurveyResourceMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=30, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document', models.FileField(blank=True, default=None, null=True, upload_to=dynamic_media.get_directory_path, validators=[validators.validate_file_extension])),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_m_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_m_owned_by', to=settings.AUTH_USER_MODEL)),
                ('tender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_m_tender_id', to='pms.PmsTenders')),
                ('tender_survey_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_m_material_id', to='pms.PmsTenderSurveyMaterials')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_m_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pms_tender_survey_resource_material',
            },
        ),
        migrations.RenameField(
            model_name='pmstendersurveysitephotos',
            old_name='photo',
            new_name='document',
        ),
        migrations.AddField(
            model_name='pmstendersurveysitephotos',
            name='document_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourceestablishment',
            name='establishment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_establishment_id', to='pms.PmsTenderSurveyResourceEstablishmentMaster'),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourceestablishment',
            name='owned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_owned_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourceestablishment',
            name='tender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_tender_id', to='pms.PmsTenders'),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourceestablishment',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_e_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourcecontractorsovendorsvendor',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pms.PmsTenderSurveyResourceContractorsOVendorsVendorModelMaster'),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourcecontractorsovendorsvendor',
            name='owned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_owned_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourcecontractorsovendorsvendor',
            name='tender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_tender_id', to='pms.PmsTenders'),
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourcecontractorsovendorsvendor',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_r_c_o_v_v_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pmstendersurveycoordinatessuppliers',
            name='tender_survey_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_material_id', to='pms.PmsTenderSurveyMaterials'),
        ),
        migrations.AddField(
            model_name='pmstendersurveycoordinatessuppliers',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_s_c_s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]

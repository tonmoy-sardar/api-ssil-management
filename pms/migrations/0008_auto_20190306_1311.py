# Generated by Django 2.0.13 on 2019-03-06 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0007_auto_20190305_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pmstendersurveyresourceestablishmentmaster',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pmstendersurveyresourceestablishmentmaster',
            name='owned_by',
        ),
        migrations.RemoveField(
            model_name='pmstendersurveyresourceestablishmentmaster',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='pmstendersurveyresourceestablishment',
            name='establishment',
        ),
        migrations.AddField(
            model_name='pmstendersurveyresourceestablishment',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='PmsTenderSurveyResourceEstablishmentMaster',
        ),
    ]

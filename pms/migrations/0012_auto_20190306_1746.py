# Generated by Django 2.0.13 on 2019-03-06 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0011_pmstenderinitialcosting_pmstenderinitialcostingexcelfieldlabel_pmstenderinitialcostingexcelfieldvalu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pmstenderinitialcostingexcelfieldvalue',
            old_name='field_label',
            new_name='initial_costing_field_label',
        ),
    ]

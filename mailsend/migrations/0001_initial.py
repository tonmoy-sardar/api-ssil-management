# Generated by Django 2.1.4 on 2019-02-18 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('html_content', models.TextField()),
                ('template_variable', models.TextField()),
            ],
            options={
                'db_table': 'mail_template',
            },
        ),
    ]

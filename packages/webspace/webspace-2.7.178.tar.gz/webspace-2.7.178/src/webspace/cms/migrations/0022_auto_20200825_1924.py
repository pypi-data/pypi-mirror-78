# Generated by Django 3.0.9 on 2020-08-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0021_auto_20200825_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='webspacesettings',
            name='secondary_inverse_bg_color',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='webspacesettings',
            name='secondary_inverse_color_uks',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]

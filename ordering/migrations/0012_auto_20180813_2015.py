# Generated by Django 2.0.6 on 2018-08-14 00:15

from django.db import migrations


class Migration(migrations.Migration):

    atomic=False

    dependencies = [
        ('ordering', '0011_auto_20180801_2022'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StoreCategory',
            new_name='Category',
        ),
    ]

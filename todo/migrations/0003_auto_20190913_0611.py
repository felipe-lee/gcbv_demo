# Generated by Django 2.2.5 on 2019-09-13 06:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('todo', '0002_auto_20190913_0545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolistmodel',
            old_name='last_edited',
            new_name='last_updated',
        ),
    ]
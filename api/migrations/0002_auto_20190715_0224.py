# Generated by Django 2.2.1 on 2019-07-15 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='height',
            new_name='resolution_height',
        ),
        migrations.RenameField(
            model_name='film',
            old_name='width',
            new_name='resolution_width',
        ),
    ]
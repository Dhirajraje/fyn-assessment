# Generated by Django 5.0.2 on 2024-02-21 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0002_remove_audittrails_updated_on_audittrails_audit_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audittrails',
            old_name='new_data',
            new_name='data',
        ),
        migrations.RemoveField(
            model_name='audittrails',
            name='old_data',
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-21 11:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audittrails',
            name='updated_on',
        ),
        migrations.AddField(
            model_name='audittrails',
            name='audit_type',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audittrails',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audittrails',
            name='tx_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

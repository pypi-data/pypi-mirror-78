# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-24 11:00


import django.utils.timezone
from django.db import migrations, models

import model_utils.fields

ORIGINAL_SOURCE_NAME = 'Enterprise User B2C Site Enrollment'
ORIGINAL_SOURCE_SLUG = 'b2c_site'
UPDATED_SOURCE_NAME = 'Enterprise User Enrollment Background Task'
UPDATED_SOURCE_SLUG = 'enrollment_task'


def update_source(apps, schema_editor):
    """
    The name of this Source is being updated to better reflect it usage.
    """
    enrollment_sources = apps.get_model('enterprise', 'EnterpriseEnrollmentSource')

    source = enrollment_sources.objects.get(slug=ORIGINAL_SOURCE_SLUG)
    source.name = UPDATED_SOURCE_NAME
    source.slug = UPDATED_SOURCE_SLUG
    source.save()


def revert_source(apps, schema_editor):
    """
    The name of this Source is being updated to better reflect it usage.
    """
    enrollment_sources = apps.get_model('enterprise', 'EnterpriseEnrollmentSource')

    source = enrollment_sources.objects.get(slug=UPDATED_SOURCE_SLUG)
    source.name = ORIGINAL_SOURCE_NAME
    source.slug = ORIGINAL_SOURCE_SLUG
    source.save()


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0079_AddEnterpriseEnrollmentSource'),
        ('enterprise', '0080_auto_20191113_1708'),
    ]

    operations = [
        migrations.RunPython(update_source, revert_source)
    ]

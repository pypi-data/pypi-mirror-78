# Generated by Django 3.0.3 on 2020-02-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tom_observations', '0007_observationstrategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='observationgroup',
            name='cadence_parameters',
            field=models.TextField(default=''),
        ),
    ]

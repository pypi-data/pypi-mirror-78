# Generated by Django 2.1.4 on 2019-01-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tom_targets', '0003_merge_20190123_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='source',
        ),
        migrations.RemoveField(
            model_name='target',
            name='source_location',
        ),
        migrations.AlterField(
            model_name='target',
            name='name2',
            field=models.CharField(blank=True, default='', help_text='An alternative name for this target', max_length=100, verbose_name='Name 2'),
        ),
        migrations.AlterField(
            model_name='target',
            name='name3',
            field=models.CharField(blank=True, default='', help_text='An alternative name for this target', max_length=100, verbose_name='Name 3'),
        ),
    ]

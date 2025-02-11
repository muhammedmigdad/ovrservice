# Generated by Django 5.1.4 on 2025-01-10 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_is_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_profile',
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False, verbose_name='Is customer'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_provider',
            field=models.BooleanField(default=False, verbose_name='Is provider'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_saparepart',
            field=models.BooleanField(default=False, verbose_name='Is saparepart'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

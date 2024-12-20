# Generated by Django 4.2.16 on 2024-11-11 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0002_alter_voter_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='vote1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voter',
            name='vote2',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voter',
            name='vote3',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voter',
            name='vote4',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voter',
            name='vote5',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voter',
            name='voterRegistration',
            field=models.TextField(default=False),
            preserve_default=False,
        ),
    ]

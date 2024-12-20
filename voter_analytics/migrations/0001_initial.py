# Generated by Django 4.2.16 on 2024-11-11 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.TextField()),
                ('first_name', models.TextField()),
                ('addressStreetNumber', models.IntegerField()),
                ('addressStreetName', models.TextField()),
                ('addressAptNum', models.TextField()),
                ('addressZipCode', models.IntegerField()),
                ('dob', models.DateField()),
                ('partyAffiliation', models.TextField()),
                ('voterScore', models.IntegerField()),
            ],
        ),
    ]

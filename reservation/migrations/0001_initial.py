# Generated by Django 4.2.20 on 2025-03-12 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_number', models.CharField(max_length=10)),
                ('origin', models.CharField(blank=True, max_length=30)),
                ('destination', models.CharField(blank=True, max_length=30)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('total_number_of_seats', models.IntegerField()),
                ('available_seats', models.IntegerField()),
            ],
        ),
    ]

# Generated by Django 5.0 on 2024-12-20 17:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('land_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('crop_type', models.CharField(choices=[('CEREAL', 'Cereal'), ('VEGETABLE', 'Vegetable'), ('FRUIT', 'Fruit'), ('LEGUME', 'Legume'), ('TUBER', 'Tuber'), ('OTHER', 'Other')], max_length=20)),
                ('variety', models.CharField(max_length=100)),
                ('planting_date', models.DateField()),
                ('expected_harvest_date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='land_management.field')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-planting_date'],
            },
        ),
    ]

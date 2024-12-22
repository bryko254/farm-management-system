# Generated by Django 5.0 on 2024-12-20 17:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_number', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('species', models.CharField(choices=[('CATTLE', 'Cattle'), ('SHEEP', 'Sheep'), ('GOAT', 'Goat'), ('PIG', 'Pig'), ('CHICKEN', 'Chicken'), ('OTHER', 'Other')], max_length=20)),
                ('breed', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=7)),
                ('status', models.CharField(choices=[('HEALTHY', 'Healthy'), ('SICK', 'Sick'), ('PREGNANT', 'Pregnant'), ('LACTATING', 'Lactating'), ('QUARANTINED', 'Quarantined')], default='HEALTHY', max_length=20)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('purchase_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('supplier', models.CharField(blank=True, max_length=200)),
                ('vaccination_status', models.BooleanField(default=False)),
                ('last_health_check', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offspring_as_father', to='livestock.animal')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offspring_as_mother', to='livestock.animal')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['tag_number'],
            },
        ),
        migrations.CreateModel(
            name='Breeding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breeding_date', models.DateField()),
                ('expected_due_date', models.DateField()),
                ('actual_birth_date', models.DateField(blank=True, null=True)),
                ('number_of_offspring', models.IntegerField(blank=True, null=True)),
                ('success', models.BooleanField(null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breeding_as_father', to='livestock.animal')),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breeding_as_mother', to='livestock.animal')),
            ],
            options={
                'ordering': ['-breeding_date'],
            },
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(choices=[('VACCINATION', 'Vaccination'), ('TREATMENT', 'Treatment'), ('CHECKUP', 'Regular Checkup'), ('INJURY', 'Injury'), ('DISEASE', 'Disease'), ('OTHER', 'Other')], max_length=20)),
                ('date', models.DateField()),
                ('condition', models.CharField(max_length=200)),
                ('treatment', models.TextField()),
                ('medication', models.CharField(blank=True, max_length=200)),
                ('dosage', models.CharField(blank=True, max_length=100)),
                ('vet_name', models.CharField(blank=True, max_length=200)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('notes', models.TextField(blank=True)),
                ('next_check_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='livestock.animal')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_type', models.CharField(choices=[('MILK', 'Milk'), ('EGGS', 'Eggs'), ('WOOL', 'Wool'), ('MEAT', 'Meat'), ('OTHER', 'Other')], max_length=20)),
                ('date', models.DateField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('unit', models.CharField(max_length=20)),
                ('quality_grade', models.CharField(blank=True, max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production_records', to='livestock.animal')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
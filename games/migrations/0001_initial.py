# Generated by Django 5.0.6 on 2024-06-24 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=100)),
                ('index', models.CharField(max_length=100)),
            ],
        ),
    ]

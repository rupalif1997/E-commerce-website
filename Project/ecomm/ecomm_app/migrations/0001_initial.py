# Generated by Django 4.2.5 on 2024-01-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=50)),
                ('upass', models.CharField(max_length=50)),
                ('ucpass', models.CharField(max_length=50)),
            ],
        ),
    ]

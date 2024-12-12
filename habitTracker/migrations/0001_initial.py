# Generated by Django 5.1.4 on 2024-12-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('days', models.JSONField(default=list)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('streak', models.PositiveIntegerField(default=0)),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
    ]

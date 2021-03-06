# Generated by Django 3.1.7 on 2021-04-02 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('hitman', 'Hitman'), ('boss', 'Boss'), ('leader', 'Big Boss')], max_length=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('target', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('new', 'New'), ('assigned', 'Assigned'), ('failed', 'Failed'), ('completed', 'Completed')], max_length=10)),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

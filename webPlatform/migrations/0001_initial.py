# Generated by Django 2.0.1 on 2018-01-14 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


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
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[200, 200], upload_to='documents/avatar/%Y/%m/%d', verbose_name='Foto perfil')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_score', models.IntegerField(db_index=True, default=0)),
                ('num_vote_up', models.PositiveIntegerField(db_index=True, default=0)),
                ('num_vote_down', models.PositiveIntegerField(db_index=True, default=0)),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('url', models.CharField(blank=True, default='', max_length=254, null=True, unique=True, verbose_name='Enlace a código fuente')),
                ('is_public', models.BooleanField(default=True, verbose_name='¿Es visible?')),
                ('number_likes', models.IntegerField(blank=True, null=True, verbose_name='Número de likes')),
                ('use_library', models.BooleanField(default=True, verbose_name='¿Utiliza Librería BeBot?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('in_library', models.BooleanField(default=True, verbose_name='¿Esta integrado en BeBot Library?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('url', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Enlace a pagina oficial')),
                ('category', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Clasificación propia del proveedor')),
                ('in_library', models.BooleanField(default=True, verbose_name='¿Esta integrado en BeBot Library?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicios', to='webPlatform.Provider', verbose_name='Proveedor del servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
                ('type_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to=settings.AUTH_USER_MODEL, verbose_name='Tipo de tag')),
            ],
        ),
        migrations.CreateModel(
            name='TypeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, default='', max_length=600, null=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha última modificación')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='providers',
            field=models.ManyToManyField(blank=True, related_name='proveedores', to='webPlatform.Provider', verbose_name='Proveedores utilizados'),
        ),
        migrations.AddField(
            model_name='project',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='servicios', to='webPlatform.Service', verbose_name='Servicios utilizados'),
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fuente', to='webPlatform.Source', verbose_name='Proveedor código fuente'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='webPlatform.Tag', verbose_name='Tags que describen el proyecto'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proyectos', to=settings.AUTH_USER_MODEL, verbose_name='Dueño del registro'),
        ),
    ]

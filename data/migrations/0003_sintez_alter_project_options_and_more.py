# Generated by Django 4.2 on 2023-04-12 16:36

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0002_project_remove_categoryproperty_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sintez',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название синтеза')),
                ('name_slug', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('code', models.IntegerField(default=0, verbose_name='Код')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('end_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('status', models.BooleanField(default=None, verbose_name='Статус')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sintezes/', verbose_name='Изображение')),
                ('smiles_formula', models.TextField(blank=True, null=True, verbose_name='Формула формата SMILES')),
            ],
            options={
                'verbose_name': 'Синтез',
                'verbose_name_plural': 'Синтез',
            },
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='image_full',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.AddField(
            model_name='project',
            name='owners',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4),
        ),
        migrations.CreateModel(
            name='SintezStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sintez_step/', verbose_name='Изображение')),
                ('sintez', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='data.sintez')),
            ],
            options={
                'verbose_name': 'Шаг синтеза ',
                'verbose_name_plural': 'Шаг синтеза',
            },
        ),
        migrations.CreateModel(
            name='SintezImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sintez_step/', verbose_name='Изображение')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('sintez', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='data.sintez')),
            ],
            options={
                'verbose_name': 'Изображение синтеза ',
                'verbose_name_plural': 'Изображение синтеза',
            },
        ),
        migrations.CreateModel(
            name='SintezFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='sintez_file/', verbose_name='Файл')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('sintez', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='data.sintez')),
            ],
            options={
                'verbose_name': 'Файл синтеза ',
                'verbose_name_plural': 'Файл синтеза',
            },
        ),
        migrations.AddField(
            model_name='sintez',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sintezes', to='data.project'),
        ),
        migrations.AddField(
            model_name='sintez',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
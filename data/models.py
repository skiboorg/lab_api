from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify
import uuid

class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    owners = models.ManyToManyField('user.User', blank=False, null=True)
    name = models.CharField('Название проекта', max_length=255, blank=False, null= True)
    name_slug = models.CharField(max_length=100, blank=True, null=True, editable=False)
    image = models.ImageField('Большое изображение', upload_to='projects/', blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    start_date = models.DateField('Стартовал',blank=True, null=True)
    end_date = models.DateField('Завершился',blank=True, null=True)
    updated_date = models.DateField('Обновлен',blank=True, null=True)
    ready_percent = models.IntegerField('Процент готовности', default=0,blank=True, null=True)
    total_hours = models.DecimalField('Потрачено часов', decimal_places=1, max_digits=4, blank=True, null=True,default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super().save(*args, **kwargs)


class Sintez(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    worker = models.ForeignKey('user.User',on_delete=models.SET_NULL, blank=False, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sintezes',blank=True, null=True)
    name = models.CharField('Название синтеза', max_length=255, blank=True, null= True)
    name_slug = models.CharField(max_length=100, blank=True, null=True, editable=False)
    code = models.CharField('Код',max_length=100, blank=True, null=True)
    hours = models.DecimalField('Потрачено часов', decimal_places=1, max_digits=4, blank=True, null=True)

    start_date = models.DateField('Дата проведения', blank=True, null=True)
    end_date = models.DateField('Дата обновления', auto_now=True)
    status = models.BooleanField('Статус', default=None,null=True)
    image = models.ImageField('Изображение', upload_to='sintezes/', blank=True, null=True)
    smiles_formula = models.TextField('Формула формата SMILES', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True, null=True)
    def __str__(self):
        return f'Синтез проекта {self.project.name} - {self.name}'

    class Meta:
        verbose_name = 'Синтез'
        verbose_name_plural = 'Синтез'

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)

        super().save(*args, **kwargs)

class SintezCard(models.Model):
    sintez = models.ForeignKey(Sintez, on_delete=models.CASCADE, related_name='cards', blank=False, null=True)
    order_num = models.IntegerField(default=1)
    is_first_card = models.BooleanField('Главный реактив', blank=True, null=True)
    is_final_card = models.BooleanField('Продукт', blank=True, null=True)
    formula_raw = models.CharField('Формула', max_length=255, blank=True, null=True)
    formula_calculated = models.CharField('Формула HTML', max_length=255, blank=True, null=True)
    formula_weight = models.DecimalField('Молекулярная масса', decimal_places=10, max_digits=20, blank=True, null=True, default=0)
    equavalent = models.DecimalField('Эквивалент', decimal_places=10, max_digits=20, blank=True, null=True, default=0)
    sample_weight = models.DecimalField('Масса образца', decimal_places=10, max_digits=20, blank=True, null=True, default=0)
    mmols = models.DecimalField('Количество молей', decimal_places=10, max_digits=20, blank=True, null=True, default=0)


    def __str__(self):
        return f'Карточка синтеза {self.sintez.name}'

    class Meta:
        ordering = ('-is_first_card', 'order_num', 'is_final_card', )
        verbose_name = 'Карточка синтеза '
        verbose_name_plural = 'Карточка синтеза'

class SintezStep(models.Model):
    sintez = models.ForeignKey(Sintez, on_delete=models.CASCADE, related_name='steps', blank=False, null=True)
    text = RichTextUploadingField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='sintez_step/', blank=True, null=True)

    def __str__(self):
        return f'Шаг синтеза {self.sintez.name}'

    class Meta:
        verbose_name = 'Шаг синтеза '
        verbose_name_plural = 'Шаг синтеза'

    # def save(self, *args, **kwargs):
    #     self.name_slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class SintezImage(models.Model):
    sintez = models.ForeignKey(Sintez, on_delete=models.CASCADE, related_name='images', blank=False, null=True)
    image = models.ImageField('Изображение', upload_to='sintez_step/', blank=True, null=True)
    text = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return f'Изображение синтеза {self.sintez.name}'

    class Meta:
        verbose_name = 'Изображение синтеза '
        verbose_name_plural = 'Изображение синтеза'

    # def save(self, *args, **kwargs):
    #     self.name_slug = slugify(self.name)
    #     super().save(*args, **kwargs)

class SintezFile(models.Model):
    sintez = models.ForeignKey(Sintez, on_delete=models.CASCADE, related_name='files', blank=False, null=True)
    file = models.FileField('Файл', upload_to='sintez_file/', blank=True, null=True)
    text = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return f'Файл синтеза {self.sintez.name}'

    class Meta:
        verbose_name = 'Файл синтеза '
        verbose_name_plural = 'Файл синтеза'

    # def save(self, *args, **kwargs):
    #     self.name_slug = slugify(self.name)
    #     super().save(*args, **kwargs)



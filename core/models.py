from django.db import models
from django.utils.text import slugify
from transliterate import translit

# Уровень образования 
class EducationLevel(models.TextChoices):
    BACHELOR = 'bachelor', 'Бакалавриат'
    MASTER = 'master', 'Магистратура'
    SPECIALIST = 'specialist', 'Специалитет'
    SPE = 'srednee', 'Орто кесиптик'

# Форма обучения 
class StudyForm(models.TextChoices):
    FULL_TIME = 'full_time', 'Күндүзгү'
    PART_TIME = 'part_time', 'Сырттан'

# =======================
# Основные 
# =======================

# Таблица направление 
class Major(models.Model):
    name = models.CharField('Направление', max_length=255)
    code = models.CharField('Шифр', max_length=20, unique=True)
    edu_level = models.CharField(
        'Уровень образования', 
        max_length=20,
        choices=EducationLevel.choices
    )

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ["name"]

    def __str__(self):
        return f'{self.code} - {self.name}'


# Таблица профиль 
class Profile(models.Model):
    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Направление'
    )

    name = models.CharField('Профиль', max_length=255)

    slug = models.SlugField(
        'Slug', 
        max_length=255, 
        unique=True, 
        blank=True,
        editable=False
    )

    study_form = models.CharField(
        'Форма обучения',
        max_length=20,
        choices=StudyForm.choices
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ["major", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, 'ru', reversed=True)
            base_slug = slugify(latin_name)
            slug = base_slug
            counter = 1

            while Profile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} - {self.major.name}'


# =======================
# Документы профиля
# =======================

# Таблица модули / дисциплинны 
class Module(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Профиль'
    )

    name = models.CharField('Название дисциплины', max_length=255)
    annotation = models.FileField('Аннотация', upload_to="modules/annotation/", blank=True, null=True)
    syllabus = models.FileField('Рабочая программа', upload_to="modules/syllabus/", blank=True, null=True)
    assesment_fund = models.FileField(
        'Фонд оценочных средств', 
        upload_to="modules/assesment/", 
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Дисциплина / Модуль / Практика'
        verbose_name_plural = 'Дисциплины / Модули / Практики'
    
    def __str__(self):
        return f"{self.name} - {self.profile.name}"


# Документы профиля 
class ProfileDocument(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Профиль'
    )

    title = models.CharField('Название документа', max_length=255)
    file = models.FileField('Файл', upload_to='profiles/', blank=True, null=True)

    class Meta:
        verbose_name = 'Документ профиля'
        verbose_name_plural = 'Документы профиля'

    def __str__(self):
        return f"{self.title} - {self.profile.name}"


# Паспорта компетенций
class CompetencePassport(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='competence_passports',
        verbose_name='Профиль'
    )

    title = models.CharField('Название документа', max_length=255)
    file = models.FileField('Файл', upload_to='passports/', blank=True, null=True)

    class Meta:
        verbose_name = 'Паспорт / Программа компетенций'
        verbose_name_plural = 'Паспорта / Программы компетенций'

    def __str__(self):
        return f"{self.title} — {self.profile.name}"


# =======================
# Глобальные документы
# =======================
 
# Лицензия 
class License(models.Model):
    title = models.CharField('Название лицензии', max_length=255)
    file = models.FileField('Изображение', upload_to="images/license/", blank=True, null=True)

    text = models.TextField('Описание', default="")

    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

    def __str__(self):
        return f'{self.title} - {self.text}'


# Приказ
class Order(models.Model):

    CATEGORY = [
        ('kr_laws', 'Кыргыз Республикасынын мыйзамдары'),
        ('gov_resolution', 'Кыргыз Республикасынын Өкмөтүнүн жоболору'),
        ('ministry_orders', 'Кыргыз Республикасынын Илим, жогорку билим берүү министрлигинин буйруктары'),
        ('nsu_orders', 'Нарын мамлекеттик университетинин буйруктары'),
        ('gos', 'ГОС'),
        ('smk1', 'CMK 1'),
        ('smk2', 'CMK 2'),
        ('smk3', 'CMK 3'),
        ('smk4', 'CMK 4'),
        ('smk5', 'CMK 5'),
    ]

    title = models.CharField('Название приказа', max_length=255)
    file = models.FileField('Файл', upload_to='orders/')
    category = models.CharField('Категория', max_length=50, choices=CATEGORY, default='nsu_orders')

    class Meta:
        verbose_name = 'Закон/Приказ'
        verbose_name_plural = 'Законы / Приказы / Постановлении'

    def __str__(self):
        return self.title


# Учебное расписание
class Schedule(models.Model):
 
    FACULTIES = [
        ('atf', 'Агрардык-техникалык факультети'),
        ('ped', 'Педагогика факультети'),
        ('phil', 'Филология факультети'),
        ('econom', 'Экономика жана табигый-гуманитардык илимдер факультети'),
        ('it', 'Чет тилдери жана компьютердик системаларды программалоо'),
    ]  

    title = models.CharField('Название', max_length=255)
    file = models.FileField('Файл (PDF)', upload_to='schedules/')
    faculty = models.CharField(
        'Факультет/колледж',
        max_length=100,
        choices=FACULTIES,
        default='atf'
    )
 
    class Meta:
        verbose_name = 'Учебное расписание'
        verbose_name_plural = 'Учебные расписания'
        ordering = ['faculty', 'title']

    def __str__(self):
        return self.title
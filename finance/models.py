from django.db import models
from django.db.models import F


class Institution(models.Model):
    class Kind(models.TextChoices):
        SCHOOL = "school", "Школа"
        KINDERGARTEN = "kindergarten", "Детский сад"

    name = models.CharField("Название", max_length=150, unique=True)
    kind = models.CharField("Тип", max_length=20, choices=Kind.choices)

    class Meta:
        verbose_name = "Учреждение"
        verbose_name_plural = "Учреждения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudyGroup(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="groups",
        verbose_name="Учреждение",
    )
    name = models.CharField("Название", max_length=50)

    class Meta:
        verbose_name = "Класс / группа"
        verbose_name_plural = "Классы / группы"
        ordering = ["institution__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "name"],
                name="unique_group_per_institution",
            )
        ]

    def __str__(self):
        return f"{self.institution} — {self.name}"


class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="Класс / группа",
    )
    is_active = models.BooleanField("Учится", default=True)

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Parent(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    telegram_id = models.BigIntegerField(
        "Telegram ID", null=True, blank=True, unique=True
    )
    children = models.ManyToManyField(
        Student,
        related_name="parents",
        verbose_name="Дети",
    )

    class Meta:
        verbose_name = "Родитель"
        verbose_name_plural = "Родители"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Event(models.Model):
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="Класс / группа",
    )
    title = models.CharField("Название", max_length=150)
    date = models.DateField("Дата мероприятия", null=True, blank=True)
    total_cost = models.DecimalField("Стоимость, ₸", max_digits=12, decimal_places=2)
    from_piggy_bank = models.DecimalField(
        "Из копилки, ₸", max_digits=12, decimal_places=2, default=0
    )
    rounding_step = models.DecimalField(
        "Округлять до, ₸", max_digits=8, decimal_places=2, default=100
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["-date", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_cost__gte=0),
                name="event_total_cost_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(from_piggy_bank__gte=0),
                name="event_from_piggy_bank_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(rounding_step__gt=0),
                name="event_rounding_step_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(from_piggy_bank__lte=F("total_cost")),
                name="event_piggy_bank_not_more_than_cost",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.group})"

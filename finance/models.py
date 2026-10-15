from django.db import models


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

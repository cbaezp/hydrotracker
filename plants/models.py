from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SeedTray(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    x_size = models.PositiveIntegerField()
    y_size = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class HydroponicGrower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ORIENTATION_CHOICES = [
        ("vertical", "Vertical"),
        ("horizontal", "Horizontal"),
    ]
    name = models.CharField(max_length=100)
    x_size = models.PositiveIntegerField()
    y_size = models.PositiveIntegerField()
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES)

    def __str__(self):
        return self.name


class PlantInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    notes = models.TextField()

    def __str__(self):
        return self.name


class Plant(models.Model):
    STAGE_CHOICES = [
        ("germination", "Germination"),
        ("growing", "Growing"),
        ("cropped", "Cropped"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_info = models.OneToOneField(PlantInfo, on_delete=models.CASCADE)
    n_seeds_used = models.PositiveIntegerField()
    current_stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    datetime_germination_to_growing = models.DateTimeField(null=True, blank=True)
    datetime_growing_to_cropped = models.DateTimeField(null=True, blank=True)
    position_x = models.PositiveIntegerField(null=True, blank=True)
    position_y = models.PositiveIntegerField(null=True, blank=True)
    seed_tray = models.ForeignKey(
        SeedTray,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plants",
    )
    hydroponic_grower = models.ForeignKey(
        HydroponicGrower,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plants",
    )

    def update_stage(self, new_stage):
        valid_transitions = {"germination": "growing", "growing": "cropped"}

        if valid_transitions.get(self.current_stage) != new_stage:
            raise ValidationError(
                f"Cannot transition from {self.current_stage} to {new_stage}"
            )

        if new_stage == "growing":
            self.datetime_germination_to_growing = timezone.now()
        elif new_stage == "cropped":
            self.datetime_growing_to_cropped = timezone.now()

        self.current_stage = new_stage
        self.save()

    def save(self, *args, **kwargs):
        # Ensure that a Plant can only be in one location at a time.
        if self.current_stage == "germination":
            self.hydroponic_grower = None
        elif self.current_stage in ["growing", "cropped"]:
            self.seed_tray = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plant_info.name} - {self.current_stage}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seed_tray", "position_x", "position_y"],
                name="unique_position_in_seedtray",
            ),
            models.UniqueConstraint(
                fields=["hydroponic_grower", "position_x", "position_y"],
                name="unique_position_in_hydroponicgrower",
            ),
        ]

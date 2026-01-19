from django.db import models
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FreelancerProfile(models.Model):
    # Comes from JWT (Auth Service)
    user_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=150)
    title = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    profile_image = models.ImageField(
        upload_to="freelancer_profiles/",
        blank=True,
        null=True
    )


    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    skills = models.ManyToManyField(Skill,related_name="freelancers",blank=True)

    availability = models.CharField(
        max_length=20,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("freelance", "Freelance")
        ],
        default="freelance"
    )

    languages = models.CharField(
        max_length=200,
        help_text="Comma-separated languages (e.g., English, Hindi)"
    )

    portfolio_url = models.URLField(blank=True)

    # Profile Stats
    total_jobs_completed = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )

    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_seen = models.DateTimeField(null=True, blank=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} (User ID: {self.user_id})"

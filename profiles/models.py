from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import reverse

from .models_utils import get_likes_received_count, get_list_of_profiles_by_user


class Association(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Profile Model

class ProfileManager(models.Manager):
    def get_my_friends_profiles(self, user):
        users = Profile.objects.get(user=user).friends.all()
        profiles = get_list_of_profiles_by_user(users)
        return profiles


class Profile(models.Model):
    """
    This model gets created automatically everytime a new user sign ups
    """

    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    pseudo = models.CharField(max_length=200, blank=True)
    
    promo = models.CharField(max_length=10, blank=True)
    assos = models.ManyToManyField(Association, blank=True)

    CATEGORIES = [
        ('etudiant', 'Étudiant/e'),
        ('administration', 'Administration'),
        ('association', 'Association'),
        ('convention', 'Soirée Convention Étudiante'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORIES, default='etudiant')

    bio = models.TextField(default="No Bio..", max_length=300, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(
        default="avatar.png",
        upload_to="avatars/",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    following = models.ManyToManyField(
        User,
        blank=True,
        related_name="following",
    )
    followers = models.ManyToManyField(
        User,
        blank=True,
        related_name="followers",
    )
    display_site_explanation = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse(
            "profiles:profile-detail-view",
            kwargs={"slug": self.slug},
        )
        

    def get_display_name(self):
        if self.pseudo:
            return self.pseudo
        
        return self.get_category_display()

    def save(self, *args, **kwargs):
        self.slug = str(self.user)
        super().save(*args, **kwargs)

    # Methods for profile details #

    def get_votes_given_count(self):
        from posts.models import Power
        votes = Power.objects.filter(profile=self)
        return len(votes)

    def get_votes_received_count(self):
        posts = self.posts.all()

        total_liked = get_likes_received_count(posts)

        return total_liked

    def get_nb_favorite_posts(self):
        from posts.models import Like
        favorites = Like.objects.filter(profile=self)
        return len(favorites)

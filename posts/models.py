from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Sum

from profiles.models import Profile
from profiles.views_utils import get_request_user_profile

from .models_utils import get_related_posts_queryset
import colorsys


class PostManager(models.Manager):
    def get_related_posts(self, user):
        profile = get_request_user_profile(user)
        friends = profile.friends.all()
        following = profile.following.all()

        related_posts = get_related_posts_queryset(profile, friends, following)

        return related_posts


class Choice(models.Model):
    """
    Model to store dynamic choices for themes
    """
    theme_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.theme_name

Choice.objects.get_or_create(theme_name='aucun')

class Post(models.Model):
    """
    This model is used to show results in main.html
    """

    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    #default_theme = Choice.objects.get(theme_name='aucun')

    theme = models.ForeignKey(Choice, on_delete=models.CASCADE)
    image = models.ImageField(
        blank=True,
        upload_to="posts",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    powered = models.ManyToManyField(Profile, blank=True, related_name="powers")

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"{self.author} - {str(self.content)[:50].strip()}.."
        return f"{self.author} - {str(self.content)}"

    def num_comments(self):
        return self.comment_set.all().count()
    
    @property
    def nombre_votant(self):
        all_power_objects = Power.objects.filter(post = self)
        return len(all_power_objects)

    @property
    def get_all_power(self):
    
        all_power_objects = Power.objects.filter(post = self)

        total_power = sum([int(power_object.power) for power_object in all_power_objects])

        return total_power if total_power else 0 

    @property
    def get_max_power(self):
        all_power_objects = Power.objects.filter(post = self)

        return len(all_power_objects)*4
    
    
    @property
    def progress(self):
        if not self.get_max_power:
            return 0

        return (self.get_all_power/self.get_max_power)*100
    
    @property
    def get_color_progress(self):
        hue = self.progress/100
        # Convertir la teinte en une couleur RVB
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)

        # Convertir les valeurs RVB en valeurs entières de 0 à 255
        rgb_int = tuple(int(x * 255) for x in rgb)

        rgb_int = (int((1-hue) * 255), int(hue * 255), int(hue * 255 * 0.5))

        # Formater la couleur en format CSS (chaîne hexadécimale)
        color_hex = "#{:02x}{:02x}{:02x}".format(*rgb_int)

        return color_hex


    class Meta:
        ordering = ("-created",)


class Comment(models.Model):
    """
    This model is used in Posts for comments
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} - {self.content}"


class Like(models.Model):
    """
    This model is used to leave likes on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} liked {self.post}"
    

class Power(models.Model):
    """
    This model is used to leave power on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    power = models.CharField(max_length=5, blank=True)
    
    def __str__(self):
        return f"{self.profile} put {self.power}/5 on {self.post}"

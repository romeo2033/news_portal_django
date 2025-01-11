from django.db import models
import accounts.models as account_models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article ,'Cтатья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(account_models.Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POSITIONS, default=article)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(account_models.User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


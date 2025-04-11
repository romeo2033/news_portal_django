from django.contrib.auth.models import User
from django.db import models
import news.models as news_models

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        updated_rating = 0

        posts_ratings = news_models.Post.objects.filter(author=self).values('rating')
        for rating in posts_ratings:
            updated_rating += rating['rating'] * 3

        comments_ratings = news_models.Comment.objects.filter(user=self.user).values('rating')
        for rating in comments_ratings:
            updated_rating += rating['rating']

        comments_on_posts_ratings = news_models.Comment.objects.filter(post__author=self).values('rating')
        for rating in comments_on_posts_ratings:
            updated_rating += rating['rating']

        self.rating = updated_rating
        self.save()

    def __str__(self):
        return self.user.username
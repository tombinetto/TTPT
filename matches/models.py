from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo_rating = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username} - Elo: {self.elo_rating}"

class Match(models.Model):
    player1 = models.ForeignKey(User, related_name='player1_matches', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2_matches', on_delete=models.CASCADE)
    player1_score = models.IntegerField
    player2_score = models.IntegerField
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2} on {self.date_played}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_elo()
    
    def calculate_elo(self):
        k = 32

        expected_score1 = 1 / (1 + 10 ** ((self.player2.elo_rating - self.player1.elo_rating) / 400))
        expected_score2 = 1 / (1 + 10 ** ((self.player1.elo_rating - self.player2.elo_rating) / 400))

        if self.player1_score > self.player2_score:
            actual_score1 = 1
            actual_score2 = 0
        else:
            actual_score1 = 0
            actual_score2 = 1

        # Calculate new ratings
        new_rating1 = self.player1.elo_rating + k * (actual_score1 - expected_score1)
        new_rating2 = self.player2.elo_rating + k * (actual_score2 - expected_score2)

        # Update player ratings
        self.player1.elo_rating = round(new_rating1)
        self.player2.elo_rating = round(new_rating2)

        # Save the updated ratings
        self.player1.save()
        self.player2.save()
# Create your models here.

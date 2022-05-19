from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.pk})    
    def __str__(self):
        return self.name

class Gorilla(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy, blank=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'gorilla_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    gorilla = models.ForeignKey(Gorilla, on_delete = models.CASCADE)
  
    def __str__(self):
        return f"Photo for gorilla_id: {self.gorilla.id} @ {self.url}"
    
class Feeding(models.Model):
    date = models.DateField("feeding date")
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    gorilla = models.ForeignKey(Gorilla, on_delete = models.CASCADE)
    
    class Meta:
        ordering = ['-date']
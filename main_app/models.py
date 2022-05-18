from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    
    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'pk': self.pk})    
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
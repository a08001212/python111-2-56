from django.db import models
class HBicycleData(models.Model):
    sna = models.CharField(max_length=100)
    sbi = models.IntegerField(default=0)
    tot = models.IntegerField(default=0)
    class Meta:
        ordering = ('-sbi',)
    def __str__(self):
        return self.sna

class NKUSTnews(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class PhoneMaker(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class PhoneModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    maker = models.ForeignKey(PhoneMaker, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-price"]

class StockInfo(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    mprice = models.FloatField()

    def __str__(self):
        return self.name

class Oil(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    def __str__(self):
        return self.name

class Codeforces_data(models.Model):
    name = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['ranking']

class Cpe(models.Model):
    name = models.CharField(max_length=30)
    average = models.FloatField(default=.0)

    def __str__(self):
        return self.name

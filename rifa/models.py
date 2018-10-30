from django.contrib.auth import get_user_model
from django.db import models

def raffle_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/raffle_<id>/<filename>
    return 'raffle_{0}/{1}'.format(instance.raffle.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=400, blank=True, null=True)


class Raffle(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=500, blank=False, null=False)
    pub_date = models.DateTimeField('publish date')
    qtd_num = models.IntegerField(blank=False, null=False)
    value = models.FloatField(blank=False, null=False)
    limit_date = models.DateTimeField('limit date')
    choosed_num = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Choice(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    number = models.IntegerField(blank=False, null=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='choices')
    date = models.DateTimeField('choose date')


class Image(models.Model):
    img = models.ImageField(upload_to=raffle_directory_path)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='images')
    main = models.BooleanField(default=True)


class Reputation(models.Model):
    SCORES = [(i,i) for i in range(1,6)]
    user_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    user_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    score = models.IntegerField(blank=False, null=False, choices=SCORES)
    comment = models.CharField(max_length=200, blank=True, null=True)
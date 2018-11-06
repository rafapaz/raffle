from django.contrib.auth import get_user_model
from django.db import models


def raffle_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/raffle_<id>/<filename>
    return 'raffle_{0}/{1}'.format(instance.raffle.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.name


class Raffle(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Título')
    desc = models.CharField(max_length=500, blank=False, null=False, verbose_name='Descrição')
    pub_date = models.DateTimeField(verbose_name='Publicado em')
    qtd_num = models.IntegerField(blank=False, null=False, verbose_name='Quantidade de números')
    value = models.FloatField(blank=False, null=False, verbose_name='Valor unitário')
    limit_date = models.DateTimeField(verbose_name='Data do sorteio')
    choosed_num = models.IntegerField(blank=True, null=True, verbose_name='Número sorteado')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')

    def __str__(self):
        return self.title


class Choice(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    number = models.IntegerField(blank=False, null=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='choices')
    date = models.DateTimeField('choose date')

    def __str__(self):
        return self.user.username + ' / ' + self.raffle.title


class Image(models.Model):
    img = models.ImageField(upload_to=raffle_directory_path)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='images')
    main = models.BooleanField(default=False)

    def __str__(self):
        return str(self.img) + ' / ' + self.raffle.title


class Reputation(models.Model):
    SCORES = [(i, i) for i in range(1, 6)]
    user_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    user_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='reputations')
    score = models.IntegerField(blank=False, null=False, choices=SCORES)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user_from.username + ' -> ' + self.user_to.username


class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=200, blank=False, null=False)
    answer = models.CharField(max_length=200, blank=True, null=True)

from django.db import models
from django.conf import settings


class Wallet(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )

    def __str__(self):
        return self.title


class AccountStatement(models.Model):
    value = models.FloatField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value)


class Currency(models.Model):
    code = models.CharField(max_length=4)
    value = models.ForeignKey(AccountStatement, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class DiffOperation(models.Model):
    OPERATION_TYPES = (
        ('SP', 'Spending'),
        ('DP', 'Deposit')
    )

    title = models.CharField(max_length=50)
    date = models.DateField()
    sum = models.FloatField()
    operation_type = models.CharField(max_length=2, choices=OPERATION_TYPES)
    wallet_title = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

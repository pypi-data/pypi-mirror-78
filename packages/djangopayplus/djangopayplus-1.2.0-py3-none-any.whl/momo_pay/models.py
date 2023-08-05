from django.db import models
from django.contrib.auth.models import User
from momopay.classes import enum



class Credit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    currency = models.CharField(max_length=10, default="GHS")
    total_credited = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    total_used = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.user.username, self.current_balance)

    def enoughBalance(self, amount):
        if self.current_balance >= amount:
            return True
        return False

    def debitBalance(self, amount):
        self.current_balance = models.F('current_balance') - amount
        self.total_used = models.F('total_used') + amount
        self.save()

    def creditBalance(self, amount):
        self.current_balance = models.F('current_balance') + amount
        self.total_credited = models.F('total_credited') + amount
        self.save()

    def reverseDebitBalance(self, amount):
        self.current_balance = models.F('current_balance') + amount
        self.total_credited = models.F('total_credited') + amount
        self.save()

    def reverseCreditBalance(self, amount):
        self.current_balance = models.F('current_balance') - amount
        self.total_used = models.F('total_used') + amount
        self.save()


class CreditTransaction(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    transacted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    transaction_amount = models.DecimalField(max_digits=14, decimal_places=4)
    balance_before = models.DecimalField(max_digits=14, decimal_places=4)
    balance_after = models.DecimalField(max_digits=14, decimal_places=4)
    medium = models.IntegerField(choices=enum.TransactionMediumTypes.choices())
    transaction_type = models.IntegerField(choices=enum.CreditTransactionTypes.choices())
    extra_info = models.CharField(max_length=255, null=True)
    channel = models.IntegerField(choices=enum.ApplicationChannels.choices())
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)



class MomoTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    network = models.IntegerField(choices=enum.NetworkTypes.choices())
    msisdn = models.CharField(max_length=20)
    status = models.IntegerField(choices=enum.StatusTypes.choices(), default=enum.StatusTypes.PENDING)
    info_sent = models.TextField()
    initial_callback = models.CharField(max_length=255, null=True)
    final_callback = models.CharField(max_length=255, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    credit_transaction = models.OneToOneField(CreditTransaction, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=50, unique=True)
    ext_id = models.CharField(max_length=50,null=True)
    channel  = models.IntegerField(choices=enum.ApplicationChannels.choices(),null=True)

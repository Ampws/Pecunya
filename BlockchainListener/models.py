from django.db import models

class EthereumTransaction(models.Model):
    blockHash = models.CharField(max_length=66, db_index=True)
    blockNumber = models.BigIntegerField(null=True, blank=True, db_index=True)
    tx_from = models.CharField(max_length=42, null=True, blank=True, db_index=True)
    gas = models.BigIntegerField(null=True, blank=True)
    gasPrice = models.BigIntegerField(null=True, blank=True)
    maxFeePerGas = models.BigIntegerField(null=True, blank=True)
    maxPriorityFeePerGas = models.BigIntegerField(null=True, blank=True)
    hash = models.CharField(max_length=66, unique=True, primary_key=True)
    input = models.TextField(null=True, blank=True)
    nonce = models.BigIntegerField(null=True, blank=True)
    to = models.CharField(max_length=42, null=True, blank=True, db_index=True)
    transactionIndex = models.PositiveIntegerField(null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    type = models.PositiveIntegerField(null=True, blank=True)
    accessList = models.TextField(null=True, blank=True)
    chainId = models.PositiveIntegerField(null=True, blank=True)
    v = models.BigIntegerField(null=True, blank=True)
    r = models.CharField(max_length=66, null=True, blank=True)
    s = models.CharField(max_length=66, null=True, blank=True)
    yParity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.hash

    class Meta:
        verbose_name = 'Ethereum Transaction'
        verbose_name_plural = 'Ethereum Transactions'

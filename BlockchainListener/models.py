from django.db import models

class TokenDetail(models.Model):
    chain_name = models.CharField(max_length=100)
    chain_id = models.PositiveIntegerField()
    contract_address = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
    creator = models.CharField(max_length=256)
    token_amount = models.DecimalField(max_digits=18, decimal_places=6)

    class Meta:
        verbose_name = "Token Detail"
        verbose_name_plural = "Token Details"

    def __str__(self):
        return f"Token Detail - Transaction Hash: {self.contract_address}"

from django.db import models
from clients.models import Client




class Estimate(models.Model):
    
    CURRENCY_CHOICES = [
    ('KRW', '원'),
    ('USD', '달러'),
    ('CNY', '위안'),
]

    STATUS_CHOICES = [
    ('draft', '대기'),
    ('confirmed', '수주'),
    ('completed', '완료'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="고객사")
    title = models.CharField(max_length=200, verbose_name="견적명")
    amount = models.IntegerField(verbose_name="금액")
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='KRW')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="상태"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        verbose_name = "견적"
        verbose_name_plural = "견적 목록"

    def __str__(self):
        return self.title
    
class EstimateItem(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200, verbose_name="품목명")
    price = models.IntegerField(verbose_name="단가")
    quantity = models.IntegerField(verbose_name="수량")

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name
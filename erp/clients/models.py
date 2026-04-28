from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="고객사명")
    address = models.TextField(blank=True, verbose_name="주소")

    class Meta:
        verbose_name = "고객사"
        verbose_name_plural = "고객사 목록"

    def __str__(self):
        return self.name


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="고객사")
    name = models.CharField(max_length=100, verbose_name="담당자명")
    phone = models.CharField(max_length=50, blank=True, verbose_name="전화번호")

    class Meta:
        verbose_name = "담당자"
        verbose_name_plural = "담당자 목록"

    def __str__(self):
        return self.name
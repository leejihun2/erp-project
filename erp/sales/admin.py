from django.contrib import admin
from django.utils.html import format_html
from .models import Estimate, EstimateItem


class EstimateItemInline(admin.TabularInline):
    model = EstimateItem
    extra = 1


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'created_at', 'total_amount', 'download_pdf')
    inlines = [EstimateItemInline]

    def total_amount(self, obj):
        return sum(item.get_total() for item in obj.items.all())
    total_amount.short_description = "총 금액"

    def download_pdf(self, obj):
        return format_html(
            '<a class="button" href="/sales/estimate/{}/pdf/" target="_blank">PDF 다운로드</a>',
            obj.id
        )
    download_pdf.short_description = "견적서"
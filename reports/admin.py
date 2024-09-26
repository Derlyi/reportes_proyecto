from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponse  # Importa HttpResponse para descargar PDF
from .models import SalesReport
from .forms import SalesReportForm
from .views import sales_report_pdf

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/sales_report.html"
    list_display = ['order', 'report_date', 'total_amount', 'status', 'download_report']
    list_filter = ['report_date', 'status']

    def changelist_view(self, request, extra_context=None):
        form = SalesReportForm(request.GET or None)
        context = {'form': form}

        if form.is_valid():
            return sales_report_pdf(request)  # Genera el PDF cuando el formulario es válido

        return TemplateResponse(request, "admin/sales_report.html", context)

    def download_report(self, obj):
        return format_html('<a class="button" href="{}">Descargar PDF</a>', f'/admin/reports/salesreport/{obj.id}/download-pdf/')
    
    download_report.short_description = "Descargar Reporte"
    download_report.allow_tags = True

    # Agrega una URL personalizada para el reporte en PDF
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/download-pdf/', self.admin_site.admin_view(self.sales_report_pdf_view), name='salesreport-download-pdf'),
        ]
        return custom_urls + urls

    # URL personalizada para descargar el reporte en PDF
    def sales_report_pdf_view(self, request, pk):
        report = SalesReport.objects.get(pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{pk}.pdf"'
        
        # Llama a la función en views.py para generar el PDF
        sales_report_pdf(report, response)
        
        return response



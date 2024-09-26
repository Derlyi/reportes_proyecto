import io
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from orders.models import Order
from .forms import SalesReportForm

def sales_report_pdf(request):
    # Inicializamos el formulario
    form = SalesReportForm(request.GET or None)
    orders = []
    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        orders = Order.objects.filter(created__range=[start_date, end_date])

    # Si no hay datos válidos, retornar un mensaje de error
    if not orders:
        return HttpResponse("No se encontraron pedidos para las fechas seleccionadas.", content_type='text/plain')

    # Crear el PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Encabezado
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, f"Informe de ventas del {start_date} al {end_date}")

    # Ajustes iniciales para la posición del texto
    y = 750
    p.setFont("Helvetica", 10)

    for order in orders:
        order_info = f"Pedido ID: {order.id} - Cliente: {order.first_name} {order.last_name} - Total: {order.get_total_cost():.2f}"
        p.drawString(100, y, order_info)
        y -= 20

        # Si el espacio vertical es insuficiente, crea una nueva página
        if y < 100:
            p.showPage()  # Añade nueva página
            p.setFont("Helvetica", 10)
            y = 800

    # Finalizar el PDF
    p.showPage()
    p.save()

    # Volver al inicio del buffer
    buffer.seek(0)

    # Devolver el archivo PDF como respuesta
    return FileResponse(buffer, as_attachment=True, filename=f'sales_report_{start_date}_to_{end_date}.pdf')


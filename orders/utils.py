# utils.py
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from .models import Order
import os

def create_invoice_pdf(order_id):
    # Obtener el pedido
    order = Order.objects.get(id=order_id)
    
    # Crear un buffer en memoria para el PDF
    buffer = BytesIO()

    # Crear un objeto SimpleDocTemplate para el PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    title_style.alignment = 0  # Alinear a la izquierda
    normal_style.alignment = 0  # Alinear a la izquierda

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear texto en la tabla a la izquierda
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica')
    ])

    # Contenido
    content = []

    # Encabezado con logotipo
    logo_path = 'orders/static/img/logo_v_pharma.png'  # Ruta directa al archivo
    if os.path.isfile(logo_path):
        logo = Image(logo_path, width=2*inch, height=1*inch)
        content.append(logo)
    else:
        content.append(Paragraph('Logotipo no encontrado', normal_style))

    # Información de la empresa
    content.append(Paragraph('V-Pharma', title_style))
    content.append(Paragraph('Número Teléfono: 312 6647917', normal_style))
    content.append(Paragraph('Correo: v-pharma@gmail.com', normal_style))
    content.append(Paragraph('<br/>', normal_style))  # Espacio adicional
    
    # Detalles de la factura
    content.append(Paragraph(f'Factura #{order.id}', title_style))
    content.append(Paragraph(f'Fecha: {order.created.strftime("%Y-%m-%d")}', normal_style))
    content.append(Paragraph(f'Nombre: {order.first_name} {order.last_name}', normal_style))
    content.append(Paragraph(f'Correo: {order.email}', normal_style))
    content.append(Paragraph(f'Dirección: {order.address}', normal_style))
    content.append(Paragraph(f'Código Postal: {order.postal_code}', normal_style))
    content.append(Paragraph(f'Ciudad: {order.city}', normal_style))
    content.append(Paragraph('<br/>', normal_style))  # Espacio adicional
    content.append(Paragraph('<br/>', normal_style))  # Espacio adicional
    content.append(Paragraph('<br/>', normal_style))  # Espacio adicional
    content.append(Paragraph('<br/>', normal_style))  # Espacio adicional

    
    # Tabla de detalles de la orden
    data = [['Cantidad', 'Producto', 'Precio']]
    for item in order.items.all():
        data.append([item.quantity, item.product.name, f'${item.price}'])
    data.append(['', 'Total', f'${order.get_total_cost()}'])
    
    table = Table(data)
    table.setStyle(table_style)
    content.append(table)

    # Pie de página
    content.append(Paragraph('<br/><br/>', normal_style))
    content.append(Paragraph('¡Gracias por tu compra!', normal_style))
    content.append(Paragraph('Esta es una factura descargable. Por favor guárdelo para sus registros.', normal_style))
    
    # Construir el PDF
    doc.build(content)

    # Obtener el contenido del PDF
    pdf_content = buffer.getvalue()
    buffer.close()

    # Crear una respuesta HTTP para el archivo PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    return response

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from io import BytesIO
import os
from datetime import datetime


def _draw_table(c, x, y, col_widths, data, row_height=8 * mm):
    # Simple table draw (headers in first row)
    total_width = sum(col_widths)
    # Draw header background
    c.setFillColor(colors.lightgrey)
    c.rect(x, y - row_height, total_width, row_height, fill=1, stroke=0)
    c.setFillColor(colors.black)
    # Draw vertical lines and text
    cur_x = x
    for i, w in enumerate(col_widths):
        # header text
        header = data[0][i]
        c.setFont('Helvetica-Bold', 9)
        c.drawString(cur_x + 2 * mm, y - row_height + 2 * mm, str(header))
        cur_x += w
    # rows
    c.setFont('Helvetica', 9)
    y_row = y - row_height
    for row in data[1:]:
        y_row -= row_height
        cur_x = x
        # background for alternate rows
        if (data.index(row) % 2) == 0:
            c.setFillColor(colors.whitesmoke)
            c.rect(x, y_row, total_width, row_height, fill=1, stroke=0)
            c.setFillColor(colors.black)
        for i, cell in enumerate(row):
            c.drawString(cur_x + 2 * mm, y_row + 2 * mm, str(cell))
            cur_x += col_widths[i]


def generate_invoice_pdf(pedido, cliente=None, items=None, logo_path=None):
    """Genera un PDF de factura con mejor diseño y devuelve los bytes."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 15 * mm
    y = height - margin

    # Draw border
    c.setLineWidth(1)
    c.rect(margin / 2, margin / 2, width - margin, height - margin)

    # Logo
    try:
        if not logo_path:
            possible = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'FRONTEND', 'public', 'logo.png')
            possible = os.path.normpath(possible)
            if os.path.exists(possible):
                logo_path = possible

        if logo_path and os.path.exists(logo_path):
            c.drawImage(logo_path, margin, y - 20 * mm, width=40 * mm, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Header text
    c.setFont('Helvetica-Bold', 18)
    c.drawCentredString(width / 2, y - 10 * mm, 'FACTURA ELECTRÓNICA')
    y -= 30 * mm

    # Invoice metadata
    c.setFont('Helvetica', 10)
    fecha_str = getattr(pedido, 'fecha_pedido', None)
    if hasattr(fecha_str, 'strftime'):
        fecha_str = fecha_str.strftime('%Y-%m-%d %H:%M')
    elif not fecha_str:
        fecha_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    pedido_id = getattr(pedido, 'id_pedido', getattr(pedido, 'id', None)) or ''
    c.drawString(margin, y, f'Número: {pedido_id}')
    c.drawString(width - margin - 120, y, f'Fecha: {fecha_str}')
    y -= 8 * mm

    if cliente:
        nombre = getattr(cliente, 'nombre', None) or getattr(cliente, 'nombre_completo', '') or ''
        correo = getattr(cliente, 'correo', '')
        c.drawString(margin, y, f'Cliente: {nombre}')
        c.drawString(width - margin - 200, y, f'Email: {correo}')
        y -= 10 * mm

    # Items table
    if not items:
        items = []

    data = [['Cant', 'Descripción', 'Precio', 'Subtotal']]
    for it in items:
        cant = it.get('cantidad', '')
        desc = it.get('descripcion', '')
        subtotal = it.get('subtotal', '')
        # precio estimado
        precio = ''
        try:
            cantidad = float(it.get('cantidad', 0))
            subtotal_f = float(it.get('subtotal', 0))
            if cantidad:
                precio = f"{subtotal_f / cantidad:.2f}"
            else:
                precio = ''
        except Exception:
            precio = ''
        data.append([cant, desc, precio, f"{subtotal}"])

    table_x = margin
    table_y = y
    col_widths = [20 * mm, 100 * mm, 30 * mm, 30 * mm]
    _draw_table(c, table_x, table_y, col_widths, data, row_height=8 * mm)

    # Calculate totals
    total = getattr(pedido, 'total', 0) or 0
    # draw total box
    y_total = table_y - (len(data) * 8 * mm) - 10 * mm
    c.setFont('Helvetica-Bold', 12)
    c.drawRightString(width - margin - 10 * mm, y_total, f'Total: {total}')

    # QR (CUFE placeholder)
    try:
        qr_value = f'Pedido:{pedido_id}|Total:{total}|Fecha:{fecha_str}'
        qr = QrCodeWidget(qr_value)
        qr_size = 60 * mm
        bounds = qr.getBounds()
        width_qr = bounds[2] - bounds[0]
        height_qr = bounds[3] - bounds[1]
        d = qr
        render_x = margin
        render_y = y_total - qr_size - 10 * mm
        renderPDF.draw(d, c, render_x, render_y)
    except Exception:
        pass

    # Footer
    c.setFont('Helvetica', 8)
    c.drawString(margin, 15 * mm, 'Software JosniShop - Gracias por su compra')

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

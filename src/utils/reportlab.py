from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_report(invoice_data: dict, filename: str, invoice_type: str) -> None:
    """Genera un reporte PDF de una factura o nota de crédito."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(invoice_type, styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(f"Nro {invoice_type}: {invoice_data['number']}", styles["Normal"])
    )
    elements.append(Paragraph(f"Fecha: {invoice_data['date']}", styles["Normal"]))
    elements.append(
        Paragraph(f"Cliente: {invoice_data['user_name']}", styles["Normal"])
    )
    elements.append(Spacer(1, 12))

    table_data = [
        ["Producto", "Tipo de Producto", "Cantidad", "Precio Unitario", "Total"]
    ]
    for item in invoice_data["items"]:
        table_data.append(
            [
                item["name"],
                item["type"],
                str(item["quantity"]),
                f"${item['unit_price']:.2f}",
                f"${item['total']:.2f}",
            ]
        )

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(f"Subtotal: ${invoice_data['subtotal']:.2f}", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Descuento: -${invoice_data['discount']:.2f}", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Total: ${invoice_data['total']:.2f}", styles["Heading2"])
    )

    doc.build(elements)

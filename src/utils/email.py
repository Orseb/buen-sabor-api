import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from src.config.settings import settings

logger = logging.getLogger(__name__)


async def send_email_with_attachment(
    to_email: str,
    subject: str,
    body: str,
    attachment_data: bytes,
    attachment_filename: str,
    attachment_content_type: str = "application/pdf",
) -> bool:
    """Send an email with an attachment using SMTP."""
    try:
        message = MIMEMultipart()
        message["From"] = settings.from_email
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        attachment = MIMEApplication(attachment_data, _subtype="pdf")
        attachment.add_header(
            "Content-Disposition", f"attachment; filename={attachment_filename}"
        )
        message.attach(attachment)

        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_use_tls,
        )

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


async def send_invoice_email(
    customer_email: str,
    customer_name: str,
    invoice_number: str,
    pdf_data: bytes,
) -> bool:
    """Send an invoice email to a customer."""
    subject = f"Factura #{invoice_number} - El Buen Sabor"

    body = f"""Estimado/a {customer_name},

Adjunto encontrará su factura #{invoice_number} de El Buen Sabor.

Gracias por su compra.

Saludos cordiales,
El equipo de El Buen Sabor"""

    return await send_email_with_attachment(
        to_email=customer_email,
        subject=subject,
        body=body,
        attachment_data=pdf_data,
        attachment_filename=f"factura_{invoice_number}.pdf",
        attachment_content_type="application/pdf",
    )


async def send_credit_note_email(
    customer_email: str,
    customer_name: str,
    credit_note_number: str,
    pdf_data: bytes,
) -> bool:
    """Send a credit note email to a customer."""
    subject = f"Nota de Crédito #{credit_note_number} - El Buen Sabor"

    body = f"""Estimado/a {customer_name},

Adjunto encontrará su nota de crédito #{credit_note_number} de El Buen Sabor.

Esta nota de crédito ha sido generada para el reembolso correspondiente a su pedido.

Si tiene alguna consulta, no dude en contactarnos.

Saludos cordiales,
El equipo de El Buen Sabor"""

    return await send_email_with_attachment(
        to_email=customer_email,
        subject=subject,
        body=body,
        attachment_data=pdf_data,
        attachment_filename=f"nota_credito_{credit_note_number}.pdf",
        attachment_content_type="application/pdf",
    )

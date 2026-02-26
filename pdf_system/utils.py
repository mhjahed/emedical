# pdf_system/utils.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, legal, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
import re


def strip_html_tags(html_content):
    """Remove HTML tags and convert to plain text paragraphs"""
    if not html_content:
        return []
    
    # Simple HTML tag removal using regex
    import re
    
    # Remove script and style tags with content
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    paragraphs = []
    
    # Split by common block elements
    blocks = re.split(r'<(?:p|div|h[1-6]|li)[^>]*>', html_content)
    
    for block in blocks:
        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', '', block)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.strip()
        
        if text:
            paragraphs.append({
                'tag': 'p',
                'text': text
            })
    
    return paragraphs


def replace_placeholders(content, data):
    """Replace placeholders with actual data"""
    if not content:
        return content
    
    for key, value in data.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, str(value) if value else '')
    
    return content


def get_page_size(size_name, orientation):
    """Get page size based on name and orientation"""
    sizes = {
        'A4': A4,
        'Letter': letter,
        'Legal': legal,
    }
    size = sizes.get(size_name, A4)
    
    if orientation == 'landscape':
        return landscape(size)
    return size


def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    
    today = timezone.now().date()
    age = today.year - birth_date.year
    
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age


def generate_pdf_from_template(template, filled_data, patient=None, doctor=None):
    """Generate PDF from template with filled data"""
    try:
        # Prepare data with common placeholders
        data = {
            'date': timezone.now().strftime('%B %d, %Y'),
            'time': timezone.now().strftime('%I:%M %p'),
            'year': timezone.now().year,
        }
        
        if patient:
            data.update({
                'patient_name': patient.get_full_name(),
                'patient_email': patient.email,
                'patient_phone': patient.phone or 'N/A',
                'patient_age': calculate_age(patient.date_of_birth) if patient.date_of_birth else 'N/A',
                'patient_gender': patient.get_gender_display() if patient.gender else 'N/A',
                'patient_blood_group': patient.blood_group or 'N/A',
                'patient_address': patient.address or 'N/A',
            })
        
        if doctor:
            data.update({
                'doctor_name': f"Dr. {doctor.user.get_full_name()}",
                'doctor_designation': doctor.designation or '',
                'doctor_department': doctor.department.name if doctor.department else '',
                'doctor_qualification': doctor.qualifications or '',
                'medi_id': doctor.user.medi_id or '',
            })
        
        # Add filled data
        data.update(filled_data)
        
        # Create PDF buffer
        buffer = BytesIO()
        
        # Get page settings
        page_size = get_page_size(template.page_size, template.orientation)
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=page_size,
            topMargin=template.margin_top,
            bottomMargin=template.margin_bottom,
            leftMargin=template.margin_left,
            rightMargin=template.margin_right
        )
        
        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=1  # Center
        ))
        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        ))
        
        # Build story (content)
        story = []
        
        # Add logo if exists
        if template.logo:
            try:
                from reportlab.platypus import Image as RLImage
                logo = RLImage(template.logo.path, width=2*inch, height=1*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 20))
            except Exception as e:
                print(f"Error adding logo: {e}")
        
        # Process header content
        if template.header_content:
            header_text = replace_placeholders(template.header_content, data)
            header_paragraphs = strip_html_tags(header_text)
            for para in header_paragraphs:
                story.append(Paragraph(para['text'], styles['CustomTitle']))
        
        story.append(Spacer(1, 20))
        
        # Process body content
        body_text = replace_placeholders(template.body_content, data)
        body_paragraphs = strip_html_tags(body_text)
        
        for para in body_paragraphs:
            story.append(Paragraph(para['text'], styles['CustomBody']))
        
        story.append(Spacer(1, 30))
        
        # Process footer content
        if template.footer_content:
            footer_text = replace_placeholders(template.footer_content, data)
            footer_paragraphs = strip_html_tags(footer_text)
            for para in footer_paragraphs:
                story.append(Paragraph(para['text'], styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        buffer.seek(0)
        pdf_content = buffer.read()
        
        # Create file name
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{template.slug}_{timestamp}.pdf"
        
        return ContentFile(pdf_content, name=file_name)
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None
# doctors/utils.py

from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.conf import settings


def generate_barcode(medi_id):
    """Generate a barcode image for the given Medi ID"""
    try:
        # Generate Code128 barcode
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(medi_id, writer=ImageWriter())
        
        # Create buffer
        buffer = BytesIO()
        barcode_instance.write(buffer, options={
            'module_width': 0.6,
            'module_height': 40.0,
            'quiet_zone': 8.0,
            'font_size': 12,
            'text_distance': 4.0,
        })
        buffer.seek(0)
        
        return ContentFile(buffer.read(), name=f'barcode_{medi_id}.png')
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None


def generate_id_card(user, profile):
    """Generate a digital ID card for doctor/staff"""
    try:
        # Card dimensions (vertical)
        width, height = 400, 600
        
        # Create card image
        card = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(card)
        
        # Load fonts (use default if custom fonts not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            name_font = ImageFont.truetype("arial.ttf", 20)
            text_font = ImageFont.truetype("arial.ttf", 14)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Colors
        primary_color = (0, 123, 255)  # Blue
        text_color = (33, 37, 41)  # Dark gray
        light_gray = (108, 117, 125)
        
        # Header background
        draw.rectangle([(0, 0), (width, 100)], fill=primary_color)
        
        # Hospital name
        hospital_name = "MediCare Hospital"
        draw.text((width // 2, 30), hospital_name, fill='white', font=title_font, anchor='mm')
        draw.text((width // 2, 60), "Medical Staff ID Card", fill='white', font=text_font, anchor='mm')
        
        # Profile picture placeholder/actual
        photo_size = 120
        photo_x = (width - photo_size) // 2
        photo_y = 120
        
        if user.profile_picture:
            try:
                profile_img = Image.open(user.profile_picture.path)
                profile_img = profile_img.resize((photo_size, photo_size))
                # Create circular mask
                mask = Image.new('L', (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
                card.paste(profile_img, (photo_x, photo_y), mask)
            except:
                # Draw placeholder circle
                draw.ellipse([(photo_x, photo_y), (photo_x + photo_size, photo_y + photo_size)], 
                           fill=light_gray, outline=primary_color, width=3)
        else:
            # Draw placeholder circle
            draw.ellipse([(photo_x, photo_y), (photo_x + photo_size, photo_y + photo_size)], 
                        fill=light_gray, outline=primary_color, width=3)
        
        # Name
        name = f"Dr. {user.get_full_name()}" if user.role == 'doctor' else user.get_full_name()
        draw.text((width // 2, 260), name, fill=text_color, font=name_font, anchor='mm')
        
        # Designation
        if hasattr(profile, 'designation') and profile.designation:
            draw.text((width // 2, 290), profile.designation, fill=light_gray, font=text_font, anchor='mm')
        
        # Department
        if hasattr(profile, 'department') and profile.department:
            draw.text((width // 2, 320), profile.department.name, fill=light_gray, font=text_font, anchor='mm')
        
        # Details section
        y_pos = 360
        details = [
            ('Medi ID:', user.medi_id or 'N/A'),
            ('Blood Group:', user.blood_group or 'N/A'),
        ]
        
        for label, value in details:
            draw.text((50, y_pos), label, fill=light_gray, font=text_font)
            draw.text((150, y_pos), value, fill=text_color, font=text_font)
            y_pos += 30
        
        # Generate and paste barcode
        if user.medi_id:
            barcode_content = generate_barcode(user.medi_id)
            if barcode_content:
                barcode_img = Image.open(BytesIO(barcode_content.read()))
                barcode_img.thumbnail((320, 120), Image.Resampling.LANCZOS)
                barcode_x = (width - 200) // 2
                card.paste(barcode_img, (barcode_x, 470))
        
        # Footer
        draw.rectangle([(0, height - 40), (width, height)], fill=primary_color)
        draw.text((width // 2, height - 20), "Valid for Internal Use Only", 
                 fill='white', font=small_font, anchor='mm')
        
        # Save to buffer
        buffer = BytesIO()
        card.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        return ContentFile(buffer.read(), name=f'id_card_{user.medi_id}.png')
    
    except Exception as e:
        print(f"Error generating ID card: {e}")
        return None
    


from PIL import Image, ImageDraw, ImageFont
import os

def create_report_image():
    # Create a white canvas (A4 ratio approx)
    width, height = 2480, 3508
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Try to load a font, fallback to default
    try:
        # On macOS, Helvetica is usually available
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_reg = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        font_header = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
    except:
        font_bold = ImageFont.load_default()
        font_reg = ImageFont.load_default()
        font_header = ImageFont.load_default()

    # Padding and margins
    margin = 150
    y = 200

    # Header
    draw.text((width/2, y), "CITY DIAGNOSTIC CENTER & PATHOLOGY LAB", fill='black', font=font_header, anchor="mm")
    y += 120
    draw.text((width/2, y), "123 Medical Drive, Health City | Ph: +91-9988776655", fill='black', font=font_reg, anchor="mm")
    y += 100
    draw.line((margin, y, width-margin, y), fill='black', width=5)
    y += 150

    # Patient Info
    info = [
        ("PATIENT NAME:", "MR. KUSHAL DEVRAJ"),
        ("AGE / SEX  :", "24 Years / Male"),
        ("DATE       :", "2026-03-30"),
        ("REF. BY    :", "Dr. Self")
    ]
    for label, val in info:
        draw.text((margin, y), label, fill='black', font=font_bold)
        draw.text((margin + 600, y), val, fill='black', font=font_reg)
        y += 100

    y += 150
    draw.text((margin, y), "TEST: COMPLETE BLOOD COUNT (CBC)", fill='black', font=font_header)
    y += 150

    # Table Header
    draw.text((margin, y), "PARAMETER", fill='black', font=font_bold)
    draw.text((margin + 800, y), "RESULT", fill='black', font=font_bold)
    draw.text((margin + 1300, y), "UNITS", fill='black', font=font_bold)
    draw.text((margin + 1800, y), "REF. RANGE", fill='black', font=font_bold)
    y += 80
    draw.line((margin, y, width-margin, y), fill='black', width=3)
    y += 100

    # Results
    results = [
        ("WBC Count", "18.5 *", "10^3/uL", "4.0 - 11.0"),
        ("Neutrophils", "85 *", "%", "40 - 75"),
        ("Hemoglobin", "10.2 *", "g/dL", "13.0 - 17.0"),
        ("Platelet Count", "82 *", "10^3/uL", "150 - 450"),
        ("MCV", "78", "fL", "80 - 100")
    ]

    for p, r, u, ref in results:
        draw.text((margin, y), p, fill='black', font=font_reg)
        draw.text((margin + 800, y), r, fill='black', font=font_reg)
        draw.text((margin + 1300, y), u, fill='black', font=font_reg)
        draw.text((margin + 1800, y), ref, fill='black', font=font_reg)
        y += 120

    y += 200
    draw.text((margin, y), "IMPRESSION & CLINICAL CORRELATION:", fill='black', font=font_bold)
    y += 120
    msg = ("Marked Leukocytosis with Neutrophilia (Left Shift) noted. "
           "Thrombocytopenia present. Microcytic Anemia observed. "
           "Findings suggest an acute systemic infection. Clinical correlation recommended.")
    
    # Primitive wrapping
    words = msg.split()
    line = ""
    for word in words:
        if len(line + word) < 60:
            line += word + " "
        else:
            draw.text((margin + 50, y), line, fill='black', font=font_reg)
            y += 80
            line = word + " "
    draw.text((margin + 50, y), line, fill='black', font=font_reg)

    y += 400
    draw.text((width - margin - 600, y), "Dr. Pathologist", fill='black', font=font_bold)
    y += 80
    draw.text((width - margin - 600, y), "MBBS, MD", fill='black', font=font_reg)

    # Save
    out_path = "/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/Sample_Hematology_Report.jpg"
    image.save(out_path, quality=95)
    print(f"Report image saved at: {out_path}")

if __name__ == '__main__':
    create_report_image()

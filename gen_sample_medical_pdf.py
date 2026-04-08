from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_pdf():
    filename = "/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/Sample_Hematology_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 50, "CITY DIAGNOSTIC CENTER & PATHOLOGY LAB")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, "123 Medical Drive, Health City | Ph: +91-9988776655")
    c.line(50, height - 75, width - 50, height - 75)

    # Patient Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "PATIENT NAME: ")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 100, "MR. KUSHAL DEVRAJ")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 120, "AGE/SEX: ")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 120, "24 Years / Male")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 140, "DATE: ")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 140, "2026-03-30")

    # Body
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "TEST: COMPLETE BLOOD COUNT (CBC)")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 210, "PARAMETER")
    c.drawString(200, height - 210, "RESULT")
    c.drawString(300, height - 210, "UNITS")
    c.drawString(400, height - 210, "REFERENCE RANGE")
    c.line(50, height - 215, width - 50, height - 215)

    c.setFont("Helvetica", 11)
    y = height - 235
    data = [
        ("WBC Count", "18.5 *", "10^3/uL", "4.0 - 11.0"),
        ("Neutrophils", "85 *", "%", "40 - 75"),
        ("Hemoglobin", "10.2 *", "g/dL", "13.0 - 17.0"),
        ("Platelet Count", "82 *", "10^3/uL", "150 - 450"),
        ("MCV", "78", "fL", "80 - 100")
    ]
    
    for p, r, u, ref in data:
        c.drawString(50, y, p)
        c.drawString(200, y, r)
        c.drawString(300, y, u)
        c.drawString(400, y, ref)
        y -= 25

    # Impression
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 20, "IMPRESSION & CLINICAL CORRELATION:")
    c.setFont("Helvetica", 11)
    msg = ("Marked Leukocytosis with Neutrophilia (Left Shift) noted. "
           "Thrombocytopenia present. Microcytic Anemia observed. "
           "Suggestive of acute systemic infection.")
    
    # Simple line wrapping
    c.drawString(50, y - 40, msg[:70])
    c.drawString(50, y - 55, msg[70:])

    # Signature
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(width - 150, 50, "Dr. Pathologist, MBBS, MD")
    
    c.save()
    print(f"Created {filename}")

if __name__ == '__main__':
    create_sample_pdf()

import pdfplumber
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# pdfmetrics.registerFont(TTFont('GreatVibes', '/Users/prajwal_b/Documents/Great_Vibes/GreatVibes-Regular.ttf'))

def generate_certificate(output_path, uid, candidate_name, course_name, org_name, institute_logo_path):
    # Set up PDF in landscape mode
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=landscape(letter))

    background_image = ImageReader("../application/utils/certificate_background.jpg")
    # Add background image
    if background_image:
        c.drawImage(background_image, 0, 0, width=width, height=height)
    
    # Add institute logo if provided
    if institute_logo_path:
        logo = ImageReader(institute_logo_path)
        c.drawImage(logo, 350, height - 160, width=80, height=80)  # Top-left corner
    
    # Define styles (fonts, sizes, colors)
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(HexColor("#000000"))  # Black color for title
    # Add Title
    c.drawCentredString(width / 2, height - 200, "CERTIFICATE OF ACHIEVEMENT")
    
    # Add Organization Name
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(width / 2, height - 230, f"Presented by")
    
    # Add UID
    c.setFont("Helvetica", 18)
    c.setFillColor(HexColor("#e6401c"))  # Blue color
    c.drawCentredString(width / 2, height - 250, f"{org_name}")
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(width / 2, height - 270, f"To")

    # Add Recipient Name
    c.setFont("Helvetica", 28)
    c.setFillColor(HexColor("#0B6ABF"))  # Blue color
    c.drawCentredString(width / 2, height - 300, candidate_name)
    
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#444444"))
    c.drawCentredString(width / 2, height - 320, f" with Student ID:")
    c.setFont("Helvetica", 16)
    c.setFillColor(HexColor("#0B6ABF"))  # Blue color
    c.drawCentredString(width / 2, height - 340, f" {uid}")

    # Add Course Name
    c.setFont("Helvetica-Bold",16 )
    c.setFillColor(HexColor("#000000")) 
    c.drawCentredString(width / 2, height - 370, f"For successfully completing the course")
    c.drawCentredString(width / 2, height - 390, f"On")
    c.setFont("Helvetica-Bold",20 )
    c.setFillColor(HexColor("#F97316"))  # Orange color
    c.drawCentredString(width / 2, height - 410, f" {course_name}")
    
    # Footer Text
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(width / 2, 100, "Thank you for your hard work and dedication.")
    
    # Save the PDF
    c.save()
    print(f"Certificate generated and saved at: {output_path}")

def extract_certificate(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from each page
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        # Use regex patterns to find the required information
        uid_pattern = r"Student ID:\s*(\S+)"
        name_pattern = r"To\s*([^\n]+)"
        course_pattern = r"On\s*([^\n]+)"
        org_pattern = r"Presented by\s*([^\n]+)"
        
        # Extract information using patterns
        uid_match = re.search(uid_pattern, text)
        name_match = re.search(name_pattern, text)
        course_match = re.search(course_pattern, text)
        org_match = re.search(org_pattern, text)
        
        if not all([uid_match, name_match, course_match, org_match]):
            raise ValueError("Could not extract all required information from the certificate")
        
        uid = uid_match.group(1).strip()
        candidate_name = name_match.group(1).strip()
        course_name = course_match.group(1).strip()
        org_name = org_match.group(1).strip()
        
        print("Extracted Data:", uid, candidate_name, course_name, org_name)
        return (uid, candidate_name, course_name, org_name)


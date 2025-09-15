#!/usr/bin/env python3

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
from reportlab.lib.colors import blue

# PDF output file
pdf_file = "090-source-page.pdf"

# Define links as a list of tuples (label, url)
links = [
    ("GitHub", "https://github.com/milahu/andre-schmitt-wenn-die-krise-kommt-2025"),
    ("DarkForest.onion", "http://git.dkforestseeaaq2dqz2uflmlsybvnq2irzn4ygyvu53oazyorednviid.onion/milahu/andre-schmitt-wenn-die-krise-kommt-2025"),
    ("DarkTea.onion", "http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/milahu/andre-schmitt-wenn-die-krise-kommt-2025"),
    ("RightToPrivacy.onion", "http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/milahu/andre-schmitt-wenn-die-krise-kommt-2025"),
    ("MyGully", "https://mygully.com/showthread.php?t=8362623"),
    ("MyBoerse", "https://myboerse.bz/threads/2637945"),
]

# Create PDF document with A4 size
doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                        rightMargin=20*mm, leftMargin=20*mm,
                        topMargin=20*mm, bottomMargin=20*mm)

# Styles
styles = getSampleStyleSheet()
monospace_style = ParagraphStyle(
    'Monospace',
    parent=styles['Normal'],
    fontName='Courier',  # Monospace font
    fontSize=11,
    leading=14,
    # textColor=blue
)

elements = []

# Title
elements.append(Paragraph("Quellen", styles['Heading2']))
elements.append(Spacer(1, 5*mm))

# Add links
for label, url in links:
    # link_paragraph = f"<b>{label}:</b> <a href='{url}' color='blue'>{url}</a>"
    # link_paragraph = f"{label}<br/><a href='{url}' color='blue'>{url}</a>"
    link_paragraph = f"{label}<br/><a href='{url}'>{url}</a>"
    elements.append(Paragraph(link_paragraph, monospace_style))
    elements.append(Spacer(1, 3*mm))

# Build PDF
doc.build(elements)

print(f"PDF generated: {pdf_file}")

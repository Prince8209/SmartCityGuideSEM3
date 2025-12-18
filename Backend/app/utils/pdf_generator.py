"""
PDF Generator Utility for Booking Confirmations
Uses ReportLab to generate professional booking confirmation PDFs
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class BookingPDFGenerator:
    """Generate booking confirmation PDFs"""
    
    def __init__(self, output_dir='bookings'):
        """Initialize PDF generator with output directory"""
        self.output_dir = output_dir
        # Create bookings directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_booking_pdf(self, booking_data):
        """
        Generate a booking confirmation PDF
        
        Args:
            booking_data (dict): Dictionary containing booking information
                - booking_reference: Unique booking reference
                - customer_name: Customer's full name
                - customer_email: Customer's email
                - customer_phone: Customer's phone number
                - city_name: Name of the city
                - check_in_date: Check-in date
                - check_out_date: Check-out date
                - num_travelers: Number of travelers
                - daily_budget: Daily budget per person
                - total_cost: Total cost of the trip
                - special_requests: Optional special requests
                - created_at: Booking creation timestamp
        
        Returns:
            str: Path to the generated PDF file
        """
        # Generate filename
        filename = f"{booking_data['booking_reference']}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        normal_style = styles['Normal']
        
        # Add title
        title = Paragraph("BOOKING CONFIRMATION", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Add booking reference and date
        ref_data = [
            ['Booking Reference:', booking_data['booking_reference']],
            ['Booking Date:', datetime.fromisoformat(booking_data['created_at']).strftime('%B %d, %Y at %I:%M %p')]
        ]
        ref_table = Table(ref_data, colWidths=[2*inch, 4*inch])
        ref_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(ref_table)
        elements.append(Spacer(1, 20))
        
        # Customer Information Section
        elements.append(Paragraph("Customer Information", heading_style))
        customer_data = [
            ['Name:', booking_data['customer_name']],
            ['Email:', booking_data['customer_email']],
            ['Phone:', booking_data['customer_phone']]
        ]
        customer_table = Table(customer_data, colWidths=[1.5*inch, 4.5*inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(customer_table)
        elements.append(Spacer(1, 20))
        
        # Trip Details Section
        elements.append(Paragraph("Trip Details", heading_style))
        
        # Calculate number of days
        check_in = datetime.fromisoformat(booking_data['check_in_date'])
        check_out = datetime.fromisoformat(booking_data['check_out_date'])
        num_days = (check_out - check_in).days
        
        trip_data = [
            ['Destination:', booking_data['city_name']],
            ['Check-in Date:', check_in.strftime('%B %d, %Y')],
            ['Check-out Date:', check_out.strftime('%B %d, %Y')],
            ['Duration:', f'{num_days} days'],
            ['Number of Travelers:', str(booking_data['num_travelers'])]
        ]
        
        if booking_data.get('special_requests'):
            trip_data.append(['Special Requests:', booking_data['special_requests']])
        
        trip_table = Table(trip_data, colWidths=[1.5*inch, 4.5*inch])
        trip_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(trip_table)
        elements.append(Spacer(1, 20))
        
        # Budget Breakdown Section
        elements.append(Paragraph("Budget Breakdown", heading_style))
        
        budget_data = [
            ['Description', 'Amount'],
            ['Daily Budget (per person)', f'₹{booking_data["daily_budget"]:,}'],
            ['Number of Days', str(num_days)],
            ['Number of Travelers', str(booking_data['num_travelers'])],
            ['', ''],
            ['Total Estimated Cost', f'₹{booking_data["total_cost"]:,}']
        ]
        
        budget_table = Table(budget_data, colWidths=[4*inch, 2*inch])
        budget_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#4a5568')),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f7fafc')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (1, -1), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            
            # Grid
            ('GRID', (0, 0), (-1, -2), 1, colors.HexColor('#e2e8f0')),
            ('BOX', (0, -1), (-1, -1), 2, colors.HexColor('#667eea')),
        ]))
        elements.append(budget_table)
        elements.append(Spacer(1, 30))
        
        # Terms and Conditions
        elements.append(Paragraph("Important Information", heading_style))
        terms_text = """
        <para fontSize=9 textColor=#718096>
        • This is a booking confirmation for your trip to {city}.<br/>
        • Please carry a valid ID proof during your travel.<br/>
        • The estimated cost is based on the daily budget and may vary based on actual expenses.<br/>
        • For any queries or modifications, please contact us with your booking reference.<br/>
        • Cancellation policy: Free cancellation up to 48 hours before check-in.<br/>
        • We wish you a wonderful trip!
        </para>
        """.format(city=booking_data['city_name'])
        elements.append(Paragraph(terms_text, normal_style))
        elements.append(Spacer(1, 30))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#718096'),
            alignment=TA_CENTER
        )
        footer_text = """
        <para>
        Thank you for choosing Smart City Guide!<br/>
        For support, contact us at pp8995982@gmail.com or +91 7069300609
        </para>
        """
        elements.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(elements)
        
        return filepath


# Convenience function
def generate_booking_pdf(booking_data, output_dir='bookings'):
    """
    Generate a booking confirmation PDF
    
    Args:
        booking_data (dict): Booking information
        output_dir (str): Directory to save PDFs
    
    Returns:
        str: Path to generated PDF
    """
    generator = BookingPDFGenerator(output_dir)
    return generator.generate_booking_pdf(booking_data)

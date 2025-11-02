"""
Email Notification Service
Supports multiple email providers: SMTP, SendGrid, and Twilio SendGrid
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict
from jinja2 import Template


class EmailService:
    """Professional email notification service."""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.from_name = os.getenv("FROM_NAME", "SkinVision AI")
        
        # SendGrid settings (alternative to SMTP)
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY", "")
        self.use_sendgrid = bool(self.sendgrid_api_key)
    
    def send_email_smtp(self, to_email: str, subject: str, html_content: str, text_content: str = "") -> bool:
        """Send email using SMTP."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"SMTP email error: {e}")
            return False
    
    def send_email_sendgrid(self, to_email: str, subject: str, html_content: str, text_content: str = "") -> bool:
        """Send email using SendGrid API."""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            return response.status_code in [200, 201, 202]
        except ImportError:
            print("SendGrid not installed. Install with: pip install sendgrid")
            return False
        except Exception as e:
            print(f"SendGrid email error: {e}")
            return False
    
    def send_notification(self, to_email: str, prediction_data: Dict, user_name: Optional[str] = None) -> bool:
        """
        Send diagnosis completion notification email.
        
        Args:
            to_email: Recipient email address
            prediction_data: Dictionary with prediction details
            user_name: Optional user name for personalization
        """
        if not to_email:
            return False
        
        # Generate email content
        subject = f"Your Skin Analysis Results - {prediction_data.get('predicted_class', 'Diagnosis Complete')}"
        html_content = self._generate_email_template(prediction_data, user_name)
        text_content = self._generate_text_email(prediction_data, user_name)
        
        # Choose email service
        if self.use_sendgrid:
            return self.send_email_sendgrid(to_email, subject, html_content, text_content)
        elif self.smtp_user and self.smtp_password:
            return self.send_email_smtp(to_email, subject, html_content, text_content)
        else:
            print("Email service not configured. Set SMTP_USER/SMTP_PASSWORD or SENDGRID_API_KEY")
            return False
    
    def _generate_email_template(self, prediction_data: Dict, user_name: Optional[str] = None) -> str:
        """Generate HTML email template."""
        disease = prediction_data.get('predicted_class', 'Unknown')
        confidence = prediction_data.get('confidence', 0.0)
        confidence_pct = int(confidence * 100)
        
        # Determine urgency
        if confidence >= 0.8:
            urgency = "High"
            urgency_color = "#EF4444"
            advice = "Consult a dermatologist within 3-7 days. This requires immediate medical attention."
        elif confidence >= 0.5:
            urgency = "Medium"
            urgency_color = "#F59E0B"
            advice = "Book an appointment within 2-4 weeks for professional evaluation."
        else:
            urgency = "Low"
            urgency_color = "#10B981"
            advice = "Monitor the area and consider rechecking in 8-12 weeks if changes occur."
        
        greeting = f"Hello {user_name}," if user_name else "Hello,"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #17252A; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2B7A78, #3AAFA9); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #DEF2F1; }}
                .result-box {{ background: #DEF2F1; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .confidence-bar {{ background: #DEF2F1; height: 30px; border-radius: 15px; overflow: hidden; margin: 10px 0; }}
                .confidence-fill {{ background: linear-gradient(90deg, #2B7A78, #3AAFA9); height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }}
                .urgency-badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; color: white; font-weight: bold; background: {urgency_color}; }}
                .footer {{ background: #17252A; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
                .button {{ display: inline-block; background: #2B7A78; color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧬 SkinVision AI</h1>
                    <p>Your Analysis Results</p>
                </div>
                <div class="content">
                    <p>{greeting}</p>
                    <p>Your skin image analysis has been completed. Here are your results:</p>
                    
                    <div class="result-box">
                        <h2 style="color: #2B7A78; margin-top: 0;">Predicted Condition</h2>
                        <h3 style="font-size: 24px; margin: 10px 0;">{disease}</h3>
                        
                        <div>
                            <strong>Confidence: {confidence_pct}%</strong>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {confidence_pct}%;">{confidence_pct}%</div>
                            </div>
                        </div>
                        
                        <div style="margin-top: 20px;">
                            <strong>Urgency Level:</strong><br>
                            <span class="urgency-badge">{urgency}</span>
                        </div>
                        
                        <div style="margin-top: 20px; padding: 15px; background: white; border-left: 4px solid {urgency_color};">
                            <strong>Recommendation:</strong><br>
                            {advice}
                        </div>
                    </div>
                    
                    <p><strong>Important:</strong> This analysis is for informational purposes only and does not replace professional medical advice. Please consult with a qualified dermatologist for diagnosis and treatment.</p>
                    
                    <div style="text-align: center;">
                        <a href="http://localhost:3000/result" class="button">View Full Report</a>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>SkinVision AI</strong> - Powered by Deep Learning Technology</p>
                    <p>This is an automated notification. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_text_email(self, prediction_data: Dict, user_name: Optional[str] = None) -> str:
        """Generate plain text email version."""
        disease = prediction_data.get('predicted_class', 'Unknown')
        confidence = prediction_data.get('confidence', 0.0)
        confidence_pct = int(confidence * 100)
        
        text = f"""
SkinVision AI - Your Analysis Results

{greeting if user_name else 'Hello'},

Your skin image analysis has been completed.

Predicted Condition: {disease}
Confidence: {confidence_pct}%

Important: This analysis is for informational purposes only and does not replace professional medical advice. Please consult with a qualified dermatologist.

View full report: http://localhost:3000/result

---
SkinVision AI - Powered by Deep Learning Technology
        """
        return text.strip()


# Singleton instance
email_service = EmailService()

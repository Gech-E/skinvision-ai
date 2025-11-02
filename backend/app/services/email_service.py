"""
Email Notification Service
Handles sending email notifications for diagnosis completion.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from jinja2 import Template


class EmailService:
    """Service for sending email notifications."""
    
    def __init__(self):
        # SMTP Configuration from environment variables
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.from_email = os.environ.get("FROM_EMAIL", self.smtp_user)
        self.enabled = os.environ.get("EMAIL_NOTIFICATIONS_ENABLED", "false").lower() == "true"
        
    def _get_connection(self):
        """Create SMTP connection."""
        if not self.enabled or not self.smtp_user:
            return None
        
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        return server
    
    def send_diagnosis_notification(
        self,
        to_email: str,
        patient_name: Optional[str] = None,
        predicted_class: str = "Unknown",
        confidence: float = 0.0,
        urgency_level: str = "Low",
        report_url: Optional[str] = None
    ) -> bool:
        """
        Send diagnosis completion notification email.
        
        Args:
            to_email: Recipient email address
            patient_name: Patient name (optional)
            predicted_class: Predicted disease class
            confidence: Confidence score (0-1)
            urgency_level: Urgency level (High/Medium/Low)
            report_url: URL to download report (optional)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print("Email notifications are disabled")
            return False
        
        if not to_email:
            print("No email address provided")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Your SkinVision AI Diagnosis Results - {predicted_class}"
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Email template
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #17252A; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #2B7A78, #3AAFA9); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .result-box { background: #DEF2F1; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2B7A78; }
                    .confidence-bar { background: #e0e0e0; height: 25px; border-radius: 12px; overflow: hidden; margin: 10px 0; }
                    .confidence-fill { background: linear-gradient(90deg, #2B7A78, #3AAFA9); height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
                    .urgency-high { color: #EF4444; font-weight: bold; }
                    .urgency-medium { color: #F59E0B; font-weight: bold; }
                    .urgency-low { color: #10B981; font-weight: bold; }
                    .button { display: inline-block; padding: 12px 24px; background: #2B7A78; color: white; text-decoration: none; border-radius: 6px; margin: 10px 0; }
                    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 12px; }
                    .disclaimer { background: #fff3cd; padding: 15px; border-radius: 6px; margin: 20px 0; border-left: 4px solid #ffc107; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🧬 SkinVision AI</h1>
                        <p>Your Diagnosis Results</p>
                    </div>
                    <div class="content">
                        <p>Hello{% if patient_name %} {{ patient_name }}{% endif %},</p>
                        <p>Your skin image analysis has been completed. Here are your results:</p>
                        
                        <div class="result-box">
                            <h3 style="margin-top: 0;">Diagnosis Result</h3>
                            <p style="font-size: 24px; font-weight: bold; color: #2B7A78; margin: 10px 0;">
                                {{ predicted_class }}
                            </p>
                            <p><strong>Confidence Score:</strong> {{ confidence_percent }}%</p>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {{ confidence_percent }}%;">
                                    {{ confidence_percent }}%
                                </div>
                            </div>
                            <p><strong>Urgency Level:</strong> 
                                <span class="urgency-{{ urgency_level.lower() }}">{{ urgency_level }}</span>
                            </p>
                        </div>
                        
                        {% if urgency_level == "High" %}
                        <div class="disclaimer">
                            <strong>⚠️ Important:</strong> Based on the analysis, we recommend consulting a dermatologist within 3–7 days. This requires professional medical attention.
                        </div>
                        {% elif urgency_level == "Medium" %}
                        <div class="disclaimer">
                            <strong>📋 Recommendation:</strong> Please book an appointment with a dermatologist within 2–4 weeks for professional evaluation.
                        </div>
                        {% else %}
                        <div class="disclaimer">
                            <strong>✅ Advice:</strong> Monitor the area and consider rechecking in 8–12 weeks if any changes occur.
                        </div>
                        {% endif %}
                        
                        {% if report_url %}
                        <p style="text-align: center;">
                            <a href="{{ report_url }}" class="button">📄 Download Full Report</a>
                        </p>
                        {% endif %}
                        
                        <p>You can view your complete analysis results and heatmap visualization by logging into your SkinVision AI account.</p>
                        
                        <div class="footer">
                            <p><strong>⚠️ Medical Disclaimer:</strong></p>
                            <p>This analysis is for informational purposes only and does not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers.</p>
                            <p style="margin-top: 20px;">
                                © SkinVision AI - Powered by Deep Learning Technology
                            </p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_template = """
            SkinVision AI - Diagnosis Results
            
            Hello{% if patient_name %} {{ patient_name }}{% endif %},
            
            Your skin image analysis has been completed.
            
            Diagnosis Result: {{ predicted_class }}
            Confidence Score: {{ confidence_percent }}%
            Urgency Level: {{ urgency_level }}
            
            {% if urgency_level == "High" %}
            IMPORTANT: Please consult a dermatologist within 3-7 days.
            {% elif urgency_level == "Medium" %}
            Recommendation: Book an appointment within 2-4 weeks.
            {% else %}
            Advice: Monitor the area and recheck in 8-12 weeks if changes occur.
            {% endif %}
            
            {% if report_url %}
            Download full report: {{ report_url }}
            {% endif %}
            
            DISCLAIMER: This analysis is for informational purposes only and does not replace professional medical advice.
            
            © SkinVision AI
            """
            
            # Render templates
            html_body = Template(html_template).render(
                patient_name=patient_name or "",
                predicted_class=predicted_class,
                confidence_percent=round(confidence * 100, 1),
                urgency_level=urgency_level,
                report_url=report_url or ""
            )
            
            text_body = Template(text_template).render(
                patient_name=patient_name or "",
                predicted_class=predicted_class,
                confidence_percent=round(confidence * 100, 1),
                urgency_level=urgency_level,
                report_url=report_url or ""
            )
            
            # Attach parts
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = self._get_connection()
            if server:
                server.send_message(msg)
                server.quit()
                print(f"Email notification sent to {to_email}")
                return True
            else:
                print("Email service not configured or disabled")
                return False
                
        except Exception as e:
            print(f"Failed to send email notification: {e}")
            return False


# Global instance
email_service = EmailService()

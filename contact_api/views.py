from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract form data
            full_name = data.get('fullName', '')
            email = data.get('email', '')
            phone = f"{data.get('countryCode', '')} {data.get('phoneNumber', '')}"
            company = data.get('companyName', 'Not specified')
            state = data.get('state', 'Not specified')
            service = data.get('serviceType', 'Not specified')
            budget = data.get('budget', 'Not specified')
            timeline = data.get('timeline', 'Not specified')
            description = data.get('projectDescription', '')

            # Compose email
            subject = f"New Contact Form Submission from {full_name}"
            message = f"""
Name: {full_name}
Email: {email}
Phone: {phone}
Company: {company}
State: {state}
Service: {service}
Budget: {budget}
Timeline: {timeline}

Project Description:
{description}
            """.strip()

            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['samuel@stagefx.us'],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})

        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send message. Please try again later.'},
                                status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def schedule_call(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract form data
            name = data.get('name', '')
            email = data.get('email', '')
            phone = data.get('phone', 'Not provided')
            date = data.get('date', '')
            time = data.get('time', '')
            timezone = data.get('timezone', '')
            service = data.get('service', '')

            # Compose email
            subject = f"New Call Scheduled: {name} - {date} at {time}"
            message = f"""
Name: {name}
Email: {email}
Date: {date}
Phone: {phone}
Time: {time} ({timezone})
Service: {service}

A new call has been scheduled. Please add it to your calendar.
            """.strip()

            # Send email to admin (always try this first)
            admin_sent = False
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['samuel@stagefx.us'],
                    fail_silently=False,
                )
                admin_sent = True
            except Exception as e:
                logger.error(f"Error sending admin email: {str(e)}")

            # Send confirmation email to user
            user_sent = False
            user_message = ""
            try:
                user_subject = f"Your Call with StageFX is Scheduled for {date} at {time}"
                user_message = f"""
Hi {name},

Thank you for scheduling a call with StageFX. Here are your call details:

Date: {date}
Time: {time} ({timezone})
Service: {service}

We're looking forward to discussing your project with you!

Best regards,
The StageFX Team
                """.strip()

                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                user_sent = True
            except Exception as e:
                logger.error(f"Error sending user email: {str(e)}")
                user_message = f"Your call has been scheduled, but we couldn't send a confirmation email to {email}. Please save these details:"

            if admin_sent:
                if user_sent:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Call scheduled successfully! A confirmation has been sent to your email.'
                    })
                else:
                    return JsonResponse({
                        'status': 'success',
                        'message': user_message + f"\n\nDate: {date}\nTime: {time} ({timezone})\nService: {service}"
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'We received your request but encountered an issue. Please contact us directly at samuel@stagefx.us to confirm your call.'
                }, status=500)

        except Exception as e:
            logger.error(f"Error in schedule_call: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while processing your request. Please try again later.'
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
from celery_worker import celery
from flask import current_app as app,render_template, request, Response, jsonify
import time
from models import Venue, User, bookedTicket
import csv
import io
from sqlalchemy import not_
import datetime 
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery.schedules import crontab
from sqlalchemy import desc
import pdfkit
from email.mime.base import MIMEBase
from email import encoders

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        10.0, 
        send_monthly_reports.s(), 
        name='Reminder every 10 seconds.'
    )
    sender.add_periodic_task(    
        10.0, 
        daily_notification.s(), 
        name='Reminder of daily notification.'
    )
    # sender.add_periodic_task(
    #     # crontab(hour=8,day_of_month=1),
    #     crontab(minute=48, hour=7, day_of_month='*'),
    #     send_monthly_reports.s(),
    #     name = 'Monthly engagement report every first day of month.'
    # )

    # sender.add_periodic_task(
    #     crontab(hour=20),
    #     # crontab(minute=53, hour=14, day_of_month='*'),
    #     daily_notification.s(),
    #     name = 'Daily engagement report sent at 8PM.'
    # )

# @celery.task()
# def add_together(a, b):
#     time.sleep(5)
    
#     return a + b


@celery.task()
def exportCSV(id):
    with app.app_context():
        venue = Venue.query.get(id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        time.sleep(5)
        venue_data = {
                    'id': venue.id,
                    'name': venue.name,
                    'address': venue.address,
                    'city': venue.city,
                    'state': venue.state,
                    'avg_venuerate':venue.avg_venuerate,
                    
                    'shows': [
                        {
                            'id': show.id,
                            'name': show.name,
                            'tag': show.tag,
                            'start_date': show.start_date, 
                            'out_date': show.out_date,  
                            'duration': str(show.duration),
                            'caption': show.caption,
                            'price': show.price,
                            'capacity': show.capacity,
                        }
                        for show in venue.venue_shows 
                    ]
                }

        csv_string = io.StringIO()
        csv_writer = csv.writer(csv_string)

        csv_writer.writerow([ 'Venue Name', 'Address', 'City', 'State', 'Average Venue Rate'])
        csv_writer.writerow([
            
            venue_data['name'],
            venue_data['address'],
            venue_data['city'],
            venue_data['state'],
            venue_data['avg_venuerate']
        ])

        csv_writer.writerow(['Show ID', 'Show Name', 'Tag', 'Start Date', 'Out Date', 'Duration', 'Caption', 'Price', 'Capacity'])
        for show in venue_data['shows']:
            csv_writer.writerow([
                show['id'],
                show['name'],
                show['tag'],
                show['start_date'],
                show['out_date'],
                show['duration'],
                show['caption'],
                show['price'],
                show['capacity'],
            ])
        return csv_string.getvalue()
    

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "abhishek@gmail.com"
SENDER_PASSWORD = ""

@celery.task
def sendMonthlyReport():
    with app.app_context():
        users = User.query.filter(not_(User.id == 1)).all()
        for user in users:
            bookings = bookedTicket.query.filter_by(user_email=user.email).all()
            month = datetime.today().strftime('%B-%Y')
            email_body = render_template('monthly_mail_temp.html', user=user, bookings=bookings, month=month)

            msg = MIMEMultipart()
            msg["From"] = SENDER_ADDRESS
            msg["To"] = user.email
            msg['Subject'] = "Monthly Engagement Report " + month
            msg.attach(MIMEText(email_body, 'html'))

            # PDF Attachment
            html = render_template('monthly_engagement_PDF.html', bookings=bookings, user=user)
            config = pdfkit.configuration(wkhtmltopdf='/mnt/c/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
            pdfkit.from_string(html, False, configuration=config)
            pdf_data = pdfkit.from_string(html, False)
            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdf_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{user.id}.pdf"')
            msg.attach(part)

            # Sending Email
            try:
                with smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT) as s:
                    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
                    s.send_message(msg)
                print(f"Engagement report sent successfully to {user.email}")
            except Exception as e:
                print(f"Error sending report to {user.email}: {e}")

    return "Engagement reports sent successfully."


from datetime import datetime, timedelta

@celery.task
def senddailyNotification():
    users = User.query.filter(not_(User.id == 1)).all()
    
    for user in users:
        last_booking = bookedTicket.query.filter_by(user_email=user.email).order_by(desc(bookedTicket.booked_date)).first()
        if last_booking:
            last_booked_date = last_booking.booked_date
            if last_booked_date < datetime.now() - timedelta(days=3):
                send_reminder_email(user)
        else:
            send_reminder_email(user)
    return 'Daily notification send.'

def send_reminder_email(user):
    email_body = render_template('daily_mail_temp.html', user=user)

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = user.email
            
    msg['Subject'] = "Reminder: Book Your Tickets Today!"
    msg.attach(MIMEText(email_body, 'html'))
    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()



@celery.task
def send_monthly_reports():
    sendMonthlyReport.delay()

@celery.task
def daily_notification():
    senddailyNotification.delay()



    
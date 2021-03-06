from django.core import mail
from django.test import TestCase
from django_mailer import queue_email_message


class FakeConnection(object):
    """
    A fake SMTP connection which diverts emails to the test buffer rather than
    sending.
    
    """
    def sendmail(self, *args, **kwargs):
        """
        Divert an email to the test buffer.
        
        """
        #FUTURE: the EmailMessage attributes could be found by introspecting
        # the encoded message.
        message = mail.EmailMessage('SUBJECT', 'BODY', 'FROM', ['TO'])
        mail.outbox.append(message)


class MailerTestCase(TestCase):
    """
    A base class for Django Mailer test cases which diverts emails to the test
    buffer and provides some helper methods.
    
    """
    def setUp(self):
        connection = mail.SMTPConnection
        if hasattr(connection, 'connection'):
            connection.pretest_connection = connection.connection
        connection.connection = FakeConnection()

    def tearDown(self):
        connection = mail.SMTPConnection
        if hasattr(connection, 'pretest_connection'):
            connection.connection = connection.pretest_connection

    def queue_message(self, subject='test', message='a test message',
                      from_email='sender@djangomailer',
                      recipient_list=['recipient@djangomailer'],
                      priority=None):
        email_message = mail.EmailMessage(subject, message, from_email,
                                          recipient_list)
        return queue_email_message(email_message, priority=priority)

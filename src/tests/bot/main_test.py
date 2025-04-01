import base64

from bot.main import make_email_message


def test_make_email_message():
    from_ = 'from@example.com'
    to = 'to@example.com'
    subject = 'Test email'

    message = make_email_message(from_, to, subject)

    assert message['raw'] == base64.urlsafe_b64encode(
        f'From: {from_}\nTo: {to}\nSubject: {subject}'.encode('utf-8')
    ).decode('utf-8')

import imaplib
import email
from email.header import decode_header

# E-posta hesabı bilgileriniz
EMAIL_USER = 'sizin mail@gmail.com'
EMAIL_PASS = 'email anahtarınız'
IMAP_SERVER = 'imap.gmail.com' # imap sağlayıcısı sadece google üzerinde test edildi 

def check_email_for_payment(description):
    # IMAP sunucusuna bağlanın
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select('inbox')

    # Gelen kutusunu kontrol edin
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # E-posta başlıklarını al
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        from_ = msg.get("From")

        # Papara'dan gelen e-postaları kontrol et
        if "Papara <bilgi@papara.com>" in from_ and ("Hesabına" in subject or "hesabında" in subject.lower()):
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        if description in body:
                            return True
            else:
                body = msg.get_payload(decode=True).decode()
                if description in body:
                    return True

    return False

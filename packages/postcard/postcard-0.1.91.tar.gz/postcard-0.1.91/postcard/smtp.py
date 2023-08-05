# -*- coding: utf-8 -*-
# @author: leesoar

"""SMTP client"""
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from postcard import setting

__all__ = ["Smtp"]


class Smtp(object):
    def __init__(self, debug=False):
        self.user = None
        self.pwd = None
        self._client = None
        self.smtp_addr = None
        self.smtp_port = None
        self.nickname = self.user
        self._debug = debug

    def login(self, user, pwd, smtp_addr=None, smtp_port=None, ssl=False):
        """Login current mailbox"""
        self.user = user
        self.pwd = pwd
        self.smtp_addr = smtp_addr or self.smtp_addr
        self.smtp_port = smtp_port or self.smtp_port

        if not self.smtp_addr:
            self.smtp_addr = self._set_smtp_addr_auto(user)

        if not self.smtp_port:
            self.smtp_port = 995 if ssl else 110

        if ssl:
            self._client = smtplib.SMTP_SSL(self.smtp_addr, self.smtp_port)
        else:
            self._client = smtplib.SMTP(self.smtp_addr, self.smtp_port)
        self._client.login(self.user, self.pwd)
        return self._client

    def close(self):
        self._client.quit()

    def set_nickname(self, nickname):
        self.nickname = nickname

    @staticmethod
    def get_addr_map():
        return setting.SMTP_ADDR

    def _set_smtp_addr_auto(self, user):
        domain = user.rsplit(".", maxsplit=1)[0].split("@")[-1]
        smtp_addr = self.get_addr_map().get(domain)
        if smtp_addr and not self.smtp_addr:
            self.smtp_addr = smtp_addr
        return self.smtp_addr

    def get_client(self):
        """Get smtp client"""
        return self._client

    def _send(self, msg: MIMEText or MIMEMultipart, receiver):
        try:
            self._client.set_debuglevel(self._debug)
            self._client.ehlo()
            self._client.sendmail(self.user, receiver, msg.as_string())
        except smtplib.SMTPException:
            return 0
        else:
            return 1

    @staticmethod
    def _review_receiver(receiver):
        if isinstance(receiver, str):
            receiver = [receiver]
        return receiver

    def send_mail(self, subject, content, receiver, subtype="html", charset="utf-8"):
        msg = MIMEText(content, subtype, charset)
        msg["Subject"] = Header(subject, charset)
        msg["From"] = formataddr([self.nickname, self.user], charset)

        msg["To"] = ",".join(self._review_receiver(receiver))

        return self._send(msg, receiver)

    def send_mail_with_attachment(self, subject, content, receiver, *file_paths, subtype="html", charset="utf-8"):
        msg = MIMEMultipart()
        msg["Subject"] = Header(subject, charset)
        msg["From"] = formataddr([self.nickname, charset], charset=charset)
        msg["To"] = ",".join(self._review_receiver(receiver))
        msg.attach(MIMEText(content, subtype, charset))

        for file_path in file_paths:
            filename = os.path.split(file_path)[-1]
            file = MIMEText(open(file_path, "rb").read(), "base64", charset)
            file["Content-Type"] = "application/octet-stream"
            file["Content-Disposition"] = f'attachment; filename="{filename}"'
            msg.attach(file)

        return self._send(msg, receiver)

    def process(self, user=None, pwd=None, smtp_addr=None, smtp_port=None, ssl=False):
        """process decorator

        Args:
            user: mailbox account
            pwd: mailbox password
            smtp_addr: current mailbox's smtp addr
            smtp_port: current mailbox's smtp port
            ssl: use SSL, default False
        Usage:
            smtp = Smtp()

            @smtp.process(user="xxx", pwd="xxx")
            def get_content():
                ret = smtp.send_mail("xxx", "xxx", "xxx")
                log.debug(ret)
        """
        user = user or self.user
        pwd = pwd or self.pwd
        smtp_addr = smtp_addr or self.smtp_addr
        smtp_port = smtp_port or self.smtp_port

        assert None not in [user, pwd], \
            "You should give your info."

        def decorator(func):
            def wrapper(*args, **kwargs):
                self.login(user, pwd, smtp_addr, smtp_port, ssl)
                ret = func(*args, **kwargs)
                self.close()
                return ret
            return wrapper
        return decorator


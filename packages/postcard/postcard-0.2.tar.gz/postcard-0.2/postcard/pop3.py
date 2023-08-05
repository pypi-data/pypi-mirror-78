# -*- coding: utf-8 -*-
# @author: leesoar

"""POP3 client"""

import base64
import poplib
from email.parser import Parser

from postcard import setting


__all__ = ["Pop3"]


class Pop3(object):
    def __init__(self):
        self.user = None
        self.pwd = None
        self._client = None
        self.pop_addr = None
        self.pop_port = None
        self.parser = Parser()

    def login(self, user, pwd, pop_addr=None, pop_port=None, ssl=False):
        """Login current mailbox"""
        self.user = user
        self.pwd = pwd
        self.pop_addr = pop_addr or self.pop_addr
        self.pop_port = pop_port or self.pop_port

        if not self.pop_addr:
            self.pop_addr = self._set_pop_addr_auto(user)

        if not self.pop_port:
            self.pop_port = 995 if ssl else 110

        if ssl:
            self._client = poplib.POP3_SSL(self.pop_addr, self.pop_port)
        else:
            self._client = poplib.POP3(self.pop_addr, self.pop_port)
        self._client.user(self.user)
        self._client.pass_(self.pwd)
        return self._client

    def close(self):
        self._client.quit()

    @staticmethod
    def get_addr_map():
        return setting.POP3_ADDR

    def _set_pop_addr_auto(self, user):
        domain = user.rsplit(".", maxsplit=1)[0].split("@")[-1]
        pop_addr = self.get_addr_map().get(domain)
        if pop_addr and not self.pop_addr:
            self.pop_addr = pop_addr
        return self.pop_addr

    def get_client(self):
        """Get pop3 client"""
        return self._client

    def how_many(self) -> int:
        """Return mailbox's email count"""
        return self._client.stat()[0]

    def __check_and_decode(self, mail_info: dict) -> dict:
        """Check encoding and decode mail's content"""
        content_encoding = mail_info.get("content-transfer-encoding", "").lower()

        try:
            if content_encoding == "base64":
                mail_info["content"] = base64.b64decode(mail_info["content"]).decode(errors="ignore")
            elif content_encoding == "quoted-printable":
                pass
        except Exception:
            pass

        return mail_info

    def retrieve(self, index_: int = None) -> dict:
        """Retrieve mail at index"""
        index_ = index_ or self.how_many()
        line_array = self._client.retr(index_)[1]
        delimiter = line_array.index(b"")
        content = (b"".join(line_array[delimiter:])).decode(errors="ignore")

        def __convert(x: bytes) -> list:
            k, v = x.decode(errors="ignore").split(":", 1)
            return [k.lower().strip(), v.lower().strip().lstrip("[").rstrip("]")]

        mail_info = dict(map(__convert, filter(lambda x: b":" in x and b"\t" not in x, line_array)))
        mail_info.update(content=content)
        return self.__check_and_decode(mail_info)

    def delete(self, index_: int = None):
        """Delete mail at index"""
        index_ = index_ or self.how_many()
        self._client.dele(index_)

    def process(self, user=None, pwd=None, pop_addr=None, pop_port=None, ssl=False):
        """process decorator

        Args:
            user: mailbox account
            pwd: mailbox password
            pop_addr: current mailbox's pop3 addr
            pop_port: current mailbox's pop3 port
            ssl: use SSL, default False
        Usage:
            pop = Pop3()

            @pop.process(user="xxx", pwd="xxx")
            def get_content():
                content = pop.retrieve()["content"]
                log.debug(content)
        """
        user = user or self.user
        pwd = pwd or self.pwd
        pop_addr = pop_addr or self.pop_addr
        pop_port = pop_port or self.pop_port

        assert None not in [user, pwd], \
            "You should give your info."

        def decorator(func):
            def wrapper(*args, **kwargs):
                self.login(user, pwd, pop_addr, pop_port, ssl)
                ret = func(*args, **kwargs)
                self.close()
                return ret
            return wrapper
        return decorator

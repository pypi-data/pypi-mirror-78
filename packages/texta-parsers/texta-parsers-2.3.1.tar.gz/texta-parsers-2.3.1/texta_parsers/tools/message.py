from bs4 import BeautifulSoup
from random import getrandbits
import email
import sys
from tika import parser as tika_parser
import os
import uuid
import logging


DIGIDOC_FORMATS = ['.ddoc', '.bdoc', '.asice', '.asics']


class HeaderParser:
    def __init__(self, msg):
        self.msg = msg
        self.fails = {}

    def parse(self):
        header_data = {}
        header_data["from"] = self._get_addr("from")
        header_data["to"] = self._get_addr("to")
        header_data["subject"] = self._get_subject()
        header_data["date"] = self._get_date()

        cc = self._get_addr("cc")
        bcc = self._get_addr("bcc")

        if(cc):
            header_data["cc"] = cc
        if(bcc):
            header_data["bcc"] = bcc

        return header_data

    def _get_addr(self, field):
        try:
            addr_list = email.utils.getaddresses(self.msg.get_all(field, []))

            all_addresses = []
            for addr_tuple in addr_list:
                addr_items = []
                for item in addr_tuple:
                    item_dec, charset = email.header.decode_header(item)[0]

                    if charset:
                        item_str = item_dec.decode(charset)
                    elif type(item_dec) == bytes:
                        item_str = item_dec.decode()
                    else:
                        assert type(item) == str
                        item_str = item_dec

                    if(item_str):
                        addr_items.append(item_str)
                all_addresses.append(" ".join(addr_items))

            return "\n".join(all_addresses)

        except:
            exc_type, value, _ = sys.exc_info()
            self.fails[field] = "{}: {}".format(exc_type.__name__, value)
            return ""

    def _get_subject(self):
        if "subject" in self.msg:
            try:
                subject_parts = email.header.decode_header(self.msg["subject"])

                subject_items = []
                for item_dec, charset in subject_parts:
                    if charset:
                        item_str = item_dec.decode(charset)
                    # charset is None for non-encoded header parts and the part itself a bytestring
                    elif type(item_dec) == bytes:
                        item_str = item_dec.decode()
                    else:
                        # if whole header is non-encoded, result is a string
                        assert type(item_dec) == str
                        item_str = item_dec

                    subject_items.append(item_str.strip())

                return " ".join(subject_items)

            except:
                exc_type, value, _ = sys.exc_info()
                self.fails["subject"] = "{}: {}".format(exc_type.__name__, value)
                return ""
        else:
            return ""

    def _get_date(self):
        if "date" in self.msg:
            date = self.msg["date"]
            if(type(date) == str):
                return email.utils.parsedate_to_datetime(self.msg["date"])
            elif(type(date) == email.header.Header):
                encoded_date, charset = email.header.decode_header(self.msg["date"])[0]
                decoded_date = None
                try:
                    decoded_date = encoded_date.decode(charset)
                except:
                    decoded_date = encoded_date.decode("Windows-1251")

                if(decoded_date):
                    return email.utils.parsedate_to_datetime(decoded_date)

class BodyParser:
    def __init__(self, msg):
        self.msg = msg
        self.fails = {}

    def _parse_body_rec(self, msg):
        if msg.get_content_disposition() == "attachment":  # therefore attachment not body part
            return ""

        body = []
        message_content_type = msg.get_content_type()
        message_main_type = msg.get_content_maintype()

        if message_content_type == "multipart/mixed":
            for payload in msg.get_payload():
                body.append(self._parse_body_rec(payload))
        elif message_main_type == "text":
            body.append(self._parse_text_content(msg))
        elif message_content_type == "multipart/alternative":
            for payload in msg.get_payload():
                body.append(self._parse_body_rec(payload))
                break
        return "\n".join(body).strip()

    def parse_body(self):
        try:
            return self._parse_body_rec(self.msg)
        except:
            exc_type, value, _ = sys.exc_info()
            self.fails["body"] = "{}: {}".format(exc_type.__name__, value)
            return ""

    def _parse_text_content(self, msg):
        body = ""
        subtype = msg.get_content_subtype()
        charset = msg.get_content_charset(failobj="us-ascii")

        if subtype == "html":
            cleaned_body = self._clean_html(msg.get_payload(decode=True).decode(charset))
            body = cleaned_body
        elif subtype == "plain":
            if(msg["Content-Transfer-Encoding"] == "8bit"):
                try:
                    body = msg.get_payload(decode=True).decode(charset)
                except UnicodeDecodeError:
                    body = msg.get_payload(decode=True).decode("latin1")
            else:
                 body = msg.get_payload(decode=True).decode(charset)

        else:
            logging.warning("Content of this type not modified: {}".format(subtype))
            body = msg.get_payload(decode=True).decode(charset)

        return body

    def _parse_attachments_rec(self, msg, save_path, msg_id, max_attachment_size, random_filenames):
        attachments_jsons = []
        for payload in msg.get_payload():
            if type(payload) != str:
                if (payload.get_content_disposition() == "attachment"
                    and payload.get_content_type() != "message/rfc822"):

                    a_parser = AttachmentParser(payload, save_path, msg_id, max_attachment_size, random_filenames)
                    attachment_data = a_parser.parse()

                    if a_parser.fails != {}:
                        attachment_data["errors"] =  a_parser.fails

                    attachments_jsons.append(attachment_data)
                elif payload.is_multipart() and payload.get_content_type() != "message/rfc822":
                    attachments_jsons += self._parse_attachments_rec(payload, save_path, msg_id, max_attachment_size, random_filenames)

        return attachments_jsons

    def parse_attachments(self, save_path, msg_id, max_attachment_size, random_filenames):
        return self._parse_attachments_rec(self.msg, save_path, msg_id, max_attachment_size, random_filenames)

    def _clean_html(self, payload):
        soup = BeautifulSoup(payload, features="lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = "\n".join(line for line in lines if line)
        return text


class AttachmentParser(BodyParser):
    def __init__(self, msg, save_path, msg_id, max_attachment_size, random_filenames):
        BodyParser.__init__(self, msg)
        self.save_path = save_path
        self.msg_id = msg_id
        self.max_attachment_size = max_attachment_size
        self.random_filenames = random_filenames

    def parse(self):
        attachment_id = str(getrandbits(64))
        attachment_json = {"msg_id": self.msg_id, "attachment_id": attachment_id}

        filename = self._get_filename()
        ext = os.path.splitext(filename)[-1]
        attachment_json["filename"] = filename

        if(ext not in DIGIDOC_FORMATS):
            attachment_json["content"] = self._parse_attachment()

        if self.save_path != None and filename != "":
            attachment_dir = os.path.join(self.save_path, self.msg_id)

            if(self.random_filenames):
                ext = os.path.splitext(filename)[-1]
                random_filename = uuid.uuid4().hex + ext
                attachment_path = os.path.join(attachment_dir, random_filename)
            else:
                attachment_path = os.path.join(attachment_dir, filename)
            self._make_dir(attachment_dir)

            try:
                with open(attachment_path, "wb") as f:
                    f.write(self.msg.get_payload(decode=True))
                attachment_json["filepath"] = attachment_path  
            except OSError:
                exc_type, value, _ = sys.exc_info()
                self.fails["filename"] = "{}: {}".format(exc_type.__name__, value)
            except TypeError:
                exc_type, value, _ = sys.exc_info()
                self.fails["filepath"] = "{}: {}".format(exc_type.__name__, value)
                

        return attachment_json

    def _get_filename(self):
        try:
            encoded_filename = self.msg.get_filename()
            return AttachmentParser.parse_filename(encoded_filename)
        except:
            exc_type, value, _ = sys.exc_info()
            self.fails["filename"] = "{}: {}".format(exc_type.__name__, value)
            return ""

    @staticmethod
    def parse_filename(encoded_filename):
        filename_parts = email.header.decode_header(encoded_filename)

        filename_items = []
        for item_dec, charset in filename_parts:
            if charset:
                item_str = item_dec.decode(charset)
            elif type(item_dec) == bytes:
                item_str = item_dec.decode()
            else:
                assert type(item_dec) == str
                item_str = item_dec

            filename_items.append(item_str.strip())

        return "".join(filename_items)

    def _parse_attachment(self):
        attachment_payload = self.msg.get_payload(decode=True)
        if(attachment_payload == None):
            self.fails["content"] = "{}".format("No payload")
            return ""
        
        if(not self._file_size_ok(attachment_payload)):
            self.fails["content"] = "File too large for content parsing."
            return ""
        else:
            result = tika_parser.from_buffer(attachment_payload)
            content = result["content"]

            if result["status"] != 200:
                self.fails["content"] = "{}: {}".format("tika", result["status"])
            if content == None:
                return ""

            lines = (line.strip() for line in content.splitlines())
            text = "\n".join(line for line in lines if line)
            return text

    def _file_size_ok(self, payload):
        if(len(payload) > self.max_attachment_size*1024**2):
            return False
        return True

    def _make_dir(self, f_dir):
        if not os.path.exists(f_dir):
            os.makedirs(f_dir)

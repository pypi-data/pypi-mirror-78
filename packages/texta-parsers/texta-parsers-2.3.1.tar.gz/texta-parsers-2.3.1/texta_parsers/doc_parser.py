import csv
import os
import shutil
import uuid
from subprocess import Popen

import pandas as pd
from pyunpack import Archive
from tika import parser

from texta_parsers.email_parser import EmailParser
from texta_parsers.settings import META_FIELD
from texta_parsers.tools.extension import Extension
from texta_parsers.tools.scanner import DocScanner
from . import exceptions


# for digidoc parser
FNULL = open(os.devnull, "w")


class DocParser:

    def __init__(self, temp_dir="", languages=["est", "eng", "rus"]):
        """
        :param: list languages: Languages for TikaOCR.
        """
        self.temp_dir = self.create_temp_dir_for_parse(temp_dir)
        self.langs = languages
        self.scanner = DocScanner()


    @staticmethod
    def create_temp_dir_for_parse(temp_dir):
        """
        Creates temp directory path.
        """
        temp_dir_for_parse = os.path.join(temp_dir, "temp_" + uuid.uuid4().hex)
        if not os.path.exists(temp_dir_for_parse):
            os.mkdir(temp_dir_for_parse)
        return temp_dir_for_parse


    def _write_uploaded_to_file(self, uploadedfile, file_name):
        if not file_name:
            raise exceptions.InvalidInputError("File name not supported.")
        # get extension from file name if any
        extension = Extension.predict(uploadedfile, file_name=file_name)
        # create new path with predicted extension
        new_name = uuid.uuid4().hex + extension
        # new_name = uploadedfile.name
        file_path = os.path.join(self.temp_dir, new_name)
        with open(file_path, "wb") as fh:
            fh.write(uploadedfile)
        return file_path


    def _extract_digidoc(self, input_path, output_dir, extracted=[]):
        """
        Extracts contents from digidoc. Works recursively.
        """
        cmd = f"digidoc-tool open {input_path} --extractAll={output_dir}"
        p = Popen(cmd, shell=True, stdout=FNULL)
        p.wait()
        # generate full paths for the output
        extracted_docs = os.listdir(output_dir)
        extracted_docs = [os.path.join(output_dir, file_name) for file_name in extracted_docs]
        # extract further if digidocs in output
        for extracted_doc in extracted_docs:
            ext = Extension.predict(extracted_doc)
            if ext in Extension.DIGIDOC_EXTENSIONS:
                self._extract_digidoc(extracted_doc, output_dir, extracted=extracted)
            else:
                extracted.append(extracted_doc)
        return extracted


    def _extract_archive(self, input_path, output_dir, extension):
        """
        Extracts contents from archives. Works recursively.
        """
        # create temporary output directory
        # just to be safe, because file names may repeat
        output_dir = os.path.join(output_dir, uuid.uuid4().hex)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # extract with digidoc client
        if extension in Extension.DIGIDOC_EXTENSIONS:
            extracted_paths = self._extract_digidoc(input_path, output_dir)
        else:
            archive = Archive(input_path)
            archive.extractall(output_dir)
        # generate full paths for the output
        extracted_paths = os.listdir(output_dir)
        extracted_paths = [os.path.join(output_dir, file_name) for file_name in extracted_paths]
        # extract further if archives in output
        for extracted_path in extracted_paths:
            if os.path.isdir(extracted_path):
                ### TODO: HOLY SHIT ITS A DIRECTORY INSIDE AN ARCHIVE!
                pass
            else:
                extracted_extension = Extension.predict(extracted_path)
                if extracted_extension in Extension.ARCHIVE_EXTENSIONS:
                    for doc in self._extract_archive(extracted_path, output_dir, extracted_extension):
                        yield doc
                elif extracted_extension in Extension.KNOWN_EXTENSIONS:
                    yield {"path": extracted_path, "extension": extracted_extension}


    def remove_temp_dir(self):
        """
        Removes temp directory path.
        """
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


    @staticmethod
    def _parse_file(document, languages):
        """
        Parses document using TIKA and Speech2Text
        """
        output_documents = []
        # TODO: WTF HAPPENS WITH OCR?
        tika_output = parser.from_file(document["path"], requestOptions={"headers": {"X-Tika-OCRLanguage": "+".join(languages)}})
        content = tika_output["content"]
        if content != None:  # remove leading and trailing spacing
            content = content.strip()

        output_documents.append({"text": content})
        return output_documents


    @staticmethod
    def _parse_collection(document):
        if (document["extension"] == ".csv"):
            # detect dialect and whether contains header
            with open(document["path"]) as f:
                lines = f.readline() + '\n' + f.readline()
                dialect = csv.Sniffer().sniff(lines)
                f.seek(0)

                has_header = csv.Sniffer().has_header(lines)
                f.seek(0)

            header = "infer" if has_header else None
            # read and yield actual data with pandas (more convenient)
            reader = pd.read_csv(document["path"], dialect=dialect, chunksize=1000, header=header)

            for chunk in reader:
                for ix, row in chunk.iterrows():
                    yield row.to_dict()

        # .xls or .xlsx
        else:
            reader = pd.read_excel(document["path"], header=0, sheet_name=None)  # dont know whether there is a header but assume that the first row is

            if isinstance(reader, dict):
                for sheet_name, df in reader.items():
                    df.fillna("", inplace=True)
                    for ix, row in df.iterrows():
                        yield row.to_dict()
            else:
                reader.fillna("", inplace=True)
                for ix, row in reader.iterrows():
                    yield row.to_dict()


    def _parse_mail(self, document):
        parser = EmailParser(tmp_folder=self.temp_dir)
        return parser.parse(document["path"])


    def parse(self, parser_input, file_name=None):
        """
        :param: str parser_input: Base64 string or file path.
        """
        if isinstance(parser_input, bytes):
            # input is in bytes
            file_paths = [self._write_uploaded_to_file(parser_input, file_name)]
        elif isinstance(parser_input, str):
            # input is path to file as string
            if not os.path.exists(parser_input):
                raise exceptions.InvalidInputError("File does not exist.")
            # input is a directory and we should scan it
            if os.path.isdir(parser_input):
                file_paths = self.scanner.scan(parser_input)
            else:
                file_paths = [parser_input]
        else:
            raise exceptions.InvalidInputError("Input should be path to file/directory or bytes.")

        # apply parsers for all paths in input
        for file_path in file_paths:
            print(file_path)
            docs_to_parse = []
            # guess extension (it also performs chck if extension is known)
            extension = Extension.predict(file_path, file_name=file_name)
            # check if an archive
            if extension in Extension.ARCHIVE_EXTENSIONS:
                docs_to_parse = self._extract_archive(file_path, self.temp_dir, extension)
            else:
                docs_to_parse.append({"path": file_path, "extension": extension})
            # parse file
            for meta in docs_to_parse:
                if (meta["extension"] in Extension.EMAIL_EXTENSIONS):
                    # returns email generator
                    gen = self._parse_mail(meta)
                    # yield items from it
                    for msg_dict, attachment_dicts in gen:
                        # add metadata to result
                        msg_dict[META_FIELD] = meta
                        for attachment in attachment_dicts:
                            attachment[META_FIELD] = meta
                        yield msg_dict, attachment_dicts
                elif (meta["extension"] in Extension.COLLECTION_EXTENSIONS):
                    # returns collection generator
                    gen = self._parse_collection(meta)
                    # yield items from it
                    for item in gen:
                        item[META_FIELD] = meta
                        yield item
                else:
                    for parsed_document in self._parse_file(meta, languages=self.langs):
                        parsed_document[META_FIELD] = meta
                        yield parsed_document

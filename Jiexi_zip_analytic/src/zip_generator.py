
""" This filer contains functions and classes related to generating XML files
and creating zip archives. Works in multiprocess mode.
"""

import os
import uuid
import string
import random
import zipfile

from wheezy.template.engine import Engine
from wheezy.template.loader import DictLoader
from wheezy.template.ext.core import CoreExtension

from settings import *
from process_worker import MultiprocessingWrapper


def load_template(file_path):
    with open(file_path, 'r') as template_file:
        return template_file.read()


def generate_zip_files_in_processes(args):
    """Run generation ZIP archives one per process from process pool

    @param `args`: program launching arguments;
    """
    mp = MultiprocessingWrapper()
    mp.pool.map(generate_zip_files, ((args, idx) for idx in xrange(NUMBER_OF_ZIP_FILES)))
    mp.pool.close()
    mp.pool.join()


def generate_zip_files(_args):
    """Generate zip file

    @param `_args` (args, zip_idx): program launching arguments, zip file index number;
    """
    args, zip_idx = _args
    xml_generator = XMLGenerator(
        tmpl=load_template(TEMPLATE_PATH),
        number_range=RANDOM_LEVEL_NUMBER_LIMITS,
        string_count_range=RANDOM_OBJECTS_LIMITS,
        args=args
    )

    zip_filename = os.path.join(args.output_dst, str(zip_idx) + '.zip')

    if not os.path.exists(args.output_dst):
        os.makedirs(args.output_dst)

    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    for xml_idx in xrange(NUMBER_OF_XML_FILES_IN_ZIP):
        zipf.writestr(*xml_generator.generate_xml_file())

    zipf.close()


class XMLGenerator(object):

    """Class for generation XML files with predefined structure with random values"""

    def __init__(self, tmpl, number_range, string_count_range, args, string_len_range=(2, 16)):
        engine = Engine(loader=DictLoader({'x': unicode(tmpl)}), extensions=[CoreExtension()])
        self.args = args
        self.tmpl = engine.get_template('x')
        self.asci_chrs = list(string.ascii_uppercase + string.ascii_lowercase + ' ')
        self.number_range = number_range
        self.string_count_range = string_count_range
        self.string_len_range = string_len_range

    def generate_xml_file(self):
        """Generate XML file

        @return:
            XML filename and XML file data.
        """
        unique_id = unicode(uuid.uuid4())
        xml_content = self.tmpl.render({
            'uniq_string_value': unique_id,
            'rand_number': unicode(self.__get_rand_number(self.number_range)),
            'random_strings': self.__get_random_strings(),
        })

        file_name = unique_id + '.xml'
        return file_name, xml_content

    def __get_random_strings(self):
        strings_count = self.__get_rand_number(self.string_count_range)

        return [unicode('').join(
            random.sample(self.asci_chrs, self.__get_rand_number(self.string_len_range))
        ) for i in xrange(strings_count)]

    def __get_rand_number(self, ranges):
        return random.randint(*ranges)


""" This filer contains functions and classes related to reading
zip archives and analyze files in this archives. Works in multiprocess mode.
"""

import os
import csv
import zipfile

from io import BytesIO
from lxml import etree

from settings import *
from process_worker import MultiprocessingWrapper


def analyze_zip_files_in_processes(args):
    """Launch one zip file analyzing per process

    @param `args`: program launching arguments;
    """
    mp = MultiprocessingWrapper()
    jobs = []

    mp.pool.apply_async(result_writer, (args, mp.managers_queue))

    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if '.zip' in filename:
                zip_filename = os.path.join(dirname, filename)
                jobs.append(mp.pool.apply_async(analyze_zip_files, (zip_filename, mp.managers_queue)))

    for job in jobs:
        job.get()

    # Stop file writer as soon as all workers has been stopped
    mp.managers_queue.put('kill')

    mp.pool.close()
    mp.pool.join()


def result_writer(args, queue):
    """Write results into csv files.

    @param `args`: program launching arguments;
    @param `queue`: cross-proses queue;
    """
    try:
        id_level_csv_name = os.path.join(args.output_dst, args.id_level_csv)
        with open(id_level_csv_name, 'w') as id_value_csv_file:
            id_value_csv_writer = csv.writer(id_value_csv_file, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

            id_name_csv_name = os.path.join(args.output_dst, args.id_name_csv)
            with open(id_name_csv_name, 'w') as id_name_csv_file:
                id_name_csv_writer = csv.writer(id_name_csv_file, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                while True:
                    task = queue.get()
                    if task == 'kill':
                        break

                    if isinstance(task, dict):
                        id_value_csv_writer.writerow([task.get('id'), task.get('level')])
                        id_name_csv_writer.writerows(
                            ((task.get('id'), object_name) for object_name in task.get('object_names'))
                        )
    except Exception, e:
        print e


def analyze_zip_files(zip_filename, queue):
    """Extract zip file and analyze it content

    @param `zip_filename`: full zip filename;
    @param `queue`: cross-proses queue;;
    """
    xml_analyzer = XMLAnalyzer(queue)

    try:
        with open(zip_filename, 'r') as zip_file:
            zip_filename_io = BytesIO(zip_file.read())
        zipf = zipfile.ZipFile(zip_filename_io, 'r', zipfile.ZIP_DEFLATED)
        for xml_file_name in zipf.namelist():
            try:
                xml_analyzer.analyze_xml(unicode(zipf.read(xml_file_name)))
            except etree.XMLSyntaxError:
                print 'XML syntax error in %s file located in %s zip' % (xml_file_name, zip_filename)

        zipf.close()

    except zipfile.BadZipfile, e:
        print 'File %s is not zip file' % (zip_filename)

    except Exception, e:
        print e


class XMLAnalyzer:

    """Simple XML analyzer. Just read XML file content, get some predefined data
    and return back to result queue."""

    def __init__(self, results_queue):
        self.results_queue = results_queue

    def analyze_xml(self, str_xml_data):
        """Analyze XML data (read predefined data) and store to result queue.

        @param `str_xml_data`: XML string data;
        """
        xml_data = {
            'id': None,
            'level': None,
            'object_names': []
        }

        root = etree.fromstring(str_xml_data)
        for var_el in root.findall('var'):
            xml_data[var_el.get('name')] = var_el.get('value')

        for object_el in root.find('objects').findall('object'):
            xml_data['object_names'].append(object_el.get('name'))

        self.results_queue.put(xml_data)

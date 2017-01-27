
import os
import csv
import shutil
import zipfile

from lxml import etree

from settings import *
from thread_worker import get_pool
from process_worker import MultiprocessingWrapper


def analyze_zip_files_in_processes(args):
    mp = MultiprocessingWrapper()
    jobs = []

    mp.pool.apply_async(result_writer, (mp.managers_queue, ))

    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if '.zip' in filename:
                zip_filename = os.path.join(dirname, filename)
                jobs.append(mp.pool.apply_async(analyze_zip_files, (zip_filename, mp.managers_queue)))

    mp.managers_queue.put('kill')

    mp.pool.close()
    mp.pool.join()


def result_writer(q):
    id_value_csv = 'id_value.csv'
    id_names_csv = 'id_names.csv'
    try:
        with open(id_value_csv, 'w') as id_value_csv_file:
            id_value_csv_writer = csv.writer(id_value_csv_file, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            with open(id_names_csv, 'w') as id_names_csv_file:
                id_names_csv_writer = csv.writer(id_names_csv_file, delimiter=' ',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                while True:
                    task = q.get()
                    if task == 'kill':
                        break

                    if isinstance(task, dict):
                        id_value_csv_writer.writerow([task.get('id'), task.get('level')])
                        id_names_csv_writer.writerows([[task.get('id'), object_name] for object_name in task.get('object_names')])
    except Exception, e:
        print e


def analyze_zip_files(zip_filename, q):
    xml_analyzer = XMLAnalyzer(q)
    zipf = zipfile.ZipFile(zip_filename, 'r', zipfile.ZIP_DEFLATED)
    for xml_file_name in zipf.namelist():
        xml_analyzer.analyze_xml(unicode(zipf.read(xml_file_name)))

    zipf.close()


class XMLAnalyzer:

    def __init__(self, results_queue):
        self.results_queue = results_queue

    def analyze_xml(self, str_xml_data):
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


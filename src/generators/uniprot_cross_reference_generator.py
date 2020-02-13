import os
import time

import csv
import logging
import upload

logger = logging.getLogger(name=__name__)


class UniProtGenerator:

    file_header = '''UniProtID\tIdentifier'''

    def __init__(self, relationships, config_info, generated_files_folder):
        self.relationships = relationships
        self.config_info = config_info
        self.generated_files_folder = generated_files_folder

    def _write_uniprot_file(cls, relationships, tab_file):
        logger.info('Writing output file')
        output_file = open(cls.generated_files_folder + '/' + tab_file, 'w')
        output_file.write(cls.file_header + '\n')
        output_file.close()

        with open(cls.generated_files_folder + '/' + tab_file, 'a') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            for item in relationships:
                writer.writerow([item['GlobalCrossReferenceID'], item['GeneID']])
        tsvfile.close()

    def generate_file(self, upload_flag=False):
        self._write_uniprot_file(self.relationships, 'CROSSREFERENCEUNIPROT_COMBINED.tsv')
        logger.info('File created')
        if upload_flag:
            logger.info("Submitting CROSSREFERENCEUNIPROT_COMBINED to FMS")
            process_name = "1"
            upload.upload_process(process_name, 'CROSSREFERENCEUNIPROT_COMBINED.tsv', self.generated_files_folder, 'CROSSREFERENCEUNIPROT', 'COMBINED', self.config_info)
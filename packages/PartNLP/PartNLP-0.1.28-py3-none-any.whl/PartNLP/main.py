"""
        PartNLP
            AUTHORS:
                MOSTAFA & SAMAN
"""
from PartNLP.core import Pipeline
from PartNLP.models.helper.constants import SUPPORTED_PROCESSORS_FOR_PACKAGES
from tqdm import tqdm
import logging
import os

BATCH_SIZES = [1000000, 10000000, 100000000, 1000000000]
# PACKAGES = ['HAZM', 'PARSIVAR', 'STANZA']


def main(packages):
    for batch_size in BATCH_SIZES:
        for package in tqdm(packages):
            Pipeline(package=package, input_file_format='TXT', file_path='/dataset/test.txt',
                     processors=SUPPORTED_PROCESSORS_FOR_PACKAGES[package], batch_size=batch_size)
    logging.info(f'the result has been saved in {os.getcwd()}/preprocessed folder')

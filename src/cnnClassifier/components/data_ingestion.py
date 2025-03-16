import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from pathlib import Path

import os
import gdown
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            # Convert Google Drive URL to direct download URL
            file_id = self.config.source_URL.split('/')[-2]  # Extract file ID
            download_url = f"https://drive.google.com/uc?id={file_id}"

            # Download file using gdown
            gdown.download(download_url, str(self.config.local_data_file), quiet=False)
            
            logger.info(f"File downloaded successfully: {self.config.local_data_file}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """ Extracts the ZIP file into the data directory """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            logger.info(f"Extraction completed at {unzip_path}")
        except zipfile.BadZipFile:
            logger.error("Downloaded file is not a valid ZIP. Check the source file.")
            raise

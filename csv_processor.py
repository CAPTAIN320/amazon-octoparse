import os
import csv
import glob
import shutil

import pandas as pd


# create folders for files
def create_folders():
    # CSV Path Directories
    csv_from_zon_Dir = './csv_from_zon'
    csv_from_zon_processed_Dir = './csv_from_zon_processed'
    csv_merchant_url_Dir = './csv_merchant_url'
    csv_product_url_Dir = './csv_product_url'
    csv_merchant_Octo_Dir = './csv_merchant_Octo'
    csv_product_Octo_Dir = './csv_product_Octo'
    concatenated_Dir = './concatenated'

    try:
        os.mkdir(csv_from_zon_Dir)
        os.mkdir(csv_from_zon_processed_Dir)
        os.mkdir(csv_merchant_url_Dir)
        os.mkdir(csv_product_url_Dir)
        os.mkdir(csv_merchant_Octo_Dir)
        os.mkdir(csv_product_Octo_Dir)
        os.mkdir(concatenated_Dir)
        print("Folders created!")
    except:
        print("Folders already created!")
        pass









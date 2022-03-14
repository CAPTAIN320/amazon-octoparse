import csv_processor
import filter
import listing


def start_csv_from_zon_processing():
    csv_processor.create_folders()

    csv_processor.create_urls(csv_from_zon_PATH = "./csv_from_zon",
                              merchant_url_PATH = "./csv_merchant_url",
                              csv_from_zon_processed_PATH = './csv_from_zon_processed')

def start_csv_merchant_Octo_processing():
    filter.csv_merchant_octo()

def create_lists():
    listing.create_blacklist()

    listing.create_whitelist()

    listing.create_whitelist_ASIN()



if __name__ == '__main__':

    start_csv_from_zon_processing()

    start_csv_merchant_Octo_processing()

    create_lists()



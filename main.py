import csv_processor
import concatenate


def start_csv_processing():
    csv_processor.create_folders()

    csv_processor.create_urls(csv_from_zon_PATH = "./csv_from_zon",
                              merchant_url_PATH = "./csv_merchant_url",
                              product_url_PATH = "./csv_product_url",
                              csv_from_zon_processed_PATH = './csv_from_zon_processed')

def start_concatenate():
    concatenate.all(csv_merchant_Octo_PATH = './csv_merchant_octo',
                    csv_product_Octo_PATH = './csv_product_octo',
                    csv_from_zon_processed_PATH='./csv_from_zon_processed',
                    concatenated_PATH='./concatenated',
                    concatenated_ASIN_PATH='./concatenated_ASIN',
                    concatenated_HTML_PATH='./concatenated_HTML')

if __name__ == '__main__':

    start_csv_processing()

    start_concatenate()



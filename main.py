import csv_processor


def start_csv_processing():
    csv_processor.create_folders()

    csv_processor.create_urls(csv_from_zon_PATH = "./csv_from_zon",
                              merchant_url_PATH = "./csv_merchant_url",
                              product_url_PATH = "./csv_product_url",
                              csv_from_zon_processed_PATH = './csv_from_zon_processed')

if __name__ == '__main__':

    start_csv_processing()



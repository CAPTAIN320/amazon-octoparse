import os
import csv
import glob
import shutil

import pandas as pd


# create folders for files
def create_folders():
    # CSV Path Directories
    csv_from_zon_PATH = './csv_from_zon'
    csv_from_zon_processed_PATH = './csv_from_zon_processed'
    csv_merchant_url_PATH = './csv_merchant_url'
    csv_product_url_PATH = './csv_product_url'
    csv_merchant_Octo_PATH = './csv_merchant_Octo'
    csv_product_Octo_PATH = './csv_product_Octo'
    concatenated_PATH = './concatenated'
    concatenated_ASIN_PATH = './concatenated_ASIN'
    concatenated_HTML_PATH='./concatenated_HTML'
    blacklist_PATH = './blacklist'
    whitelist_PATH = './whitelist'

    try:
        os.mkdir(csv_from_zon_PATH)
        os.mkdir(csv_from_zon_processed_PATH)
        os.mkdir(csv_merchant_url_PATH)
        os.mkdir(csv_product_url_PATH)
        os.mkdir(csv_merchant_Octo_PATH)
        os.mkdir(csv_product_Octo_PATH)
        os.mkdir(concatenated_PATH)
        os.mkdir(concatenated_ASIN_PATH)
        os.mkdir(concatenated_HTML_PATH)
        os.mkdir(blacklist_PATH)
        os.mkdir(whitelist_PATH)
        print("Folders created!")
    except:
        print("Folders already created!")
        pass

# creates Merchant and Product urls
def create_urls(csv_from_zon_PATH = "./csv_from_zon",
                merchant_url_PATH = "./csv_merchant_url",
                product_url_PATH = "./csv_product_url",
                csv_from_zon_processed_PATH = './csv_from_zon_processed'):
    # Path of csv from ZonAsin
    csv_files = glob.glob(csv_from_zon_PATH+"/*.csv")
    for file in csv_files:
        base_file_name = os.path.basename(file)
        print(base_file_name)
        file_name = os.path.splitext(base_file_name)[0]
        print(file_name)

        # reads csv file and assigns it to a dataframe
        df = pd.read_csv(file)

        # removes duplicate ASIN
        df = df.drop_duplicates(subset=["ASIN"])
            
        # sets ASIN as the index (unique ID) of the dataframe
        df = df.set_index("ASIN", drop=False)
            
        # retains only ASINs with a Brand
        df = df[df["Brand"].notnull()]
        
        # sorts values prioritizing MerchantID and then Brand
        df = df.sort_values(["MerchantID", "Brand"])

        # removes duplicate Brand
        df = df.drop_duplicates(subset=["Brand"], keep="first")

        merchant_url_array = []
        for id in df["MerchantID"]:
            url = "https://www.amazon.com/gp/help/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller={}&isAmazonFulfilled=1"
            merchant_url = url.format(id)
            merchant_url_array.append(merchant_url)
        
        df["merchant_url"] = merchant_url_array

        # datafram with only ASINs with a MerchantID
        df_merchant_id = df[df["MerchantID"].notnull()]
        df_merchant_id["merchant_url"].to_csv(os.path.join(merchant_url_PATH, file_name + '_merchant_url.csv'),
                                            index=False)
        print("exported ",df_merchant_id["merchant_url"].count()," merchant urls")

        # dataframe with only ASINs without a MerchantID
        df_no_merchant_id = df[df["MerchantID"].isnull()]
        # removes ASINs sold by Amazon
        # print("There are ",df_no_merchant_id["SoldBy"].value_counts()["Amazon.com"]," Amazon.com")
        df_no_merchant_id = df_no_merchant_id[df_no_merchant_id["SoldBy"].isnull()]
        df_no_merchant_id["URL"].to_csv(os.path.join(product_url_PATH, file_name + '_product_url.csv'),
                                            index=False)
        print("exported ",df_no_merchant_id["URL"].count()," product urls")

        # generate and export csv file
        df.to_csv(os.path.join(csv_from_zon_processed_PATH, file_name + '_processed.csv'))

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
    csv_merchant_Octo_PATH = './csv_merchant_Octo'
    csv_merchant_Octo_processed_PATH = './csv_merchant_Octo_processed'
    blacklist_PATH = './blacklist'
    whitelist_PATH = './whitelist'
    whitelist_ASIN_PATH = './whitelist_ASIN'
    csv_filtered_PATH = './csv_filtered'

    try:
        os.mkdir(csv_from_zon_PATH)
        os.mkdir(csv_from_zon_processed_PATH)
        os.mkdir(csv_merchant_url_PATH)
        os.mkdir(csv_merchant_Octo_PATH)
        os.mkdir(csv_merchant_Octo_processed_PATH)
        os.mkdir(blacklist_PATH)
        os.mkdir(whitelist_PATH)
        os.mkdir(whitelist_ASIN_PATH)
        os.mkdir(csv_filtered_PATH)
        print("Folders created!")
    except:
        print("Folders already created!")
        pass

# creates Merchant and Product urls
def create_urls(csv_from_zon_PATH = "./csv_from_zon",
                merchant_url_PATH = "./csv_merchant_url",
                csv_from_zon_processed_PATH = './csv_from_zon_processed',
                blacklist_File = './blacklist/MerchantID_blacklist.csv',
                whitelist_File = './whitelist/MerchantID_whitelist.csv'):
    
    df_blacklist = pd.read_csv(blacklist_File)
    df_whitelist = pd.read_csv(whitelist_File)

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

        # dataframe with only ASINs with a MerchantID
        df_merchant_id = df[df["MerchantID"].notnull()]

        

        df_merchant_id["merchant_url"].to_csv(os.path.join(merchant_url_PATH, file_name + '_merchant_url.csv'),
                                            index=False)
        print("exported ",df_merchant_id["merchant_url"].count()," merchant urls")

        # generate and export csv file
        df.to_csv(os.path.join(csv_from_zon_processed_PATH, file_name + '_processed.csv'))


# Returns csv output of Merchant ID with Country
def csv_merchant_octo(csv_merchant_Octo_PATH = './csv_merchant_octo',
                      csv_merchant_Octo_processed_PATH = './csv_merchant_Octo_processed'):

    csv_files_merchant_OCTO = glob.glob(csv_merchant_Octo_PATH + "/*.csv")

    for file in csv_files_merchant_OCTO:

        base_file_name = os.path.basename(file)
        print(base_file_name)
        file_name = os.path.splitext(base_file_name)[0]
        file_name = file_name[:-14]

        print("Processing Merchant Octo file: "+ file_name.title())

        df_merchant_octo = pd.read_csv(os.path.join(csv_merchant_Octo_PATH, file_name + '_merchant_octo.csv'))
    
        merchant_id_octo = []
        for url in df_merchant_octo["Page_URL"]:
            merchant_id_from_url = url[41:-20]
            merchant_id_octo.append(merchant_id_from_url)

        df_merchant_octo["merchant_id_octo"] = merchant_id_octo
        # print(df_merchant_octo["merchant_id_octo"])

        df_merchant_octo["business_address"] = df_merchant_octo["business_address"].astype(str)
        country_merchant_octo = []
        for merchant_address in df_merchant_octo["business_address"]:
            country_merchant = merchant_address[-2:]
            country_merchant_octo.append(country_merchant)

        df_merchant_octo["country_merchant_octo"] = country_merchant_octo

        df = pd.DataFrame()
        # df["MerchantID", "country_merchant_octo"] = df_merchant_octo[["merchant_id_octo","country_merchant_octo"]]
        df["MerchantID"] = df_merchant_octo["merchant_id_octo"]
        df["country_merchant_octo"] = df_merchant_octo["country_merchant_octo"]
        print (df)

        # generate and export csv file
        return df.to_csv(os.path.join(csv_merchant_Octo_processed_PATH, file_name + '.csv'), index=False)

create_urls()
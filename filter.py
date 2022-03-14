import os
import csv
import glob
import shutil

import pandas as pd

# Returns dataframe output of Merchant ID with Country
def csv_merchant_octo(csv_merchant_Octo_PATH = './csv_merchant_octo'):

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

        df = df_merchant_octo[["merchant_id_octo","country_merchant_octo"]]
        print (df)

        return df

# merge product_octo with csv_processed
# def csv_product_octo(csv_product_Octo_PATH = './csv_product_octo'):

#     csv_files_product_OCTO = glob.glob(csv_product_Octo_PATH + "/*.csv")

#     for file in csv_files_product_OCTO:

#         base_file_name = os.path.basename(file)
#         print(base_file_name)
#         file_name = os.path.splitext(base_file_name)[0]
#         file_name = file_name[:-13]

#         df_product_octo = pd.read_csv(os.path.join(csv_product_Octo_PATH, file_name + '_product_octo.csv'))
    
#         df_product_octo["seller_address"] = df_product_octo["seller_address"].astype(str)
#         country_product_octo = []
#         for product_address in df_product_octo["seller_address"]:
#             country_product = product_address[-2:]
#             country_product_octo.append(country_product)

#         df_product_octo["country_product_octo"] = country_product_octo

#         print(df_product_octo)
#         return df_product_octo

# exports the concatenated csv file
# def export_concantenated_csv(merge_df,
#                              file_name,
#                              concatenated_PATH='./concatenated'):
#     merge_df = merge_df[["ASIN", 
#                          "Brand",
#                          "SoldBy", 
#                          "MerchantID", 
#                          "country_merchant_octo",
#                          "country_product_octo"]]
#     merge_df.to_csv(os.path.join(concatenated_PATH, file_name + '_concatenated.csv'),
#                     index=False)

# exports the concatenated ASIN csv file
# def export_ASIN_csv(merge_df,
#                     file_name,
#                     concatenated_ASIN_PATH='./concatenated_ASIN'):
#     merge_df = merge_df[["ASIN"]]
#     merge_df.to_csv(os.path.join(concatenated_ASIN_PATH, file_name + '_concatenated_ASIN.csv'),
#                     index=False)

# exports the concatenated csv file as html
# def export_html(merge_df,
#                 file_name,
#                 concatenated_HTML_PATH='./concatenated_HTML'):
#     merge_df = merge_df[["ASIN",
#                          "Brand",
#                          "SoldBy",
#                          "MerchantID",
#                          "country_merchant_octo",
#                          "country_product_octo"]]

#     merge_df.to_html(os.path.join(concatenated_HTML_PATH, file_name + '.html'),
#                      escape=False)






csv_merchant_octo(csv_merchant_Octo_PATH = './csv_merchant_octo')
# csv_product_octo(csv_product_Octo_PATH = './csv_product_octo')


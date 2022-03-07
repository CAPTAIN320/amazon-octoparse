# This file creates blacklist and whitelist

import glob
import pandas as pd
import os
from functools import reduce

def create_blacklist(concatenated_PATH='./concatenated',
                     blacklist_PATH='./blacklist'):
    csv_files = glob.glob(concatenated_PATH + "/*.csv")

    blacklist_merchant_array = []
    blacklist_product_array = []
    for file in csv_files:
        base_file_name = os.path.basename(file)
        file_name = os.path.splitext(base_file_name)[0]
        file_name = file_name[:-13]

        print("Extracting blacklists from: "+ file_name.title())
        
        df_concantenated = pd.read_csv(file)
        # print(df_concantenated)

        df_merchant = df_concantenated[["MerchantID", 
                                        "country_merchant_octo"]]
        
        df_product = df_concantenated[["Brand",
                                        "country_product_octo"]]
        
        # get Chinese rows from merchant_octo
        df_blacklist_merchant = df_merchant.loc[df_merchant["country_merchant_octo"] == "CN"]
        # print(df_blacklist_merchant)
        
        blacklist_merchant_array.append(df_blacklist_merchant)
        
        # get Chinese rows from product_octo
        df_blacklist_product = df_product.loc[df_product["country_product_octo"] == "CN"]
        # print(df_blacklist_product)
        
        blacklist_product_array.append(df_blacklist_product)
        

    # merge blacklist of merchant IDs
    df_blacklist_merchant_merged = reduce(lambda left,right: pd.merge(left,
                                                    right,
                                                    how='outer'),
                                        blacklist_merchant_array)
    print(len(blacklist_merchant_array) , "merchant files merged to form blacklist.")

    # removes duplicate MerchantID
    df_blacklist_merchant_merged = df_blacklist_merchant_merged.drop_duplicates(subset=["MerchantID"],
                                                                                keep="first")

    # exports merchant blacklist as csv file
    df_blacklist_merchant_merged.to_csv(os.path.join(blacklist_PATH, 'MerchantID_blacklist.csv'),
                                        index=False)
    print(df_blacklist_merchant_merged)

    # merge blacklist of merchant IDs
    df_blacklist_product_merged = reduce(lambda  left,right: pd.merge(left,
                                                    right,
                                                    how='outer'),
                                        blacklist_product_array)
    print(len(blacklist_product_array) , "merchant files merged to form blacklist.")

    # removes duplicate Brand
    df_blacklist_product_merged = df_blacklist_product_merged.drop_duplicates(subset=["Brand"],
                                                                            keep="first")

    # exports Brand blacklist as csv file
    df_blacklist_product_merged.to_csv(os.path.join(blacklist_PATH, 'Brand_blacklist.csv'),
                                        index=False)

def create_whitelist(concatenated_PATH='./concatenated',
                     whitelist_PATH='./whitelist'):

    csv_files = glob.glob(concatenated_PATH + "/*.csv")

    whitelist_merchant_array = []
    whitelist_product_array = []
    for file in csv_files:    
        country_array = ["US", "GB", "GR", "CA", "AU", "KR", "FR"]

    for country in country_array:
            base_file_name = os.path.basename(file)
            file_name = os.path.splitext(base_file_name)[0]
            file_name = file_name[:-13]

            print("Extracting whitelists from: "+ file_name)

            df_concantenated = pd.read_csv(file)
            #print(df_concantenated)

            df_merchant = df_concantenated[["MerchantID", 
                                            "country_merchant_octo"]]
            
            df_product = df_concantenated[["Brand",
                                        "country_product_octo"]]
            
            #get US rows from merchant_octo
            df_whitelist_merchant = df_merchant.loc[df_merchant["country_merchant_octo"] == country]
            #print(df_whitelist_merchant)
            
            whitelist_merchant_array.append(df_whitelist_merchant)
            
            #get US rows from product_octo
            df_whitelist_product = df_product.loc[df_product["country_product_octo"] == country]
            #print(df_whitelist_product)
            
            whitelist_product_array.append(df_whitelist_product)
    
    #merge whitelist of merchant IDs
    df_whitelist_merchant_merged = reduce(lambda  left,right: pd.merge(left,
                                                    right,
                                                    how='outer'),
                                        whitelist_merchant_array)
    print(len(whitelist_merchant_array) , "merchant files merged to form whitelist.")

    #removes duplicate MerchantID
    df_whitelist_merchant_merged = df_whitelist_merchant_merged.drop_duplicates(subset=["MerchantID"],
                                                                                keep="first")

    #exports merchant whitelist as csv file
    df_whitelist_merchant_merged.to_csv(os.path.join(whitelist_PATH, 'MerchantID_whitelist.csv'),
                                            index=False)

    print(df_whitelist_merchant_merged)

    #merge whitelist of merchant IDs
    df_whitelist_product_merged = reduce(lambda  left,right: pd.merge(left,
                                                    right,
                                                    how='outer'),
                                        whitelist_product_array)
    print(len(whitelist_product_array) , "merchant files merged to form whitelist.")

    #removes duplicate Brand
    df_whitelist_product_merged = df_whitelist_product_merged.drop_duplicates(subset=["Brand"],
                                                                            keep="first")

    #exports Brand whitelist as csv file
    df_whitelist_product_merged.to_csv(os.path.join(whitelist_PATH, 'Brand_whitelist.csv'),
                                            index=False)


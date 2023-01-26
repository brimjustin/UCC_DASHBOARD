""" ETL Script """
import pandas as pd


class ETL:
    def __init__(self, default_file, df=None):
        self.default_file = default_file
        self.df = df

    def extract(self):
        # Extract Data
        self.df = pd.read_excel(self.default_file)
        return self.df

    def transform(self):
        # Remove unwanted columns
        self.df = self.df.drop(columns=["region", "Address Line 2", "Buyer ID", "Equipment New-Used",
                                        "Equipment Serial Number", "Secured Party Name",
                                        "UCC Date", "Assignee Company", "Assignee ID", "Country",
                                        "Buyer SIC Description", "Secured Party ID Ref", "uccnum",
                                        "Equipment Value", "Sub County", "Equipment Code", "Equipment Category",
                                        "Equipment Sub Category"])
        # Re-Name Columns
        self.df = self.df.rename(columns={"Company Name": "company_name", "Name": "customer_name",
                                          "DM Constant Key": "key", "Equipment Unit": "unit",
                                          "Equipment Manufacturer": "brand", "Equipment Model": "model",
                                          "Equipment Size": "size_code", "Equipment Description": "descr",
                                          "Equipment Size Description": 'equip_size_descr', "Address Line 1": "address",
                                          "City": "city", "County": "county", "State Code": "state", "Zip Code": "zip",
                                          "UCC Status": "sale/lease", "UCC ID": "group_sale"})

        # Remove rows with null models
        # self.df = self.df.dropna(axis=0)

        # Make fips in correct length
        self.df['fips'] = self.df['fips'].astype(str)

        def remove_fips_numbers(x):
            return x[4:-3]

        self.df['fips'] = self.df['fips'].apply(lambda x: remove_fips_numbers(x))

        # Remove Zip ending numbers
        self.df['zip'] = self.df['zip'].astype(str)

        def remove_zip_numbers(x):
            return x[:-4]

        self.df['zip'] = self.df['zip'].apply(lambda x: remove_zip_numbers(x))

        # Size Code to new HP column
        self.df['size_code'] = self.df['size_code'].astype(str)

        def size_category_to_hp(data, col):
            letter_map = {'A': 19, 'B': 20, 'C': 30, 'D': 40, 'E': 60, 'F': 70, 'G': 80,
                          'H': 90, 'I': 100, 'J': 110, 'K': 120, 'L': 130, 'M': 150,
                          'N': 160, 'O': 180, 'P': 220, 'Q': 230, 'R': 240, 'S': 0,
                          'T': 300, 'U': 320, 'V': 350, 'X': 0}
            self.df['hp'] = data[col].map(letter_map)
            self.df['hp'].fillna(0, inplace=True)
            self.df['hp'] = self.df['hp'].astype(int)
            return self.df

        self.df = size_category_to_hp(self.df, 'size_code')

        # Change HP to Correct Values
        def correct_hp_values(data, col):
            hp_values = {'1025R': 24, 'BX23S': 22, 'L2501': 25, 'B2601HSD': 24,
                         'BX2380': 22, 'L3901': 37, 'L3301': 33, 'WORKMASTER25S': 25,
                         'B2650HSD': 25, 'B2301HSD': 22, 'WORKMASTER25': 25,
                         'BX1880': 17, 'LX2610SUHSD': 25, 'LX2610HSD': 25, 'L3560': 37,
                         'CK2610HST': 25, 'MT125': 25, 'BX2680': 25, 'L2501HST': 25,
                         'WORKMASTER40': 40, 'L4701': 47, 'M7060': 71, 'XJ2025H': 24,
                         'GC1725MB': 25, 'CK3510HST': 35, 'L6060': 62, 'MX5200': 55,
                         'MT225S': 25, 'GC1723EB': 22, 'MX5400': 55, 'LX3310HSD': 30,
                         'MX6000': 63, '2515H': 25, 'WORKMASTER35': 35, 'GC1723E': 22,
                         'L3901HST': 37, 'CK3510SEHST': 35, 'CK3510SE': 35, '1023E': 22,
                         '1526HST': 25, '1526S': 25, '1533': 35, '1533HST': 35, '1533S': 35,
                         '1538HST': 38, '1538S': 38, '1626': 26, '1626HST': 26, '1626S': 26,
                         '1635HST': 36, '1635S': 36, '1640HST': 39, '1640S': 39, '2025R': 24,
                         '2032R': 30, '2038R': 37, '2205H': 22, '221': 22, '221AXH': 22,
                         '2400': 24, '2400H': 24, '2505H': 24, '2510': 25, '2510H': 25,
                         '2515R': 25, '2538HST': 37, '2545S': 45, '2555HST': 55, '2555S': 55,
                         '260': 260, '2610H': 24, '2638HST': 37, '2645S': 44, '2655': 55,
                         '2655HST': 55, '2655S': 55, '2660HST': 37, '2810': 29, '290': 290,
                         '3015H': 30, '3025D': 24, '3025E': 24, '3032E': 23, '3033R': 32,
                         '3035D': 34, '3038E': 37, '3039R': 38, '3043D': 42, '3046R': 45,
                         '310': 310, '315': 315, '324': 24, '324AXH': 24, '335': 335,
                         '3515C': 35, '3515CH': 35, '3515H': 35, '3520H': 35, '3540HST': 40,
                         '3550HST': 50, 'POWERSTAR120': 120, 'T4.120': 117, 'BOOMER45': 45,
                         'BOOMER55': 55, 'WORKMASTER75': 74, 'WORKMASTER70': 70, 'T4.75': 74,
                         'T4.110V': 106, 'T4.90V': 84, 'WORKMASTER50': 53, 'T4.80V': 74,
                         'T6.175': 145, 'T4.100V': 98, 'T4.100F': 98, 'POWERSTAR90': 86,
                         'BOOMER50': 50, 'WORKMASTER60': 60, 'TS6.130': 130, 'T5.120': 117,
                         'POWERSTAR75': 74, 'BOOMER24': 24, 'WORKMASTER33': 32, 'T6.165': '135',
                         'WORKMASTER37': 36, 'T4.110': 107, 'T1510': 30, 'T3.80F': 74,
                         'T4.65': 64, 'T4.110F': 106, '424AXH': 24, '424': 24, 'YT235': 34,
                         'YT359': 59, 'YM342': 41, 'SA424': 24, '424XHTTLD': 24, 'YT347': 46,
                         'YM359': 59, 'B26': 24}
            self.df['hp'] = self.df.apply(lambda x: hp_values.get(x['model'], x['hp']), axis=1)
            return self.df

        self.df = correct_hp_values(self.df, 'model')

        # Re-Index columns
        self.df = self.df.reindex(columns=['key', 'company_name', 'customer_name', 'unit', 'brand', 'model',
                                           'equip_size_descr', 'size_code', 'hp', 'group_sale', 'descr', 'address',
                                           'city', 'county', 'state', 'zip', 'fips', 'sale/lease'])

        # Add Lat/Long Coordinates from Zip
        lat_long_df = pd.read_csv('/Users/mac/Desktop/BRIM_DATA/data/zip-codes.csv')
        lat_long_df = lat_long_df.rename(columns={'ZIP': 'zip'})
        to_delete = range(0, 32289)
        lat_long_df = lat_long_df.drop(lat_long_df.index[to_delete])
        lat_long_df['zip'] = lat_long_df['zip'].astype(str)

        self.df['lat'] = None
        self.df['lon'] = None

        for index, row in self.df.iterrows():
            zip_code = row.loc['zip']
            match = lat_long_df[lat_long_df['zip'] == zip_code]
            lat = match['LAT'].iloc[0] if len(match) > 0 else None
            lon = match['LNG'].iloc[0] if len(match) > 0 else None
            lat_long_df.loc[index, 'lat'] = lat.astype(float) if lat is not None else lat
            lat_long_df.loc[index, 'lon'] = lon.astype(float) if lon is not None else lon
            self.df.at[index, 'lat'] = lat
            self.df.at[index, 'lon'] = lon

        self.df = self.df.dropna(subset=['lat', 'lon'], how='any')

        return self.df

    def load(self, filename):
        self.df.to_csv(path_or_buf=f"/Users/mac/Desktop/BRIM-DATA/UCC_DASHBOARD/data/{filename}.csv",
                       index=False)


# ETL Data
etl = ETL('/Users/mac/Desktop/BRIM-DATA/UCC_DASHBOARD/data/KBE UCC 5 Years.xlsx')
extract = etl.extract()
transform = etl.transform()
etl.load('KBE_Transformed_DF')

etl = ETL('/Users/mac/Desktop/BRIM-DATA/UCC_DASHBOARD/data/Brim UCC 5 Years.xlsx')
extract2 = etl.extract()
transform2 = etl.transform()
etl.load('Transformed_DF')

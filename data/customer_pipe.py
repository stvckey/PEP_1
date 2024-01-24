import pandas as pd
import yaml
import re

# loading data from demographics yaml file
with open('customer_demographics.yaml', 'r') as stream:
    data = yaml.safe_load(stream)

# each entry contains the same order and name for the keys
# creating a pandas df with the key:value pair of each entry as the column:value
demo_df = pd.DataFrame(data.values())

def reformat_phone_number(phone):
    if pd.isnull(phone) or phone is None or len(phone) < 10:
        return None
    # Extract digits from the phone number
    matches = re.findall(r'(\d*)', phone)
    all_digits = ''.join(matches)
    
    # Remove leading 1 if number starts with 1
    if all_digits.startswith('1') and len(all_digits) > 10:
        all_digits = all_digits[1:]
    
    # Remove leading 001 from numbers that start with 001
    if len(all_digits) > 10 and all_digits.startswith('0') and all_digits[2] == '1':
        all_digits = all_digits[3:]
    
    # add ext for exension after 10 digits of a phone number
    ext = ''
    if len(all_digits) > 10:
        ext = ' ext: ' + all_digits[10:]
        all_digits = all_digits[:10]
    
    # reformatting the phone number format
    formatted_number = '{}-{}-{}{}'.format(all_digits[:3], all_digits[3:6], all_digits[6:10], ext)
    return formatted_number

# Applying the reformatting function to the 'phone_number' column
demo_df['phone_number'] = demo_df['phone_number'].apply(reformat_phone_number)

# function to remove unecessary info from credit provider
def remove_numbers_and_digit(text):
    if pd.isnull(text) or text is None:
        return None
    return re.sub(r'\d+|\b[dD]igit\b', '', text).strip()


demo_df['credit_card_provider'] = demo_df['credit_card_provider'].apply(remove_numbers_and_digit)


demo_df['email'] = demo_df['email'].drop_duplicates(keep='first')


# Changing customer_id to demogrpahics ID and creating the customer ID's based on the index
demo_df.rename(columns={"customer_id":"customer_demographic_id"},inplace=True)
demo_df['customer_id'] = demo_df.index

demo_col_list = ['customer_demographic_id','customer_id', 'name', 'email',
                 'phone_number', 'address', 'city', 'state', 'zip_code',
                 'credit_card_number', 'credit_card_expires',
                 'credit_card_security_code', 'credit_card_provider']

demo_df.dropna(subset=['address','email','phone_number'],how='all',inplace=True)

demo_df = demo_df[demo_col_list]


# loading data from orders.csv
orders_df = pd.read_csv("./orders.csv", encoding="utf-8")


# creating customer statistics dataframe to be used as the customer_statistics table
customer_stats = orders_df[['customer_id','items','total']]

# aggregating customer statistics to show stats for each customer
customer_stats = orders_df.groupby('customer_id').agg(
    total_orders=('customer_id', 'size'),
    total_items=('items', 'sum'),
    total_spent=('total', 'sum')
).reset_index()

# merging our dataframes
customer_order_df = orders_df.merge(customer_stats, on="customer_id")
final_merge = customer_order_df.merge(demo_df, on='customer_id', how='left')

# exporting our dataframes to csv format
final_merge.to_csv('./cleaned_data/final_merge.csv',index=False)


demo_table = final_merge[demo_col_list].drop_duplicates(subset='customer_id')
demo_table.dropna(subset="customer_demographic_id",inplace=True)
demo_table.to_csv('./cleaned_data/customer_demo_final.csv',index=False)

customer_columns = customer_stats.columns
customer_table = final_merge.loc[:, final_merge.columns.isin(customer_columns)].drop_duplicates(subset='customer_id')
customer_table.dropna(subset="total_spent",inplace=True)
customer_table.to_csv('./cleaned_data/customer_stats_final.csv',index=False)

order_columns = orders_df.columns
orders_table = final_merge[order_columns]
orders_table.dropna(subset='order_id',inplace=True)
orders_table.to_csv('./cleaned_data/orders_final.csv',index=False)
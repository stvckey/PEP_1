import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, IntegrityError
import getpass
import sys

def main_menu():
    print("\nSelect an option:\n"
          + "1. View Statistics\n"
          + "2. Import data from CSV Files\n"
          + "3. Exit")
    
    menu_choice = get_input(1, 3)
    if menu_choice == 1:
        customer_statistics_df = pd.read_sql_table('customer_statistics', engine)
        customer_demographics_df = pd.read_sql_table('customer_demographics', engine)
        orders_df = pd.read_sql_table('orders', engine)

        statistics_menu(customer_statistics_df, customer_demographics_df, orders_df)
    elif menu_choice == 2:
        importRecords()
    else:
        sys.exit()





def statistics_menu(customer_statistics_df, customer_demographics_df, orders_df):
    while True:
        print("\nView Statistics for:\n"
            + "0. Go back to Main Menu\n"
            + "1. Customers\n"
            + "2. Orders")
        
        stat_menu_choice = get_input(0, 2)
        if stat_menu_choice == 1:
            get_customer_statistics(customer_statistics_df, customer_demographics_df)
        elif stat_menu_choice == 2:
            get_order_statistics(orders_df)
        else:
            print()
            break


def get_customer_statistics(stats_df, demo_df):
    total_customers = stats_df['customer_id'].nunique()
    total_orders = stats_df['total_orders'].sum()
    total_items = stats_df['total_items'].sum()
    total_spent = stats_df['total_spent'].sum()


    while True:
        print("\nSelect Statistic:\n"
                + "0. Go Back\n"
                + "1. Total Customers\n"
                + "2. Total Orders from all customers\n"
                + "3. Total Items bought from customers\n"
                + "4. Total Spent from all customers\n"
                + "5. All of the Above\n"
                + "6. Demographics")

        cust_stat_choice = get_input(0, 6)
        if cust_stat_choice == 1: 
            print(f'Total Customers: {total_customers}')
        elif cust_stat_choice == 2:
            print(f'Total Orders: {total_orders}')
        elif cust_stat_choice == 3:
            print(f'Total Items: {total_items}')
        elif cust_stat_choice == 4:
            print(f'Total Spent: ${total_spent}')
        elif cust_stat_choice == 5:
            print(f'Total Orders: {total_customers}')
            print(f'Total Orders: {total_orders}')
            print(f'Total Items: {total_items}')
            print(f'Total Spent: ${total_spent}')
        elif cust_stat_choice == 6:
            get_demographic_statistics(demo_df)
        else:
            break

def get_demographic_statistics(demographics_df):
    state_counts = demographics_df['state'].value_counts()
    most_common_credit_card_provider = demographics_df['credit_card_provider'].mode().values[0]
    unique_email_count = demographics_df['email'].nunique()
    city_distribution = demographics_df['city'].value_counts()
    most_orders = demographics_df["state"].value_counts().sort_values(ascending=False).head(10)

    while True:
        print("\nSelect Statistic:\n"
                + "0. Go Back\n"
                + "1. Count of each State in the Demographic\n"
                + "2. Most Common Credit card Providor\n"
                + "3. Count of Unique Emails\n"
                + "4. City Distribution\n"
                + "5. States with the most orders")

        order_stat_choice = get_input(0, 5)
        if order_stat_choice == 1: 
            print(f'State Counts:\n{state_counts}')
        elif order_stat_choice == 2:
            print(f'Most Common Credit Card Provider: {most_common_credit_card_provider}')
        elif order_stat_choice == 3: 
            print(f'# of Unique Emails: {unique_email_count}')
        elif order_stat_choice == 4: 
            print(f'City Distribution:\n{city_distribution}')
        elif order_stat_choice == 5: 
            print(f'States with the most orders:\n{most_orders}')
        else:
            print()
            break


def get_order_statistics(orders_df):
    total_orders_count = orders_df['order_id'].nunique()
    total_orders_amount = pd.to_numeric(orders_df['total']).sum()
    top_aperitifs = orders_df['aperitifs'].value_counts()
    top_appetizers = orders_df['appetizers'].value_counts()
    top_entrees = orders_df['entrees'].value_counts()
    top_desserts = orders_df['desserts'].value_counts()


    while True:
        print("\nSelect Statistic:\n"
                + "0. Go Back\n"
                + "1. Total Orders\n"
                + "2. Amount Made by All Orders\n"
                + "3. All of the Above\n"
                + "4. Top Aperitifs\n"
                + "5. Top Appetizers\n"
                + "6. Top Entrees\n"
                + "7. Top Desserts")
        

        order_stat_choice = get_input(0, 7)
        if order_stat_choice == 1: 
            print(f'Total Orders: {total_orders_count}')
        elif order_stat_choice == 2:
            print(f'Order Amount: ${total_orders_amount}')
        elif order_stat_choice == 3: 
            print(f'Total Orders: {total_orders_count}')
            print(f'Order Amount: ${total_orders_amount}')
        elif order_stat_choice == 4:
            print(top_aperitifs)
        elif order_stat_choice == 5:
            print(top_appetizers)
        elif order_stat_choice == 6:
            print(top_entrees)
        elif order_stat_choice == 7:
            print(top_desserts)
        else:
            print()
            break


def importRecords():
    print("Are you sure you want to import records into the restaurant database?: ")
    if get_confirmation():
        # List of tables
        tables = ['customer_statistics', 'orders', 'customer_demographics']

        try:
            for table in tables:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(f'{table}.csv')

                # Write the DataFrame to the SQL database
                df.to_sql(table, engine, if_exists='append', index=False)

            print('Records Imported.')
        except FileNotFoundError:
            print("Error: Make sure you have 'customer_demographics.csv', 'customer_statistics.csv', and 'orders.csv' at the root of the directory")
            sys.exit()
        except IntegrityError:
            print("Some of the data already exists within the database")
            sys.exit()

def get_input(start: int, end: int):
    choice = input()
    while not choice.isdigit() or not (start <= int(choice) <= end):
        choice = input("Not a valid choice. Pick a number from the list: ")

    return int(choice)

def get_confirmation():
    choice = input().upper()
    if choice in {"Y", "YES", "1"}:
        return True
    elif choice in {"N", "NO", "0"}:
        return False
    else:
        print("Type 'yes' or 'no', or simply 'Y' or 'N', or even '1' or '0'.")
        return get_confirmation()
    

if __name__ == "__main__":
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    # Check Server Config
    server_engine = create_engine(f'mysql://{username}:{password}@localhost/')
    try:
        server_engine.connect()
    except OperationalError:
        print("Check if Username/Password are right. Also check if your local MySQL server is running.")
        sys.exit()
    
    # Check Database
    engine = create_engine(f'mysql://{username}:{password}@localhost/restaurant')
    try:
        engine.connect()
    except OperationalError:
        print("'restaurant' database not detected")
        print("Creating 'restaurant' database...")
        with server_engine.connect() as connection:
            with open('restaurant_query.sql', 'r') as sql_file:
                sql_queries = sql_file.read()

            connection.execute(text(sql_queries))

    while True:
        main_menu()



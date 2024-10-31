
############### CREATING FOREIGN KEYS ################
# a script that adds a column address_id to users table
# and creates a foreign key constraint between the address_id column and the id column of the addresses table.

# THIS IS ONLY FOR CREATING A FOREIGN KEY CONSTRAINT FOR AN EXISTING TABLES

# IF YOU WANT TO CREATE A FOREIGN KEY CONSTRAINT FOR NEW TABLES, YOU CAN DEFINE IT IN models.py.


from sqlalchemy import inspect, Table, Column, Integer, String, MetaData
from database import engine

def run_migration():
    connection = engine.connect()
    inspector = inspect(engine)
    metadata = MetaData()
    metadata.bind = engine

    # Start a transaction
    trans = connection.begin()
    try:
        # Check if 'addresses' table exists
        if 'addresses' not in inspector.get_table_names():
            # Create 'addresses' table
            addresses_table = Table('addresses', metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('city', String),
                                    Column('street', String),
                                    Column('house_num', Integer)
                                    )
            addresses_table.create(engine)
            print("Created 'addresses' table.")
        else:
            print("'addresses' table already exists.")

        # Check if 'address_id' column exists in 'users' table
        users_columns = [column['name'] for column in inspector.get_columns('users')]
        if 'address_id' not in users_columns:
            # Add 'address_id' column to 'users' table
            connection.execute('ALTER TABLE users ADD COLUMN address_id INTEGER')
            print("Added 'address_id' column to 'users' table.")
        else:
            print("'address_id' column already exists in 'users' table.")

        # Check for existing foreign keys
        fkeys = inspector.get_foreign_keys('users')
        fk_exists = any(fk['constrained_columns'] == ['address_id'] for fk in fkeys)

        if not fk_exists:
            # Add foreign key constraint
            connection.execute('''
                ALTER TABLE users
                ADD CONSTRAINT fk_users_addresses
                FOREIGN KEY (address_id) REFERENCES addresses(id)
            ''')
            print("Added foreign key constraint between 'users.address_id' and 'addresses.id'.")
        else:
            print("Foreign key constraint already exists.")

        # Commit the transaction
        trans.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        trans.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    run_migration()




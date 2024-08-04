class Validation:
    def __init__(self, mydb):
        self.mydb = mydb
        self.mycursor = mydb.cursor()

    def check_table_exists(self):
        # Create cursor
        mycursor = self.mydb.cursor()

        # Check if the table exists
        if not self.table_exists(mycursor, "audio"):
            # Table doesn't exist, create it
            self.create_table(mycursor)
            print("Table 'audio' created successfully.")
        else:
            print("Table 'audio' already exists.")

    def table_exists(self,cursor, table_name):
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None

    def create_table(self,cursor):
        cursor.execute("""
            CREATE TABLE audio (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(255),
                content TEXT
            )
        """)
import sqlite3


class StoreEmail:
    __con = None

    def __init__(self):
        DB_NAME = 'email_storage.db'
        self.__con = sqlite3.connect(DB_NAME)

    """
    basic table layout
    email(id, sender (fk), receivers (fk), subject, text, from_this)
    email_address(id, local, domain)
    email_recipients(id, email_id (fk), email_address (fk))
    from_this is supposed to represent whether email is to or from a user's email address or elsewhere
    """
    def create_db(self):
        query = """
        CREATE TABLE address(
            local TEXT NOT NULL,
            domain TEXT NOT NULL,
            PRIMARY KEY(local, domain)
        )
        
        CREATE TABLE email(
            id INTEGER NOT NULL PRIMARY KEY,
            addr_local TEXT NOT NULL,
            addr_domain TEXT NOT NULL,
            subject TEXT,
            body TEXT NOT NULL,
            from_this BOOLEAN,
            FOREIGN KEY (addr_local, addr_domain)
                REFERENCES address (local, domain)
                    ON UPDATE CASCADE
        )
        
        CREATE TABLE recipient(
            email_id INTEGER NOT NULL,
            addr_local TEXT NOT NULL,
            addr_domain TEXT NOT NULL,
            FOREIGN KEY (addr_local, addr_domain)
                REFERENCES address (local, domain)
                    ON UPDATE CASCADE
            FOREIGN KEY (
        );
        """
        self.__execute(query)

    def store_emails(self, es: [Email]):
        base = "INSERT INTO "
        return None

    def load_emails(self):
        query = "SELECT * FROM email"
        return self.__execute(query, fetch=True)

    """Executes a query on the database"""
    def __execute(self, query, fetch=False):
        return self.__execute_with_con(query, self.__con, fetch)

    @staticmethod
    def __execute_with_con(queries, con, fetch=False):
        x = None
        c = con.cursor()
        for query in queries:
            c.execute(query)
        if fetch is True:
            x = c.fetchall()
        c.close()
        return x

    def close(self):
        self.__con.close()


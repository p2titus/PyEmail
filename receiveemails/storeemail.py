import sqlite3
from containers import *

class StoreEmail:
    __con = None

    def __init__(self):
        db_name = 'email_storage.db'
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
            PRIMARY KEY(id)
            FOREIGN KEY (addr_local, addr_domain)
                REFERENCES address (local, domain)
                    ON UPDATE CASCADE
        )
        
        CREATE TABLE recipient(
            email_id INTEGER NOT NULL,
            addr_local TEXT NOT NULL,
            addr_domain TEXT NOT NULL,
            PRIMARY KEY (email_id, addr_local, addr_domain)
            FOREIGN KEY (addr_local, addr_domain)
                REFERENCES address (local, domain)
                    ON UPDATE CASCADE
            FOREIGN KEY (email_id)
                REFERENCES email (id)
                    ON UPDATE CASCADE
        );
        """
        self.__execute(query)

    def store_emails(self, es: [Email]):
        address_insertions = self.__gen_addr_insertions(es)
        email_insertions = self.__gen_email_insertions(es)
        recipient_insertions = self.__gen_recipient_insertions(es)
        full_queries = address_insertions.append(email_insertions.append(recipient_insertions))
        self.__execute(full_queries)

    def __gen_addr_insertions(self, es: [Email], recurse=False):
        insertions = []
        for e in es:
            if recurse is False:
                a = e.sender
                x = self.__gen_addr_insertions(e.recipients, recurse=True)  # python has a slightly loose type system
                insertions.append(x)
            elif recurse is True:
                b, a = e
            insertion = "INSERT INTO address(?, ?)", (a.local, a.domain)
            insertions.append(insertion)

        return insertions

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


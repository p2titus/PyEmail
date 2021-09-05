import sqlite3
from containers import *

class StoreEmail:
    __con = None

    def __init__(self, db_name='email_storage.db'):
        self.__con = sqlite3.connect(db_name)

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

    @staticmethod
    def __gen_addr_insertions(es: [Email], recurse=False):
        insertions = []
        for e in es:
            if recurse is False:
                a = e.sender
                # recursive call deals with all recipients
                x = StoreEmail.__gen_addr_insertions(e.recipients, recurse=True)
                insertions.append(x)
            else:  # if recurse is True:
                b, a = e
            insertion = "INSERT INTO address(?, ?)", (a.local, a.domain)
            insertions.append(insertion)

        return insertions

    # basic idea outlined in __gen_addr_insertions - this implementation has less informative variable names
    @staticmethod
    def __gen_email_insertions(es: [Email]):
        acc = []

        for e in es:
            s = e.sender
            if e.from_this is True:
                ft = 1
            else:
                ft = 0
            x = "INSERT INTO email(?, ?, ?, ?, ?)", (s.local, s.domain, e.subject, e.body, ft)
            acc.append(x)

        return acc

    # TODO - this
    @staticmethod
    def __gen_recipient_insertions(es: [Email]):
        acc = []

        for e in es:
            pass

        return acc

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


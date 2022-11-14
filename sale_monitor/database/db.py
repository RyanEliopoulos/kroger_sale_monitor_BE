from typing import Tuple, List, Union

from flask import current_app, g
from flask.cli import with_appcontext
import sqlite3
import click


class DBInterface:
    """ Essentially static """

    @staticmethod
    def _execute_query(sql_string: str
                       , parameters: tuple = None
                       , selection: bool = False) -> Tuple[int, dict]:
        """ selection: returns cursor after executing query
        """
        db: sqlite3.Connection = DBInterface.get_db()
        cursor: sqlite3.Cursor = db.cursor()
        try:
            if parameters is None:
                cursor.execute(sql_string)
                db.commit()
            else:
                cursor.execute(sql_string, parameters)
                db.commit()
            if selection:
                return 0, {'cursor': cursor}
            else:
                return 0, {}
        except sqlite3.Error as e:
            return -1, {'error': str(e)}

    @staticmethod
    def close_db(e=None):
        """ Runs on teardown """
        db = g.pop('db', None)
        if db is not None:
            db.close()

    @staticmethod
    def get_db() -> sqlite3.Connection:
        """ If multiple db calls are made per request this will
            prevent opening multiple connections to the database

            Helper for all db functions
        """
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            # Activating foreign key constraint enforcement
            cursor: sqlite3.Cursor = g.db.cursor()
            cursor.execute('PRAGMA foreign_keys = 1')
            g.db.row_factory = sqlite3.Row
        return g.db

    @staticmethod
    def get_all() -> Union[None, Tuple[int, dict]]:
        """ Will pull out all of the info. Should return None if there is no contact entry? """
        print('in get_all')
        sqlstring: str = """ SELECT * 
                             FROM contact_details
                                  LEFT JOIN watched_products 
                                  ON contact_details.id = watched_products.contact_id 
                         """
        ret = DBInterface._execute_query(sqlstring, selection=True)
        if ret[0]:
            print(f'SQL error in get_all: {ret}')
            return ret
        crsr: sqlite3.Cursor = ret[1]['cursor']
        sqlrows: List[sqlite3.Row] = crsr.fetchall()
        if len(sqlrows) == 0:
            # No contact information exists
            print('get_all row length is zero. No contact information exists')
            return None
        print('Successfully pulled data in get_all. Packaging for consumption')
        data_dict: dict = {
            'id': sqlrows[0]['id'],
            'location_id': sqlrows[0]['location_id'],
            'chain': sqlrows[0]['chain'],
            'address1': sqlrows[0]['address1'],
            'city': sqlrows[0]['city'],
            'state': sqlrows[0]['state'],
            'zipcode': sqlrows[0]['zipcode'],
            'email':  sqlrows[0]['email'],
            'products': []
        }
        for row in sqlrows:
            product_dict: dict = {
                'upc': row['product_upc'],
                'target_price': row['target_price'],
                'last_discount_rate': row['last_discount_rate'],
            }
            data_dict['products'].append(product_dict)
        return 0, {'data': data_dict}

    @staticmethod
    def set_email(contact_id: int, email: str) -> Tuple[int, dict]:
        print('in DBInterface.set_email')
        sqlstring: str = """ UPDATE contact_details
                             SET email = ?
                             WHERE id = ?
                         """
        ret = DBInterface._execute_query(sqlstring, (email,
                                                     contact_id))
        if ret[0]:
            print(f'error executing SQL in DBI.set_email: {ret}')
            return ret
        print('Successfully set_email')
        return 0, {}

    @staticmethod
    def set_store(contact_id: int, location_id: str, chain: str
                  , address1: str, city: str, state: str, zipcode: str) -> Tuple[int, dict]:
        print('in DBInterface.set_store')
        sqlstring: str = """ UPDATE contact_details
                             SET location_id = ?,
                                 chain = ?,
                                 address1 = ?,
                                 city = ?,
                                 state = ?,
                                 zipcode = ?
                             WHERE id = ?
                         """
        ret = DBInterface._execute_query(sqlstring, (location_id,
                                                     chain,
                                                     address1,
                                                     city,
                                                     state,
                                                     zipcode,
                                                     contact_id))
        if ret[0]:
            print(f'Error executing SQL in set_store: {ret}')
            return ret
        print('success executing SQL in set_store')
        return 0, {}

    @staticmethod
    def new_watched(contact_id: int, upc: str, target_price: float) -> Tuple[int, dict]:
        """
          Needs to return the primary key of the new entry
        """
        print('in DBInterface.new_watched')
        sqlstring: str = """ INSERT INTO watched_products
                             VALUES (?, ?, ?)
                         """
        ret = DBInterface._execute_query(sqlstring,
                                         (contact_id,
                                          upc,
                                          target_price),
                                         selection=True)
        if ret[0]:
            print(f'SQL error in new_watched: {ret}')
            return ret
        crsr: sqlite3.Cursor = ret[1]['cursor']
        new_id: str = crsr.lastrowid
        print(f'SQL success in new_watched. primary key: {new_id}')
        return 0, {'new_watched_id': new_id}

    @staticmethod
    def delete_watched(target_id: int) -> Tuple[int, dict]:
        print('in DBInterface.delete_watched')
        sqlstring = """ DELETE FROM watched_products
                        WHERE id = ?
                    """
        ret = DBInterface._execute_query(sqlstring, (target_id,))
        if ret[0]:
            print(f'SQL error in DBinterface.delete_watched: {ret}')
            return ret
        print('SQL success in DBinterface.delete_watched')
        return 0, {}

    @staticmethod
    def update_watched(target_id: int, upc: str, target_price: float) -> Tuple[int, dict]:
        print('in DBinterface.update_watched')
        sqlstring = """ UPDATE watched_products
                        SET upc = ?,
                            target_price = ?,
                        WHERE id = ?
                    """
        ret = DBInterface._execute_query(sqlstring,
                                         (upc,
                                          target_price,
                                          target_id))
        if ret[0]:
            print(f'SQL error in DBInterface.update_watched: {ret}')
            return ret
        print('SQL success in update_watched')
        return 0, {}

# Auxiliary functions
def init_db():
    db = DBInterface.get_db()
    with current_app.open_resource('./database/schema.sql') as f:
        # Writing tables
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    # Establishes directives for the application to follow.
    app.teardown_appcontext(DBInterface.close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database')
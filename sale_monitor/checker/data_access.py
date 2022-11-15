import sqlite3
from typing import Tuple, List


def get_watch_data() -> List[dict]:
    """ Returns the groups of data necessary to evaluate the sale and
        update database entries belonging to multiple users.
    """
    connection: sqlite3.Connection = sqlite3.connect('../../instance/sale_monitor.sqlite',
                                                     detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    crsr: sqlite3.Cursor = connection.cursor()

    sqlstring = """ Select 
                        wp.watched_product_id
                        ,cd.email
                        ,cd.location_id
                        ,wp.product_upc
                        ,wp.product_description
                        ,wp.timestamp_last_checked
                        ,wp.target_price
                        ,wp.promo_price
                        ,wp.normal_price
                    FROM contact_details cd, watched_products wp
                    WHERE cd.email = wp.contact_email
                    GROUP BY wp.watched_product_id
                             ,cd.location_id
                             ,cd.email
                             ,wp.product_upc
                             ,wp.product_description
                """
    crsr.execute(sqlstring)
    results: List[sqlite3.Row] = crsr.fetchall()
    return_list: List = []
    for row in results:
        if row['product_upc'] is None:
            # Ignore 'accounts' with no watched products
            continue
        return_list.append(
            {'email': row['email'],
             'watched_product_id': row['watched_product_id'],
             'location_id': row['location_id'],
             'product_upc': row['product_upc'],
             'product_description': row['product_description'],
             'target_price': row['target_price'],
             'promo_price': row['promo_price'],
             'normal_price': row['normal_price'],
             'timestamp_last_checked': row['timestamp_last_checked']
             }
        )
    return return_list


def update_watched_data(data_dict):
    sqlstring: str = """ UPDATE watched_products
                         SET promo_price = ?,
                             normal_price = ?,
                             timestamp_last_checked = ?
                         WHERE watched_product_id = ?
                     """
    connection: sqlite3.Connection = sqlite3.connect('../../instance/sale_monitor.sqlite',
                                                     detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    crsr: sqlite3.Cursor = connection.cursor()
    crsr.execute(sqlstring, (data_dict['promo_price'],
                             data_dict['normal_price'],
                             data_dict['timestamp_last_checked'],
                             data_dict['watched_product_id']))
    connection.commit()

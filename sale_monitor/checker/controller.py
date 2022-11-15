"""
   Entry point for the scheduled price check
"""

import data_access
import log
import notifier
from decimal import Decimal
from datetime import datetime
from sale_monitor.kroger.Communicator import Communicator
from typing import List


def update_db(data_dicts: List[dict]):
    for dic in data_dicts:
        data_access.update_watched_data(dic)


def controller():
    data_dicts: List = data_access.get_watch_data()
    for dic in data_dicts:
        ret = Communicator.product_details(dic['product_upc'], dic['location_id'])
        if ret[0]:
            log.log(f"API call failure with details: {dic}\n {ret}")
        else:
            # Evaluate pricing difference and
            try:
                promo_price: Decimal = Decimal(ret[1]['data']['items'][0]['price']['promo']).quantize(Decimal('1.00'))
                normal_price: Decimal = Decimal(ret[1]['data']['items'][0]['price']['regular']).quantize(Decimal('1.00'))
            except KeyError as e:
                log.log(f'{ret[1]}')
                log.log(f"KeyError checking product {dic['product_description']}")
                continue
            target_price: Decimal = Decimal(dic['target_price']).quantize(Decimal('1.00'))  # Enforce 2 decimal places
            compare_at: Decimal
            if 0 < promo_price:  # 0 when there is no sale
                compare_at = promo_price
            else:
                compare_at = normal_price
                promo_price = normal_price
            print(f'Compare at: {compare_at}')
            if compare_at <= target_price:
                # A sale!
                price_diff: Decimal = normal_price - promo_price
                discount: Decimal = price_diff / normal_price
                scaled_discount: int = int((discount * 100).quantize(Decimal('1')))
                product_description: str = ret[1]['data']['description']
                msg: str = f"{product_description} is on sale at {scaled_discount}% off (${compare_at})."
                print(f"sending notifcation to {dic['email']} with message: {msg}")
                notifier.send_notification(dic['email'], msg)
            # Updating dicts with latest info
            dic['promo_price'] = str(promo_price)
            dic['normal_price'] = str(normal_price)
            dic['timestamp_last_checked'] = datetime.now().timestamp()

    update_db(data_dicts)


if __name__ == '__main__':
    controller()
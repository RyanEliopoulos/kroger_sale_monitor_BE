
def image_sizing(data):
    # Flattens a list of product info from Kroger
    # and prints the variety of image sizes contained therein

    size_set = set()
    print('in image_size')
    for product in data:
        # print(f'This is the product: {product}')
        for img in product['images']:
            # print(f'This is the img: {img}')
            for size_dict in img['sizes']:
                # print(f'This is the size: {size_dict}')
                size_set.add(size_dict['size'])
    print(size_set)
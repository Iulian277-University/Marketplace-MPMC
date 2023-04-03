"""
This module represents the Cart.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

class Cart:
    """
    Class that represents a shopping cart. It's used by the consumers.
    """

    def __init__(self):
        """
        Constructor
        """
        self.products = []

    def add_product(self, product, producer_id):
        """
        Adds a product to the shopping cart.

        :type product: String
        :param product: the name of the product

        :type producer_id: Int
        :param producer_id: the ID of the producer that added the product

        """
        self.products.append({
            "product": product,
            "producer_id": producer_id
        })

    def remove_product(self, product):
        """
        Removes a product from the shopping cart.
        Returns the ID of the producer that added the product
        or -1 if the product is not in the cart.

        :type product: String
        :param product: the name of the product

        :rtype: Int
        :return: the ID of the producer that added the product
        """
        for item in self.products:
            if item['product'] == product:
                self.products.remove(item)
                return item['producer_id']

        return -1

    def get_products(self):
        """
        Returns the list of products in the shopping cart.

        :rtype: List
        :return: the list of products in the shopping cart
        """
        return [item['product'] for item in self.products]

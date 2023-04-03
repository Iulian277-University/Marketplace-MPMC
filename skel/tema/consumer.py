"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts # List of operations to perform on the cart
        self.marketplace = marketplace # Marketplace reference
        self.retry_wait_time = retry_wait_time # Time to wait before retrying an operation
        self.name = kwargs['name'] # Consumer name

    def run(self):
        for cart in self.carts:
            # Create a new `cart_id`
            cart_id = self.marketplace.new_cart()

            # Add/Remove products to/from the cart
            for op in cart:
                # Unpack the operation in `type_`, `product` and `quantity`
                type_, product, quantity = op.values()

                # Perform the operation `quantity` times
                for _ in range(quantity):
                    if type_ == 'add':
                        # Wait until the Marketplace signals that the `Consumer` can add to cart
                        while not self.marketplace.add_to_cart(cart_id, product):
                            sleep(self.retry_wait_time)
                    elif type_ == 'remove':
                        self.marketplace.remove_from_cart(cart_id, product)

            # After all operations are performed, the `Consumer` checks out
            products = self.marketplace.place_order(cart_id)

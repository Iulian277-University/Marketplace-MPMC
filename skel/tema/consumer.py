"""
This module represents the Consumer.
"""

from threading import Thread, Lock
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
        self.print_lock = Lock() # Lock for thread safe printing

    def run(self):
        def perform_op(operation):
            """
            Perform an operation on the cart.

            :type op: Dict
            :param op: the operation to perform

            :rtype: None
            """
            # Unpack the operation in `type_`, `product` and `quantity`
            type_, product, quantity = operation.values()

            # Perform the operation `quantity` times
            for _ in range(quantity):
                if type_ == 'add':
                    # Wait until the Marketplace signals that the `Consumer` can add to cart
                    while not self.marketplace.add_to_cart(cart_id, product):
                        sleep(self.retry_wait_time)
                elif type_ == 'remove':
                    self.marketplace.remove_from_cart(cart_id, product)

        for cart in self.carts:
            # Create a new `cart_id`
            cart_id = self.marketplace.new_cart()

            # Perform all operations on the cart
            _ = [perform_op(op) for op in cart]

            # After all operations are performed, the `Consumer` checks out
            products = self.marketplace.place_order(cart_id)

            # Print the products in the cart
            for product in products:
                with self.print_lock:
                    print(f'{self.name} bought {product}', flush=True)

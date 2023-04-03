"""
This module represents the Producer.
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        :type products: List()
        :param products: a list of products that the producer will produce

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type republish_wait_time: Time
        :param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products # List of products to produce
        self.marketplace = marketplace # Marketplace reference
        self.republish_wait_time = republish_wait_time # Time to wait before republishing
        self.producer_id = marketplace.register_producer() # Producer ID

    def run(self):
        while True:
            for product, quantity, wait_time in self.products:
                # Wait `wait_time` seconds before producing the next product
                sleep(wait_time)

                # Wait until the marketplace signals that the `Producer` can publish
                _ = [sleep(self.republish_wait_time) for _ in range(quantity) \
                        if not self.marketplace.publish(self.producer_id, product)]

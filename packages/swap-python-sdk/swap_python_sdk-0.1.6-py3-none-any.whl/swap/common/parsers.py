import json
from swap.common.logging import logger
from swap.common.schemas import ServiceDiscoveryResponseSchema
from swap.common.filters import ServiceDiscoveryResponseFilter


class Parser:
    def apply_pre_processing(self, response):
        try:
            pre_processed_response = json.loads(response)
        except json.JSONDecodeError as e:
            logger.info(f'One of the responses we got back from SWAP couldnt be parsed')
            logger.info(f'The response we tried to load is as follows:')
            logger.info(response)
            return 'JSONDecodeError'

        return pre_processed_response

    def apply_filters(self, response):
        return self.filter.apply(response)

    def parse(self, response):
        preprocessed_response = self.apply_pre_processing(response)

        if preprocessed_response == 'JSONDecodeError':
            return 'JSONDecodeError'

        filtered_response = self.apply_filters(preprocessed_response)

        return self.schema.load(filtered_response)


class ServiceDiscoveryResponseParser(Parser):
    def __init__(self):
        self.filter = ServiceDiscoveryResponseFilter()
        self.schema = ServiceDiscoveryResponseSchema()

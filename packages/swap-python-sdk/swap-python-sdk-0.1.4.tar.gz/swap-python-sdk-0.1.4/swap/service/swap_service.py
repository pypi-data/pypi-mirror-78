from swap.messaging.listeners import MessageListener
from swap.messaging import (
    ExecutionStatusUpdateMessage, ExecutionCompletionMessage, ExecutionFailureMessage
)
from swap.messaging.clients import DASClient
import json
from swap.service.datasets import GCSDataset, CDFDataset

class SwapService:

    def __init__(self, service_config):
        self.service_config = service_config

    def send_execution_status_update(self, details='', code='0', text='Execution update'):
        print('Sending execution status update')
        execution_status_update = ExecutionStatusUpdateMessage(
            message_id=self.message_id,
            config=self.service_config,
            offer_execution_request=self.offer_execution_request,
            execution_details=details,
            exec_status_code=code,
            exec_status_text=text
        )

        execution_status_update.publish()

    def send_execution_completion(self, code='0', text='Execution complete', output_id='placeholder_id'):
        print('Sending execution completion')

        if output_id is not 'placeholder_id':
            self.set_output_id(output_id)

        execution_completion = ExecutionCompletionMessage(
            message_id=self.message_id,
            config=self.service_config,
            offer_execution_request=self.offer_execution_request,
            output_data_id = self.output_file_uri,
            exec_comp_code=code,
            exec_comp_text=text
        )

        execution_completion.publish()

    def send_execution_failure(self, code='0', text='Execution failed'):
        print('Sending execution failure update')

        execution_failure_message = ExecutionFailureMessage(
            message_id=self.message_id,
            config=self.service_config,
            offer_execution_request=self.offer_execution_request,
            exec_fail_code=code,
            exec_fail_text=text
        )

        execution_failure_message.publish()

    def _load_parsed_tokens(self):
        parsed_tokens = []
        for dataset in self.offer_execution_request.input_data:
            token = dataset.data_token
            client = DASClient()
            redeemed_token = client.redeem_token(token=token)
            parsed_token = json.loads(redeemed_token)
            parsed_tokens.append(parsed_token['links'][0])
        return parsed_tokens

    def _load_storage_types(self):
        storage_types = []
        for parsed_token in self.parsed_tokens:
            storage_types.append(parsed_token['connectionDetails']['storageType'])
        return storage_types

    def _load_gcp_data_parameters(self, parsed_token):
        name = parsed_token['metadata']['dataName']
        url = parsed_token['connectionDetails']['dataUrl']
        size = parsed_token['metadata']['dataSize']

        custom_metadata = ""
        try:
            metadata_ready_for_json = parsed_token['metadata']['customMetadata'].replace("'", '"')
            custom_metadata = json.loads(metadata_ready_for_json)
        except:
            print(f'Service tried to load custom metadata provided by user into dict but failed. Custom metadata:{parsed_token["metadata"]["customMetadata"]}')
            pass

        return GCSDataset(name=name, url=url, size=size, custom_metadata=custom_metadata)

    def _load_cdf_data_parameters(self, parsed_token):
        id = parsed_token['connectionDetails']['storageId']
        crs = ''
        survey_id = ''

        try:
            for item in parsed_token['metadata']['customMetadata']:
                if item['metadataKey'] == 'crs':
                    crs = item['metadataValue']

                if item['metadataKey'] == 'survey_id':
                    survey_id = item['metadataValue']
        except:
            pass

        custom_metadata = ""
        try:
            metadata_ready_for_json = parsed_token['metadata']['customMetadata'].replace("'", '"')
            custom_metadata = json.loads(metadata_ready_for_json)
        except:
            print(f'Service tried to load custom metadata provided by user into dict but failed. Custom metadata:{parsed_token["metadata"]["customMetadata"]}')
            pass

        return CDFDataset(id=id, crs=crs, survey_id=survey_id, custom_metadata=custom_metadata)

    def _load_data_parameters(self):
        self.data_details = []

        for parsed_token in self.parsed_tokens:
            if parsed_token['connectionDetails']['storageType'] == 'GCP':
                self.data_details.append(self._load_gcp_data_parameters(parsed_token))
            if parsed_token['connectionDetails']['storageType'] == 'CDF':
                self.data_details.append(self._load_cdf_data_parameters(parsed_token))

    def _load_output_file_uri(self):
        return self.offer_execution_request.output_data.file_uri

    def set_output_id(self, output_id):
        self.output_file_uri = output_id

    def start(self):
        print(f'Started service {self.service_config.name}')

        listener = MessageListener(config=self.service_config)
        listener.handler.register_callback(message_type='OfferExecutionRequest', callback=self)
        listener.listen()

    def call(self, message_id, offer_execution_request, parameters):

        if parameters is list:
            for unwanted_param in ['description_text']:
                del parameters[unwanted_param]

        self.message_id = message_id
        self.offer_execution_request = offer_execution_request
        self.parameters = parameters

        self.parsed_tokens = self._load_parsed_tokens()

        self.storage_types = self._load_storage_types()

        self.output_file_uri = self._load_output_file_uri()

        self._load_data_parameters()

        self.execute()

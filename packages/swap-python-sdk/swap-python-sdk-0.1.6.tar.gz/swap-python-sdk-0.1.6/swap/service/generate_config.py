#!/usr/bin/env python
from jinja2 import Template
from os import path
from uuid import uuid4
import webbrowser
import requests
import json
from swap.common.config import Settings

config_template = """from swap.messaging.models import Config
from service.parameters import parameters

service_config = Config(
    project='{{ project }}',
    topic='{{ topic }}',
    subscription='{{ subscription }}',
    catalogue_uuid='{{ catalogue_uuid }}',
    dataset_type='{{ dataset_type }}',
    name='{{ name }}',
    service_description='{{ service_description }}',
    service_provider_name='{{ service_provider_name }}',
    service_provider_signature='{{ service_provider_signature }}',
    service_provider_uuid='{{ service_provider_uuid }}',
    icon_base64='{{ icon_base64 }}',
    icon_url='{{ icon_url }}',
    parameters=parameters
)"""


class ConfigGenerator:
    def __init__(self, config_output_path, parameters):
        self.template = Template('')
        self.config_output_path = config_output_path
        self.parameters = parameters
        self.swap_api_token= Settings.SWAP_API_TOKEN
        self.template = Template(config_template)

    def generate_subscription(self):
        # Call UBL to generate pub/sub subscription
        subscription_generation_url = 'https://ubl.stage.baringa-pharos.com/template_app/subscription'
        response = requests.get(subscription_generation_url,
                                params={
                                    "api_key": self.swap_api_token
                                })

        response_as_dict = json.loads(response.text)
        new_subscription_id = response_as_dict['subscription_id']

        return new_subscription_id

    def render(self, subscription):
        name = input('Enter a name for your service: ')
        name = name + '_dev'
        description = input('Enter a description for your service: ')

        return self.template.render(
            project='microservice-pilot',
            topic='akerbp-stage-pre-seismic-processing',
            subscription=subscription,
            catalogue_uuid=uuid4(),
            dataset_type='SEGY',
            name=name,
            service_description=description,
            service_provider_name='AkerBP',
            service_provider_signature=uuid4(),
            service_provider_uuid=uuid4(),
            icon_base64='ICON_BASE64',
            icon_url='https://ui.dev.baringa-pharos.com/static/media/Skua-salt-2010.4fa0f606.jpg',
            parameters='self.parameters'
        )

    def write(self, data):
        with open(self.config_output_path, 'w') as file:
            file.write(data)

    def generate(self):
        subscription = self.generate_subscription()
        data = self.render(subscription)
        self.write(data)

        print(f'A new service config has been successfully written to {path.abspath(self.config_output_path)}')

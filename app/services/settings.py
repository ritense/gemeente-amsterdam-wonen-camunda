import os

OPEN_ZAAK = 'openzaak'

DOMAIN_CATALOGS = 'catalogi'
SUB_DOMAIN_CATALOGS = 'catalogussen'
SUB_DOMAIN_CASE_TYPES = 'zaaktypen'
SUB_DOMAIN_STATE_TYPES = 'statustypen'
SUB_DOMAINS_CATALOGS = [SUB_DOMAIN_CATALOGS, SUB_DOMAIN_CASE_TYPES, SUB_DOMAIN_STATE_TYPES]

DOMAIN_CASES = 'zaken'
SUB_DOMAIN_CASES = 'zaken'
SUB_DOMAIN_STATES = 'statussen'
SUB_DOMAINS_CASES = [SUB_DOMAIN_CASES, SUB_DOMAIN_CASES]

STATES = [
    'Issuemelding',
    'Onderzoek buitendienst',
    '2de Controle',
    '3de Controle',
    'Hercontrole',
    '2de hercontrole',
    '3de hercontrole',
    'Avondronde',
    'Onderzoek advertentie',
    'Weekend buitendienstonderzoek',
]

ORGANISATION_RSIN = '221222558' # Just a randomly generated id for now (https://www.testnummers.nl/)
CONNECTIONS = {
    OPEN_ZAAK:  {
            'host': os.environ['OPEN_ZAAK_CONTAINER_NAME'],
            'port': os.environ['OPEN_ZAAK_PORT'],
            'api_version': os.environ['OPEN_ZAAK_API_VERSION'],
            'client': os.environ['OPEN_ZAAK_CLIENT'],
            'secret_key': os.environ['OPEN_ZAAK_SECRET_KEY']
        }
}

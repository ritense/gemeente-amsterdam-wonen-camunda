from services.service import create_service
from services.settings import OPEN_ZAAK, DOMAIN_CATALOGS, SUB_DOMAINS_CATALOGS, SUB_DOMAIN_CASE_TYPES

service = create_service(OPEN_ZAAK, DOMAIN_CATALOGS, SUB_DOMAINS_CATALOGS)

def get_case_types():
    return service.get(SUB_DOMAIN_CASE_TYPES)

def create_case_type(catalog_uri):
    data = {
        "omschrijving": "Illegale vakantieverhuur",
        "vertrouwelijkheidaanduiding": "vertrouwelijk",
        "doel": "Toezicht en handhaving van illegale vakantieverhuur",
        "aanleiding": "Melding of onderzoek",
        "indicatieInternOfExtern": "extern",
        "handelingInitiator": "indienen",
        "onderwerp": "Vakantieverhuur",
        "handelingBehandelaar": "behandelen",
        "doorlooptijd": "P1M",
        "opschortingEnAanhoudingMogelijk": True,
        "verlengingMogelijk": False,
        "publicatieIndicatie": True,
        "productenOfDiensten": [],
        "referentieproces": {
            "naam": "Nog geen naam"
        },
        "catalogus": catalog_uri,
        "besluittypen": [],
        "gerelateerdeZaaktypen": [],
        "beginGeldigheid": "2020-05-28",
        "versiedatum": "2020-05-28"
    }

    case_type = service.post(SUB_DOMAIN_CASE_TYPES, data)
    return case_type

def publish_case_type(uri):
    case_type = service.publish(uri)
    return case_type

def delete_case_type(uri):
    response = service.delete(uri)
    return response
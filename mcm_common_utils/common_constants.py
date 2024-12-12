from enum import Enum


# Enums
class Microservice(Enum):
    RESULTS_AGGREGATION_SERVICE = 0
    QUERY_PROCESSING_SERVICE = 1
    CONTENT_GENERATION_SERVICE = 2
    USER_DATA_SERVICE = 3
    LINGO4G_SERVICE = 10
    # NEO4J_SERVICE = 11
    # ELASTIC_SEARCH_SERVICE = 12


class ServiceStatusEnum(Enum):
    OK = 'OK'
    NOT_OK = 'NOT_OK'
    ERROR = 'ERROR'


# Constants
# TODO some of below constants needs to be loaded via environment variables of the container
AWS_REGION_DEFAULT = "ap-southeast-2"

SECRETS_MANAGER_ENDPOINT_URL = {
    'dev': 'https://vpce-04aad738a6fce4f60-qqvbm5am.secretsmanager.ap-southeast-2.vpce.amazonaws.com',
    'uat': 'https://vpce-020d1ce0b2ceb958f-huug2nqu.secretsmanager.ap-southeast-2.vpce.amazonaws.com',
    'prod': ''
}

service_discovery_map = {
    Microservice.RESULTS_AGGREGATION_SERVICE: "http://results-aggregation-service:8080/",
    Microservice.QUERY_PROCESSING_SERVICE: "http://query-processing-service:8080/",
    Microservice.CONTENT_GENERATION_SERVICE: "http://content-generation-service:8080/",
    Microservice.USER_DATA_SERVICE: "http://user-data-service:8080/",
    Microservice.LINGO4G_SERVICE: "http://lingo4g-service:8080/",
}

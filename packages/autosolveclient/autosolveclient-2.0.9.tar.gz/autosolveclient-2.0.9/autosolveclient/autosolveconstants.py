class AutoSolveConstants:
    #NAMES
    HOSTNAME = "amqp.autosolve.aycd.io"
    VHOST = "oneclick"
    DIRECT_EXCHANGE = "exchanges.direct"
    FANOUT_EXCHANGE = "exchanges.fanout"
    RECEIVER_QUEUE_NAME = "queues.response.direct"
    MAX_ATTEMPTS = 50
    RETRY_DELAY = 0
    MAX_DELAY = 30
    SEQUENCE = [0, 2, 3, 5, 8, 13, 21, 34]


    #ROUTES
    TOKEN_SEND_ROUTE = "routes.request.token"
    CANCEL_SEND_ROUTE = "routes.request.token.cancel"
    TOKEN_RECEIVE_ROUTE = "routes.response.token"
    CANCEL_RECEIVE_ROUTE = "routes.response.token.cancel"

    #CONFIG
    AUTO_DELETE = False
    DURABLE = True
    AUTO_ACK = True
    EXCLUSIVE = False

    #EVENTS
    ERROR_EVENT = "AutoSolveError"
    RESPONSE_EVENT = "AutoSolveResponse"
    CANCEL_RESPONSE_EVENT = "AutoSolveResponse_Cancel"

    #ERRORS
    INVALID_CLIENT_KEY = "Invalid Client Key"
    INVALID_API_KEY_OR_ACCESS_TOKEN = "Invalid API or Access Key"
    TOO_MANY_REQUESTS = "Too many validation requests have been made. Cooling down"
    INPUT_VALUE_ERROR = "Input value for access_token is invalid or client_key/api_key are not set"
    INIT_ERROR = "Error initializing client."

    #STATUS
    SUCCESS = "info"
    WARNING = "warning"
    ERROR = "error"
    STATUS = "status"
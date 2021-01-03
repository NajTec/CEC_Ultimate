export IOTHUB_EVENTHUB_NAME="myhsiothub"

# see: Endpoints ⇒ Messaging ⇒ Events ⇒ "Event Hub-compatible endpoint"
export IOTHUB_EVENTHUB_ENDPOINT="Endpoint=sb://iothub-ns-myhsiothub-6934845-d4046aff22.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=NgeR8a3GhdeBBWVeEYpUyG4irVlv3bimOkqxYFY0BzE=;EntityPath=myhsiothub"

# see: Endpoints ⇒ Messaging ⇒ Events ⇒ Partitions
export IOTHUB_EVENTHUB_PARTITIONS="4"

# see: Shared access policies, we suggest to use "service" here
export IOTHUB_ACCESS_POLICY="iothubowner"

# see: Shared access policies ⇒ key name ⇒ Primary key
export IOTHUB_ACCESS_KEY="NgeR8a3GhdeBBWVeEYpUyG4irVlv3bimOkqxYFY0BzE="
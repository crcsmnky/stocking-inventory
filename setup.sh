#!/bin/bash

# # create bucket
# gsutil mb gs://stocking-inventory

# # create pubsub topics
# gcloud pubsub topics create inventory
# gcloud pubsub topics create messaging

# # setup pubsub push subscriptions
# gcloud pubsub subscriptions create inventory-push \
# --topic inventory \
# --push-endpoint https://inventory-dot-sndp-next.appspot.com/process-inventory?token=ec121ff80513ae58ed478d5c5787075b \
# --ack-deadline 10

# gcloud pubsub subscriptions create messaging-push \
# --topic messaging \
# --push-endpoint https://messaging-dot-sndp-next.appspot.com/process-message?token=ec121ff80513ae58ed478d5c5787075b \
# --ack-deadline 10

# # setup bucket change notifications
# gsutil notifications create -f json -e OBJECT_FINALIZE -t inventory gs://stocking-inventory

# # teardown

set -e

BUCKET_NAME=stocking-inventory
INVENTORY=inventory
MESSAGING=messaging
INVENTORY_ENDPOINT=https://inventory-dot-sndp-next.appspot.com/process-inventory
MESSAGING_ENDPOINT=https://messaging-dot-sndp-next.appspot.com/process-message
PUBSUB_TOKEN=ec121ff80513ae58ed478d5c5787075b

TYPE=${1}
COMMAND=${2}

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

function usage
{
    echo "$ setup.sh [bucket|topics|subscriptions|changes|all] [up|down]"
}

function bucket
{
    if [[ ${COMMAND} -eq "up" ]]; then
        gsutil mb 'gs://${BUCKET_NAME}'

    elif [[ ${COMMAND} -eq "down" ]]; then
        gsutil rb 'gs://${BUCKET_NAME}'
    fi
}

function topics
{
    if [[ ${COMMAND} -eq "up" ]]; then
        gcloud pubsub topics create ${INVENTORY}
        gcloud pubsub topics create ${MESSAGING}
    
    elif [[ ${COMMAND} -eq "down" ]]; then
        gcloud pubsub topics delete ${INVENTORY}
        gcloud pubsub topics delete ${MESSAGING}
    fi    
}

function subscriptions
{
    if [[ ${COMMAND} -eq "up" ]]; then
        gcloud pubsub subscriptions create ${INVENTORY}-push \
        --topic ${INVENTORY} \
        --push-endpoint ${INVENTORY_ENDPOINT}?token=${PUBSUB_TOKEN} \
        --ack-deadline 10

        gcloud pubsub subscriptions create ${MESSAGING}-push \
        --topic ${MESSAGING} \
        --push-endpoint ${MESSAGING_ENDPOINT}?token=${PUBSUB_TOKEN} \
        --ack-deadline 10

    elif [[ ${COMMAND} -eq "down" ]]; then
        gcloud pubsub subscriptions delete ${INVENTORY}-push
        gcloud pubsub subscriptions delete ${MESSAGING}-push
    fi
}

function changes
{
    if [[ ${COMMAND} -eq "up" ]]; then
        gsutil notifications create -f json -e OBJECT_FINALIZE -t ${INVENTORY} gs://${BUCKET_NAME}

    elif [[ ${COMMAND} -eq "down" ]]; then
        gsutil notifications delete gs://${BUCKET_NAME}
    fi
}

function all
{
    bucket
    topics
    subscriptions
    changes
}

if [[ -z $@ ]]; then
    usage
    exit 0
fi

case "$TYPE" in
    bucket )
        bucket
        ;;
    topics )
        topics
        ;;
    subscriptions )
        subscriptions
        ;;
    changes )
        changes
        ;;
    all )
        all
        ;;
    * )
        usage
        ;;
esac

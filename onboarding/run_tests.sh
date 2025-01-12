#!/bin/bash
set -e

ARGS=$*
FILTER_PROVISION_SCENARIO="host"

# ..:: Params ::..
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -kp|--KeyPairName) AWS_KEY_PAIR_NAME="$2"; shift ;;
        -sn|--subnet) AWS_SUBNET="$2"; shift ;;
        -vpc|--vpc) AWS_VPC="$2"; shift ;;
        -s|--dd-site) DD_SITE="$2"; shift ;;
        -pk|--private-key-path) AWS_PRIVATE_KEY_PATH="$2"; shift ;;
        -it|--instance-type) AWS_INSTANCE_TYPE="$2"; shift ;;
        -fl|--filter-language) FILTER_LANGUAGE="$2"; shift ;;
        -fe|--filter-env) FILTER_ENV="$2"; shift ;;
        -fod|--filter-os-distro) FILTER_OS_DISTRO="$2"; shift ;;
        -fw|--filter-weblog) FILTER_WEBLOG="$2"; shift ;;
        -fp|--filter-provision-scenario) FILTER_PROVISION_SCENARIO="$2"; shift ;;
        *) cat USAGE.md; exit 8 ;;
    esac
    shift
done

#Parameters validation. Custom exit code for parameter validation.
[[ -z "$AWS_KEY_PAIR_NAME" ]] && echo "--KeyPairName parameter is mandatory." && cat USAGE.md && exit 8
[[ -z "$AWS_SUBNET" ]] && echo "--subnet parameter is mandatory." && cat USAGE.md && exit 8
[[ -z "$AWS_VPC" ]] && echo "--vpc parameter is mandatory." && cat USAGE.md && exit 8
[[ -z "$AWS_PRIVATE_KEY_PATH" ]] && echo "--private-key-path parameter is mandatory." && cat USAGE.md && exit 8
[[ -z "$AWS_INSTANCE_TYPE" ]] && echo "--instance-type parameter is mandatory." && cat USAGE.md && exit 8
[[ -z "$FILTER_PROVISION_SCENARIO" ]] && echo "--filter-provision-scenarioparameter is mandatory." && cat USAGE.md && exit 8


SUPPORTED_LANGUAGES="java nodejs dotnet python"
[[ (! -z "$FILTER_LANGUAGE") && (! $SUPPORTED_LANGUAGES =~ (^|[[:space:]])$FILTER_LANGUAGE($|[[:space:]])) ]] && echo "Bad param --filter-language. Supported languages are: $SUPPORTED_LANGUAGES" && exit 8


# .:: Launch infraestructure ::.

aws-vault exec sandbox-account-admin -- pulumi up --yes \
    -c ddinfra:aws/defaultKeyPairName=$AWS_KEY_PAIR_NAME \
    -c ddinfra:aws/subnet_id=$AWS_SUBNET \
    -c ddinfra:aws/vpc_security_group_ids=$AWS_VPC \
    -c ddagent:site=$DD_SITE \
    -c ddinfra:aws/defaultPrivateKeyPath=$AWS_PRIVATE_KEY_PATH \
    -c ddinfra:aws/instance_type=$AWS_INSTANCE_TYPE \
    -c ddfilter:language=$FILTER_LANGUAGE \
    -c ddfilter:env=$FILTER_ENV \
    -c ddfilter:os_distro=$FILTER_OS_DISTRO \
    -c ddfilter:weblog=$FILTER_WEBLOG \
    -c ddfilter:provision_scenario=$FILTER_PROVISION_SCENARIO \
    -C . -s dev
#For Verbose add those params to pulumi up:--logtostderr --logflow -v=9

echo "Export private IPs "
pulumi stack output --json > pulumi.output.json 

# .:: Launch tests ::.

export DD_APP_KEY=$(pulumi config get ddagent:appKey)
export DD_API_KEY=$(pulumi config get ddagent:apiKey)

PARENT_DIR=$(dirname $PWD)
pytest -s -c $PWD/conftest.py tests/installation/* --json-report
###venv/bin/python -m pytest -s -c $PWD/conftest.py $ARGS

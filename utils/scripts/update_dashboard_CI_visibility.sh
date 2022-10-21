if [ "$#" -ne 2 ] ; then
  echo "Script execution requires 2 parameters: Pipeline id and dashboard variable name" 
  exit 1
fi
SYS_PIPELINE_RUN_ID=$1
DASHBOARD_VARIABLE_NAME=$2

echo "PIPELINE RUN ID $SYS_PIPELINE_RUN_ID"

# Path parameters
export dashboard_id="zqg-kqn-2mc"

export dashboard_json=$(
curl -X GET "https://api.datadoghq.com/api/v1/dashboard/${dashboard_id}" \
-H "Accept: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}")

#Search in all template variables (no more than 4) trying to find DASHBOARD_VARIABLE_NAME pass as parameter
#When I achieve to find the variable, I will change the default value with the last pipelineId + run attemp number 
for counter in 0 1 2 3  
do
    dashboard_json_variable=$(jq -r ".template_variables[$counter].prefix"  <<< "$dashboard_json")
    echo "-> $dashboard_json_variable"
    if [ "$dashboard_json_variable" = "$DASHBOARD_VARIABLE_NAME" ]; then
        echo "Updating dashboard variable: $DASHBOARD_VARIABLE_NAME "
        export dashboard_json_updated=$(jq -r ".template_variables[${counter}].default = \"$SYS_PIPELINE_RUN_ID\""  <<< "$dashboard_json")
        break
    fi
done

curl -X PUT "https://api.datadoghq.com/api/v1/dashboard/${dashboard_id}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
$dashboard_json_updated
EOF
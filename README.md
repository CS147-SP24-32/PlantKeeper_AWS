# PlantKeeper
To deploy the AWS backend:

    sam package --output-template-file packaged.yaml && \
    sam deploy --template-file packaged.yaml --parameter-overrides AlertEmail="youremail@example.com"

If successful, the output will contain the endpoint URL.
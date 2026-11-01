``` shell
# Prepare service principal
SUBSCRIPTION_ID='3881e809-e8cc-4a7a-a830-f0e9eb92dbc7'

az ad sp create-for-rbac                    \
--name "karlpoc"                            \
--scopes /subscriptions/${SUBSCRIPTION_ID}  \
--role Reader
```


``` shell
docker run -it --rm \
-e AZURE_CLIENT_ID="<appId>" \
-e AZURE_CLIENT_SECRET="<password>" \
-e AZURE_TENANT_ID="<tenant>" \
mcr.microsoft.com/azure-cli:latest \
sh -c "az login --service-principal -u \$AZURE_CLIENT_ID -p \$AZURE_CLIENT_SECRET --tenant \$AZURE_TENANT_ID && az account show"
```

``` shell
docker compose up
```
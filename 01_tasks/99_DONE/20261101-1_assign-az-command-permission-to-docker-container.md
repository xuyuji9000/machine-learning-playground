
# Command

```shell
# prepare a clean az login status
az account list -otable
az logout

# Log with a separate testing account
TENANT_ID='3bf7de9e-c986-44dd-baa7-138dfe56ed74'

az login \
--tenant ${TENANT_ID}
```


``` shell
# run an az command
# with local logged in az command
docker run -it \
-v "$HOME/.azure:/root/.azure" \
mcr.microsoft.com/azure-cli:azurelinux3.0 \
az group list -otable
```




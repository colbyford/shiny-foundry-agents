# Microsoft Foundry Agents in Shiny Apps

<h3 align="right">Colby T. Ford, Ph.D.</h3>

Logic for Deploying Custom Microsoft Foundry Agents as Shiny Python Apps in Azure


## Run the Shiny App Locally

```bash
## Install the required Python packages
python -m pip install -r app/requirements.txt

## Start the Shiny app and launch it in the browser
python -m shiny run --reload --launch-browser app/app.py
```


## Deploy the Shiny App to Azure

```bash
## Install the Azure Developer CLI (azd) if you haven't already
## https://aka.ms/azure-dev/install
## Log in to your Azure account
azd login
## Initialize the Azure project in the root of the repo
azd init
## Deploy the infrastructure
azd deploy
## Run the app in Azure
azd up
```


### Grant Permissions between App and Agent

First, create a user assigned managed identity for the web app.
```bash
az webapp identity assign \
  --name <WEB_APP_NAME> \
  --resource-group <RESOURCE_GROUP>

az ad sp show --id http://<WEB_APP_NAME>
## This will give you the service principal ID for the web app's managed identity.
```

Then, grant the web app's service principal permissions to access the agent.

```bash
az role assignment create \
    --assignee <WEB_APP_SERVICE_PRINCIPAL_ID> \
    --role "Azure AI User" \
    --scope /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>
```
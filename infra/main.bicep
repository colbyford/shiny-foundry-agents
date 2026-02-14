
param location string = resourceGroup().location
param appName string = 'app-shiny-foundry-agent-001'
param pythonVersion string = '3.11'

resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      appCommandLine: 'shiny run app.py --host 0.0.0.0'
      appSettings: [
        {
          name: 'PORT'
          value: '8000'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
    }
    httpsOnly: true
  }

  tags: { 'azd-service-name' : 'app' }
}

output endpoint string = 'https://${webApp.properties.defaultHostName}'

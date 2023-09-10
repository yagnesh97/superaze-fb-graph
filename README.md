# Getting Started with Automate Facebook Post with Graph API
Introducing a comprehensive guide to efficiently automate the process of publishing posts on your Facebook page.

## Prerequisites

* Python 3
* Account on [Github](https://github.com/)
* Account and app on [Meta for Developers](https://developers.facebook.com/apps/611749401076520/dashboard/)
* Account on [Microsoft Azure](https://portal.azure.com/)

## Getting Started

### Facebook Graph API
Create an access token for the Facebook Graph API that never expires.

#### Get your Page ID and Page name
* Refer [Graph Explorer](https://developers.facebook.com/docs/pages/getting-started#use-the-graph-explorer) to obtain your `Page ID` and `Page name`, which will be utilized in the environment.

#### Steps for generating an access token with no expiration date:
1. Refer [Pages API - Access Token](https://developers.facebook.com/docs/pages/access-tokens#get-a-page-access-token) to generate a Long-lived Page Access Token.
2. Go to [Access token debugger](https://developers.facebook.com/tools/debug/accesstoken/) to see detailed info for an access token. Paste the Long-Lived Page Access Token and hit the `Debug` button.
3. Copy the `App-Scoped User ID`.
4. Paste **App-Scoped User ID** and **Long-lived Page Access Token** to the below endpoint and hit the same.
   ```https://graph.facebook.com/v17.0/{app_scoped_user_id}/accounts?access_token={long_lived_access_token}```
5. This will provide you with a JSON response containing an access_token that never expires.

### Bing News Search API

Subscribe to [Bing News Search API](https://learn.microsoft.com/en-us/bing/search-apis/bing-news-search/overview) and generate an access token.

### Azure Functions

Explore [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/) to set up your serverless computing service and obtain your [Function URL](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python-v2%2Cin-process%2Cfunctionsv2&pivots=programming-language-python#usage), a HTTP endpoint for executing your code.

## Deployment

#### Set Environment Variables

* Refer [Application Settings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings?tabs=portal#settings) in the `Function App` to configure the environment variables.
* Refer [Functions deployment](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators) to run the function locally and deploy your project & function app.
* Refer [Secrets in Github Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) to configure your secrets such `FUNCTION_KEY` and `ACCESS_TOKEN` in your [master.yml](.github/workflows/master.yml).
* Configure your endpoint in the [master.yml](.github/workflows/master.yml) and push your commits to the remote master branch in order to execute your workflow.

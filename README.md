## Description
It's a template to implement integration tasks with huntflow API.
It contains two webhook handlers at hf_integration_sample/api/views:

* applicant_hook.py - suppopsed to be used as a hook for applicant changes
* vacancy_hook.py - supposed to be used as a hook for vacancy changes

Hooks already have defined incoming data structures (actually not all fields are defined, just the
base ones) (hf_integration_sample.api.serializers.request):

* applicant_hook.ApplicantHookRequest - request structure for applicant's changes
* vacancy_hook.VacancyHookRequest - request structure for vacancy's changes

The whole application is based on FastAPI framework (https://fastapi.tiangolo.com).
For integration with Huntflow API here is already implemented:

* requests signature checks
* PING requests processing
* http client for Huntflow API

## Settings

All possible application settings are defined in hf_integration_sample/app/config.py.
To redefine a config parameter use environment variables or an env file (located at config/).
For particular integration you definitely have to change:

* HF_API_URL: - url (including schema) where Huntflow API server serves requests
* HF_API_TOKEN: - Huntflow API token created via Huntflow web interface, look at
  https://dev-100-api.huntflow.dev/v2/docs#overview for information about API tokens
* HF_ORG_ACCOUNT_ID: - ID of organization account in Huntflow service, you can get it using API
  method https://dev-100-api.huntflow.dev/v2/docs#get-/accounts
* SERVICE_SECRET: - some string to secure webhooks endpoints (the same secret should be specified
  when you create a webhook in huntflow interface).

## Running locally

* install dependencies from requirements.txt (with pip: pip install -r requirements.txt)
* run service: python main.py (will be started at 8000 port)

## Code structure

* codestyle/ - requirements for codestyle enforcements and checks
* config/ - place to store .env files with application settings for different environments
* hf_integration_sample/api/ - service endpoints implementation, which is structured to:
    * controllers - main logic implementation
    * serializers - data structures for requests and responses (with built-in simple validation)
    * views - routes with endpoints. Endpoints have no logic, they are just connect serializers and
      controllers
* hf_integration_sample/app/ - contains common application boilerplate (middlewares, logging,
  dependecies)
* hf_integration_sample/common_dto/ - definition of data structures (used both in webhooks endpoints
  and in calls to Huntflow API). Here DTO - data transfer object.
* hf_integration_sample/integrations/ - implementation of clients to external services. Only one
  client is implemented - Huntflow API client (also it's implementation is like a starting template,
  it's far away from complete implementation).
* hf_integration_sample/utils/ - different helping stuff (which has nowhere else to put)

# corva-worker-python

A repository for integrated python data app development.

![develop](https://github.com/corva-ai/corva-worker-python/workflows/CI/badge.svg?branch=master)

## Publishing to PYPI

Follow these steps to publish the distribution to PYPI:
1. Check out "master" branch
2. Update the version (with v1.2.3 format) in setup.py, commit the change, and push
3. Tag the master branch the same as the above and push

## Included Modules
### API
API requests retries:
- Uses Retry from urllib3 and HTTPAdapter from requests.adapters
- Default retry count: 5
- Retried for status codes: 408, 429, 500, 502, 503, 504
- Retried for methods: GET, POST, PATCH, PUT, DELETE
- Backoff factor: 0.3

Http status codes:
- 401: Unauthorized
- 403: Forbidden
- 408: Request Timeout
- 429: Too Many Requests
- 500: Internal Server Error
- 502: Bad Gateway
- 503: Service Unavailable
- 504: Gateway Timeout

### State Handlers
### Task Handler
Task handler class allows triggering lambda functions whenever a task is submitted to the `/v2/tasks` endpoint.
Refer to [Task Handler Documentation](docs/TASK_HANDLER.md) 
### Logging
### Rollbar
### APP and Modules
### Wellbore

# requests-wrapper
| Code quality checks  | Status |
| ------------- |:-------------:|
| CodeFactor      |  [![Codefactor](https://www.codefactor.io/repository/github/chilledgeek/requests-wrapper/badge?style=plastic)](https://www.codefactor.io/repository/github/chilledgeek/requests-wrappert) |
| Github Workflows |  [![GithubWorkflows](https://github.com/chilledgeek/requests-wrapper/workflows/Tests/badge.svg?branch=master)](https://github.com/chilledgeek/requests-wrapper/actions?query=workflow%3ATests)|
| Codecov | [![codecov](https://codecov.io/gh/chilledgeek/requests-wrapper/branch/master/graph/badge.svg)](https://codecov.io/gh/chilledgeek/requests-wrapper)|



This repo is a wrapper programme based python's requests package, 
adding a simple API key management capability.

It is designed to:
- Enable calling API endpoints using multiple API keys
- So that different API keys can be used for each consecutive call
- This can potentially benefit in cases where each API key is rate limiting
- When the rate limit is specified, this wrapper will automatically sleep accordingly until 
  the API key can be used again, reducing the chance of getting 
  a bad `429 Too Many Requests` error code

## Installation
```pip install requests-wrapper```

## Example
``` python
from requests_wrapper.requests_wrapper import RequestsWrapper

# Load API keys, api_key_header and rate limit when constructing the class instance
requests_wrapper = RequestsWrapper(
    api_keys=["<api_key1>", "<api_key2>"],
    api_key_header="Authorization",
    call_limit_per_second=2
)

queries = ["search_term1", "search_term2", "search_term3"]
responses = []

for query in queries:

    # Calling this is almost the same as calling requests, 
    # with the addition of specifying the http_method 
    response = requests_wrapper.call(
        http_method="get",
        url="<my_url>",
        params={"q": query}
    )

    responses.append(response)
```

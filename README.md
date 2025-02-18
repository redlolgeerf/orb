orb
====

An api for getting the usage data for the current billing period.


Running
=======

`uv run -- fastapi dev orb/main.py`


Tests
=======

`uv run -- pytest tests`


Descisions made
===============

1. packaging

I decided to use `uv`. Just because I haven't used before, so it was a great opportunity to learn something new :-)
Because it's my first time using it, I haven't structured the project in the best way. If I wanted to spend more time on this, I would try to figure out, how to separate test dependencies from main ones.

1. fastapi

Because the service is just calling other apis and combinging data from them, most of the work done is just waiting for an http response. As it is io intensive and not cpu intensive, I've chosed to use fastapi. There are obviously other python async frameworks. Reasons for fastapi: established and mature, fast, has neat api.

1. pydantic

We need to deserialise data recieved from other services. In order to make it maintainable, I'm using pydantic dataclasses to do so. Plus it works great with fastapi.

1. Decimals

Because we are dealing with floating numbers arithmetic, I'm using Decimals. Unfortuenatly, that does not work with the scheme provided, so I'm converting them to a float before returning a response.


Concessions
===============

1. Logging

Because of time constrains I didn't do anything about logging. If this would be a real world service, I would use structlog 

1. Observability

Same as the above. In real world scenario, I would want to use opentelemetry/prometheus to have an insight in response time, errors, response time of external services.

1. Error handling

Right now, the service does not try to handle any errors and just returns 500 response.

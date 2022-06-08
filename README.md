![seizu logo](/images/logo-horizontal-with-text-black.png#gh-light-mode-only)
![seizu logo](/images/logo-horizontal-with-text-white.png#gh-dark-mode-only)

# Seizu (星図)

## What is Seizu?

[Seizu (星図)](https://paypay.github.io/seizu/) is a react/mui frontend and python backend for various forms of reporting of Neo4j graph data.
It is well suited for building reporting for tools like [cartography](https://github.com/lyft/cartography) and [starbase](https://github.com/JupiterOne/starbase)

Seizu includes:

* A configuration-driven react/mui frontend, with support for a dashboard, arbitrary reports, using a row/panel based layout with various panel types for visualizing data
* A backend worker that can run queries on a schedule, or triggered by graph events, with action plugins that can use the results; for example, sending query results to a slack channel, or an sqs queue
* A backend worker that can push query results from panels into statsd, for historical data tracking purposes
* A mechanism of providing SSO for Neo4j, when Seizu is placed behind an OAuth2 proxy

## Getting started

Seizu has a [quickstart guide](https://paypay.github.io/seizu/dev/docker-compose.html#quickstart), which can be used for evaluation, or development.

## Documentation

* [Installation documentation](https://paypay.github.io/seizu/install/backend.html)
* [Dashboard configuration](https://paypay.github.io/seizu/install/dashboard.html)
* [Scheduled query documentation](https://paypay.github.io/seizu/install/scheduled-queries.html)
* [Basic development documentation](https://paypay.github.io/seizu/dev/docker-compose.html)

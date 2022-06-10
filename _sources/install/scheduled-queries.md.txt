# Scheduled Queries

## Purpose

Dashboards are a good visual representation of a system, for when you want to actively check something, but sometimes you want to be passively notified about changes in the graph data.

Seizu can run queries on a set schedule, or when the SyncMetadata graph data changes.
It can take the query results and pass them into a list of configurable actions.

## Configuration

Scheduled queries are configured as part of the dashboard configuration.

| Field | Description |
|-------|-------------|
| name | A user-friendly name for the scheduled query. |
| cypher | A cypher query to use for this scheduled query. This is a reference to a query in the queries configuration section. The query must return the data as ``details`` |
| params | A list of parameters to pass into the query. See [the PanelParam schema](schema.html#panelparam) for more info. |
| frequency | The frequency, in minutes, to run this query. Mutually exclusive with ``watch_scans``. |
| watch\_scans | A list of SyncMetadata types that will be watched to trigger this query. Each list item is a dictionary, which takes ``grouptype`` and ``syncedtype``. The query will be triggered if any list item matches. Mutually exclusive with ``frequency``. |
| enabled | Whether or not this scheduled query will be run. |
| actions | A list of actions to run, for the query results. See the built-in actions section, or the documentation specific for a custom action for details on how to configure this. |

### Scheduling

To schedule a job to run on a frequency, use the ``frequency`` setting.
This setting is based on minutes.
The following scheduled query will run every 24 hours:

```yaml
  recent-cves-by-severity:
    name: Recently published HIGH/CRITICAL CVEs
    cypher: recent-cves
    params:
      - name: syncedtype
        value:
          - recent
      - name: base_severity
        value:
          - HIGH
          - CRITICAL
    # every 24 hours
    frequency: 1440
    enabled: True
    actions:
      - action_type: slack
        action_config:
          title: Recently published HIGH/CRITICAL CVEs
          initial_comment: |
            The following HIGH/CRITICAL CVEs have been published in the last 2 hours.
          channels:
            # vulnerabilities-alert
            - C00000000
```

If you are using cartography, you can also have a query schedule itself based on a change in the SyncMetadata for a particular type of sync.
The following scheduled query will be triggered when a kubernetes sync successfully completes:

```yaml
  images-with-no-scan:
    name: K8s container images with no vulnerability scans
    cypher: k8s-images-without-scans
    watch_scans:
      - grouptype: KubernetesCluster
        syncedtype: KubernetesCluster
    enabled: True
    actions:
      - action_type: sqs
        action_config:
          sqs_queue: k8s-image-scanner
```

``watch_scans`` works by tracking the schedule query in the graph, and comparing the time of the SyncMetadata nodes to the last time the scheduled query ran.
Due to this, when a new query is added, it will be run immediately, and then only run again after changes are detected.

### Built-in Actions

#### slack

The ``slack`` scheduled query action module can take query results, and attach them as a CSV to a slack message.

The following settings can be set in ``action_config`` for this module:

| Field | Description |
|-------|-------------|
| title | The title of the slack message to send. Required. |
| initial\_comment | The message contents. The CSV will be attached to this message. Required. |
| channels | A list of channel IDs to send this message to. This must be channel IDs and not channel names. Required. |

This action module requires the following environment variable configuration to be set:

* `SLACK_OAUTH_BOT_TOKEN`: The slack oauth API bot token, for authentication.

#### sqs

The ``sqs`` scheduled query action module can take query results and enqueue each result into a specified SQS queue.

The following settings can be set in ``action_config`` for this module:

| Field | Description |
|-------|-------------|
| sqs\_queue | The SQS queue name to enqueue results into. Required. |

For local development purposes, the ``sqs`` module also has two configuration options:

* `SQS_CREATE_SCHEDULED_QUERY_QUEUES`: Whether or not to attempt to automatically create the configured queues.
* `SQS_URL`: URL for the SQS server. For use when running a local/fake SQS server.

#### log

The ``log`` scheduled query action module can take query results and log the results.

The following settings can be set in ``action_config`` for this module:

| Field | Description |
|-------|-------------|
| message | The log message to log. Default: ``Result for <scheduled_query_id>`` |
| level | The log level to use. Valid values: ``debug``, ``info``, ``warning``, ``error``, ``critical``. Default: ``info`` |
| log\_attrs | A list of attributes from the returned data to log. Required. |

This module is primarily intended for test and development, so it is not enabled by default.

### Custom actions

Custom actions can be included through python modules.
This is configured through the ``SCHEDULED_QUERY_MODULES`` setting, which is a comma separated list, with a default of ``reporting.scheduled_query_modules.sqs,reporting.scheduled_query_modules.slack``.

The custom action module must implement the action ModuleInterface:

.. literalinclude:: ../../../reporting/scheduled_query_modules/__init__.py
    :pyobject: ModuleInterface

Note that the above is a type hint for a module itself.
So, these functions should be implemented directly in the module, and not as a subclass.
For example:

```python
def action_name() -> str:
    return "print"


def setup() -> None:
    return


def handle_results(
    scheduled_query_id: str,
    action: ScheduledQueryAction,
    results: List[Dict[str, Any]],
) -> None:
    for result in results:
        print(result)
```

Settings for the modules should be fetched within the module itself, for example:

```python
from reporting.utils.settings import str_env

_SLACK_OAUTH_BOT_TOKEN = str_env("SLACK_OAUTH_BOT_TOKEN")
```

## Run the ``schedule-queries`` worker

The worker can be run as a flask CLI command:

```bash
$> export FLASK_APP=reporting.reporting.scheduled_queries
$> flask worker schedule-queries
```

This worker runs until it is explicitly terminated.

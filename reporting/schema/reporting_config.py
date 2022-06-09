from dataclasses import field
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

import marshmallow.validate
import yaml
from marshmallow_dataclass import class_schema
from marshmallow_dataclass import dataclass
from marshmallow_dataclass import NewType
from marshmallow_jsonschema import JSONSchema


InputTypes = NewType(
    "InputTypes",
    str,
    validate=marshmallow.validate.OneOf(["autocomplete", "text"]),
)


@dataclass
class InputDefault:
    label: str = field(
        metadata={
            "description": "The label for the default.",
            "required": True,
        }
    )

    value: str = field(
        metadata={
            "description": "The value for the default.",
            "required": True,
        }
    )

    class Meta:
        ordered = True


@dataclass
class Input:
    input_id: str = field(
        metadata={
            "required": True,
            "description": "Reference to the query in the inputs section.",
            "examples": ["cve_base_severity"],
        }
    )

    label: str = field(
        metadata={
            "required": True,
            "description": "The label to use for the select element.",
            "examples": ["CVE base severity"],
        },
    )

    _type: InputTypes = field(
        metadata={
            "required": True,
            "data_key": "type",
            "description": "The type of input to use.",
            "examples": ["autocomplete"],
        },
    )

    cypher: Optional[str] = field(
        default=None,
        metadata={
            "required": False,
            "description": "The Cypher query to execute. Must return ``value``.",
            "examples": [
                """
                .. code-block:: cypher

                  MATCH (c:CVE)
                  RETURN DISTINCT c.base_severity AS value
                """
            ],
        },
    )

    default: Optional[InputDefault] = field(
        default=None,
        metadata={
            "description": "The default value to set if no value is selected.",
            "examples": [
                """
                .. code-block:: yaml

                  label: (all)
                  value: .*
                """
            ],
        },
    )

    size: Optional[float] = field(
        default=2.0,
        metadata={
            "description": "The size of the input element.",
            "examples": ["2.0"],
        },
    )

    class Meta:
        ordered = True


@dataclass
class BarPanelSettings:
    legend: Optional[str] = field(
        metadata={
            "required": False,
            "description": (
                "The type of legend to use; ``row`` or ``column``. If unset,"
                " then no legend will be used."
            ),
        }
    )

    class Meta:
        ordered = True


@dataclass
class PiePanelSettings:
    legend: Optional[str] = field(
        metadata={
            "required": False,
            "description": (
                "The type of legend to use; ``row`` or ``column``. If unset,"
                " then no legend will be used, and arc labels will be used"
                " instead."
            ),
        }
    )

    class Meta:
        ordered = True


@dataclass
class PanelParam:
    name: str = field(
        metadata={
            "required": True,
            "description": "The parameter name to use when passing this input into the query.",
            "examples": ["severity"],
        }
    )

    input_id: Optional[str] = field(
        default=None,
        metadata={
            "required": False,
            "description": "Reference to the query in the inputs section.",
            "examples": ["cve_base_severity"],
        },
    )

    value: Optional[Any] = field(
        default=None,
        metadata={
            "required": False,
            # explicitly define the jsonschema since marshmallow_jsonschema
            # has a bug around the Any type
            "_jsonschema_type_mapping": {
                "description": "The parameter value to pass into the query.",
                "examples": [
                    """
                    .. code-block:: yaml

                      params:
                        - name: integrityImpact
                          value: HIGH
                    """
                ],
            },
        },
    )

    class Meta:
        ordered = True


@dataclass
class Panel:
    _type: str = field(
        metadata={
            "required": True,
            "data_key": "type",
            "description": "The type of panel to use.",
            "examples": ["table"],
            "validate": marshmallow.validate.OneOf(
                [
                    "table",
                    "vertical-table",
                    "count",
                    "bar",
                    "pie",
                    "progress",
                    "oncall-table",
                    "markdown",
                ]
            ),
        },
    )

    cypher: Optional[str] = field(
        default=None,
        metadata={
            "description": "A reference to a cypher from the cypher section of the configuration.",
            "examples": ["cves"],
        },
    )

    details_cypher: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "A reference to a cypher from the cypher section of the configuration."
                " Must return ``details``. Used in the details section of the panel, as"
                " a table."
            ),
            "examples": ["cves-details"],
        },
    )

    params: List[PanelParam] = field(
        default_factory=list,
        metadata={
            "required": False,
            "description": (
                "A list of parameters to send into the query. The parameters can"
                " directly have values, or can be a reference to an input."
            ),
            "examples": [
                """
                .. code-block:: yaml

                  params:
                    - name: severity
                      input_id: cve_base_severity
                    - name: integrityImpact
                      value: HIGH
                """
            ],
        },
    )

    caption: Optional[str] = field(
        default=None,
        metadata={
            "description": "The caption to use for the panel.",
            "examples": ["Critical CVEs"],
        },
    )

    table_id: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The cypher attribute to use for the table's unique ID, if using a"
                " type of table or vertical-table. If not set, a random ID will be"
                " generated. A table_id should be set for ``vertical-table``, or"
                " the panel will have a random ID used as the caption."
            ),
            "examples": ["cve_id"],
        },
    )

    markdown: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The markdown to use for the panel. Only used for type ``markdown``."
            ),
            "examples": [
                """
                .. code-block:: markdown

                    ## Affects

                    Versions x.x.x - x.x.x

                    ## Recommended action

                    Upgrade to the latest version of the software.
                """
            ],
        },
    )

    size: Optional[float] = field(
        default=2.0,
        metadata={
            "description": "The size of the panel.",
            "examples": ["2.0"],
        },
    )

    threshold: Optional[float] = field(
        default=None,
        metadata={
            "description": "The size of the panel.",
            "examples": ["70"],
        },
    )

    bar_settings: Optional[BarPanelSettings] = field(
        default=None,
        metadata={
            "description": "Settings specific to bar panels.",
            "examples": [
                """
                .. code-block:: yaml

                  bar_settings:
                    legend: column
                """
            ],
        },
    )

    pie_settings: Optional[PiePanelSettings] = field(
        default=None,
        metadata={
            "description": "Settings specific to pie panels.",
            "examples": [
                """
                .. code-block:: yaml

                  pie_settings:
                    legend: column
                """
            ],
        },
    )

    metric: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The statsd metric to send from the panel data."
                " Only used for ``count`` and ``progress`` panels."
            ),
            "examples": ["cves.severity"],
        },
    )

    class Meta:
        ordered = True


@dataclass
class Row:
    name: str = field(
        metadata={
            "required": True,
            "description": "The name of the row; shown as title above the row.",
            "examples": ["CVEs"],
        },
    )

    panels: List[Panel] = field(
        metadata={
            "required": True,
            "description": "The panels to show in the row.",
            "examples": [
                """
                .. code-block:: yaml

                  panels:
                    - cypher: cves-by-severity
                      details_cypher: cves-by-severity-details
                      type: count
                      params:
                        base_severity: CRITICAL
                      caption: Critical CVEs
                      size: 2
                """
            ],
        },
    )

    class Meta:
        ordered = True


@dataclass
class Dashboard:
    rows: List[Row] = field(
        default_factory=list,
        metadata={
            "required": True,
            "description": "The rows of the dashboard.",
            "examples": [
                """
                .. code-block:: yaml

                  rows:
                    - name: "CVEs by severity"
                      panels:
                        - cypher: cves-by-severity
                          details_cypher: cves-by-severity-details
                          type: count
                          params:
                            base_severity: CRITICAL
                          caption: Critical CVEs
                          size: 2
                """
            ],
        },
    )

    class Meta:
        ordered = True


@dataclass
class Report:
    name: str = field(
        metadata={
            "required": True,
            "description": "The name of the report.",
            "examples": ["CVEs"],
        },
    )

    inputs: List[Input] = field(
        default_factory=list,
        metadata={
            "required": False,
            "description": "The inputs to use for the report.",
            "examples": [
                """
                .. code-block:: yaml

                  inputs:
                    - input_id: cve_base_severity
                      cypher: |-
                        MATCH (c:CVE)
                        RETURN c.base_severity AS base_severity
                      default:
                        label: (all)
                        value: .*
                      label: Base Severity
                      type: autocomplete
                      size: 2
                """
            ],
        },
    )

    rows: List[Row] = field(
        default_factory=list,
        metadata={
            "required": True,
            "description": "The rows of the report.",
            "examples": [
                """
                .. code-block:: yaml

                  rows:
                    - name: "CVEs"
                      panels:
                        - cypher: cves
                          type: table
                          params:
                            - name: severity
                              input_id: cve_base_severity
                          size: 12
                """
            ],
        },
    )

    class Meta:
        ordered = True


@dataclass
class ScheduledQueryWatchScan:
    grouptype: Optional[str] = field(
        default=".*",
        metadata={
            "description": (
                "Match against the grouptype attribute of the SyncMetadata"
                " node, as a regex. If not set, the query will match against"
                " ``.*``."
            ),
            "examples": ["CVE"],
        },
    )

    syncedtype: Optional[str] = field(
        default=".*",
        metadata={
            "description": (
                "Match against the syncedtype attribute of the SyncMetadata"
                " node, as a regex. If not set, the query will match against"
                " ``.*``."
            ),
            "examples": ["year"],
        },
    )

    groupid: Optional[str] = field(
        default=".*",
        metadata={
            "description": (
                "Match against the groupid attribute of the SyncMetadata"
                " node, as a regex. If not set, the query will match against"
                " ``.*``."
            ),
            "examples": ["2019"],
        },
    )

    class Meta:
        ordered = True


@dataclass
class ScheduledQueryAction:
    action_type: str = field(
        metadata={
            "required": True,
            "description": "The type of action to perform.",
            "examples": ["slack", "sqs"],
        },
    )

    action_config: Dict[str, Any] = field(
        metadata={
            # explicitly define the jsonschema since marshmallow_jsonschema
            # has a bug around the Any type
            "_jsonschema_type_mapping": {
                "description": (
                    "The configuration for the action. See the documentation for the"
                    " relevant scheduled query module for information about the"
                    " configuration needed for each action type."
                ),
                "examples": [
                    """
                    .. code-block:: yaml

                      action_config:
                        webhook_url: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
                        channel: #cve
                        username: CVE
                        icon_emoji: :cve:
                    """
                ],
                "additionalProperties": {
                    "title": "action_config",
                },
            },
        },
    )

    class Meta:
        ordered = True


@dataclass
class ScheduledQueryParam:
    name: str = field(
        metadata={
            "required": True,
            "description": "The parameter name to use when passing this input into the query.",
            "examples": ["severity"],
        }
    )

    value: Any = field(
        metadata={
            "required": True,
            # explicitly define the jsonschema since marshmallow_jsonschema
            # has a bug around the Any type
            "_jsonschema_type_mapping": {
                "description": "The parameter value to pass into the query.",
                "examples": [
                    """
                    .. code-block:: yaml

                      params:
                        - name: integrityImpact
                          value: HIGH
                    """
                ],
            },
        },
    )

    class Meta:
        ordered = True


@dataclass
class ScheduledQuery:
    name: str = field(
        metadata={
            "required": True,
            "description": "The name of the scheduled query.",
            "examples": ["Recently published HIGH/CRITICAL CVEs"],
        },
    )

    cypher: str = field(
        metadata={
            "required": True,
            "description": "The cypher to use for the scheduled query.",
            "examples": ["recent-cves"],
        },
    )

    params: List[ScheduledQueryParam] = field(
        default_factory=lambda: [],
        metadata={
            "required": False,
            "description": (
                "A dictionary of parameters to pass to the cypher query. The keys"
                " are the variable names, and the values are the values to pass."
            ),
            "examples": [
                """
                .. code-block:: yaml

                  params:
                    - name: syncedtype
                      value:
                        - recent
                    - name: base_severity
                      value:
                        - HIGH
                        - CRITICAL
                """
            ],
        },
    )

    frequency: Optional[int] = field(
        default=None,
        metadata={
            "description": (
                "The frequency of the scheduled query in minutes. Mutually"
                " exclusive with ``watch_scans``."
            ),
            "examples": ["1440"],
        },
    )

    watch_scans: List[ScheduledQueryWatchScan] = field(
        default_factory=list,
        metadata={
            "required": False,
            "description": (
                "The scans to watch for the scheduled query. Based on"
                " SyncMetadata. Query will triger if any of the watched"
                " scans listed are updated. Mutually exclusive with"
                " ``frequency``."
            ),
            "examples": [
                """
                .. code-block:: yaml

                  watch_scans:
                    - grouptype: CVE
                      syncedtype: recent
                    - grouptype: CVE
                      syncedtype: modified
                """
            ],
        },
    )

    enabled: Optional[bool] = field(
        default=True,
        metadata={
            "description": (
                "Whether the scheduled query should be enabled. If not set, the"
                " scheduled query will be enabled."
            ),
            "examples": ["true"],
        },
    )

    actions: List[ScheduledQueryAction] = field(
        default_factory=list,
        metadata={
            "description": (
                "The actions to perform when the scheduled query is triggered."
            ),
            "examples": [
                """
                .. code-block:: yaml

                  actions:
                    - action_type: slack
                      title: Recently published HIGH/CRITICAL CVEs
                      initial_comment: |
                        The following HIGH/CRITICAL CVEs have been published in the last 24 hours.
                      channels:
                        - C0000000000
                """
            ],
        },
    )

    class Meta:
        ordered = True


@dataclass
class ReportingConfig:
    """
    test
    """

    version: Optional[int] = field(
        default=1,
        metadata={
            "required": False,
            "description": ("The configuration file format version."),
        },
    )

    queries: Dict[str, str] = field(
        default_factory=dict,
        metadata={
            "description": "The queries to use for the report.",
            "examples": [
                """
                .. code-block:: yaml

                  queries:
                    cves-severity-of-total: |-
                      MATCH (c:CVE)
                      WITH COUNT(DISTINCT c.id) AS denominator
                      MATCH (c:CVE)
                      WHERE c.base_severity = "CRITICAL"
                      RETURN count(DISTINCT c.id) AS numerator, denominator
                    cves-by-severity: |-
                      MATCH (c:CVE)
                      WHERE c.base_severity = $base_severity
                      RETURN count(c.id) AS count
                    cves: |-
                      MATCH (c:CVE)
                      WHERE c.base_severity =~ ($base_severity)
                      RETURN {
                        cve_id: c.id,
                        base_severity: c.base_severity,
                        severity: c.severity,
                        description: c.description
                      } AS details
                      ORDER BY details.severity DESC
                    recent-cves: |-
                      MATCH (s:SyncMetadata)
                      WHERE s.grouptype = "CVE" AND s.syncedtype IN $syncedtype
                      WITH datetime({epochSeconds: s.lastupdated}) - duration({hours: 24}) AS feedupdatetime
                      MATCH (c:CVE)
                      WHERE (datetime(c.published_date) > feedupdatetime AND c.base_severity IN $base_severity
                      RETURN {
                        id: c.id,
                        base_severity: c.base_severity,
                        base_score: c.base_score,
                        description: c.description_en
                      } AS details
                """
            ],
        },
    )

    dashboard: Dashboard = field(
        default_factory=Dashboard,
        metadata={
            "description": "The dashboard to use for the report.",
            "examples": [
                """
                .. code-block:: yaml

                  dashboard:
                    rows:
                      - name: CVEs by severity as percentage of total
                        panels:
                          - cypher: cves-severity-of-total
                            type: progress
                            params:
                              - name: base_severity
                                value: CRITICAL
                            caption: Critical CVEs
                            size: 2
                      - name: CVEs by severity
                        panels:
                          - cypher: cves-by-severity
                            type: count
                            params:
                              - name: base_severity
                                value: CRITICAL
                              caption: Critical CVEs
                            size: 2
                          - cypher: cves-by-severity
                            type: count
                            params:
                              - name: base_severity
                                value: HIGH
                            caption: High CVEs
                            size: 2
                """
            ],
        },
    )

    reports: Dict[str, Report] = field(
        default_factory=dict,
        metadata={
            "required": False,
            "description": "The reports to use for the report.",
            "examples": [
                """
                .. code-block:: yaml

                  reports:
                    cves:
                      name: CVEs
                      inputs:
                        - input_id: cve_base_severity
                          cypher: |-
                            MATCH (c:CVE)
                            RETURN c.base_severity AS base_severity
                          default:
                            label: (all)
                            value: .*
                          label: Base Severity
                          type: autocomplete
                          size: 2
                      rows:
                        - name: CVEs
                          panels:
                            - cypher: cves
                              type: table
                              params:
                                - name: severity
                                  input_id: cve_base_severity
                              size: 12
                """
            ],
        },
    )

    scheduled_queries: Dict[str, ScheduledQuery] = field(
        default_factory=dict,
        metadata={
            "required": False,
            "description": "The scheduled queries to use for the report.",
            "examples": [
                """
                .. code-block:: yaml

                  scheduled_queries:
                    cves-by-severity:
                      name: CVEs by severity
                      frequency: 1440
                      watch_scans:
                        - grouptype: CVE
                          syncedtype: recent
                      actions:
                        - action_type: slack
                          title: Recently published HIGH/CRITICAL CVEs
                          initial_comment: |
                            The following HIGH/CRITICAL CVEs have been published in the last 24 hours.
                          channels:
                            - C0000000000
                """
            ],
        },
    )

    Schema: ClassVar[Type[marshmallow.Schema]] = marshmallow.Schema

    class Meta:
        ordered = True


def output_json_schema() -> Dict[str, Any]:
    json_schema = JSONSchema(props_ordered=True)
    schema = class_schema(ReportingConfig)()
    return json_schema.dump(schema)


def dump_yaml(reporting_config: ReportingConfig) -> str:
    return yaml.dump(
        ReportingConfig.Schema().dump(reporting_config),
        default_flow_style=False,
        allow_unicode=True,
    )


def load(reporting_config: Dict[str, Any]) -> ReportingConfig:
    return ReportingConfig.Schema().load(reporting_config)


def load_yaml(reporting_config_yaml: str) -> ReportingConfig:
    return load(yaml.safe_load(reporting_config_yaml))


def load_file(reporting_config_file: str) -> ReportingConfig:
    with open(reporting_config_file, "r") as f:
        return load_yaml(f.read())

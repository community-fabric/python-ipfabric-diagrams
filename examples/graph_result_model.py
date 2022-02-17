from ipfabric_diagrams.output_models.graph_result import GraphResult


if __name__ == '__main__':
    print(GraphResult.schema_json(indent=2))

"""
{
  "title": "GraphResult",
  "type": "object",
  "properties": {
    "nodes": {
      "title": "Nodes",
      "type": "object",
      "additionalProperties": {
        "$ref": "#/definitions/Node"
      }
    },
    "edges": {
      "title": "Edges",
      "type": "object",
      "additionalProperties": {
        "anyOf": [
          {
            "$ref": "#/definitions/NetworkEdge"
          },
          {
            "$ref": "#/definitions/PathLookupEdge"
          }
        ]
      }
    },
    "pathlookup": {
      "$ref": "#/definitions/PathLookup"
    }
  },
  "required": [
    "nodes",
    "edges"
  ],
  "definitions": {
    "Node": {
      "title": "Node",
      "type": "object",
      "properties": {
        "path": {
          "title": "Path",
          "type": "string"
        },
        "boxId": {
          "title": "Boxid",
          "type": "string"
        },
        "children": {
          "title": "Children",
          "type": "array",
          "items": {}
        },
        "graphType": {
          "title": "Graphtype",
          "type": "string"
        },
        "id": {
          "title": "Id",
          "type": "string"
        },
        "label": {
          "title": "Label",
          "type": "string"
        },
        "parentPath": {
          "title": "Parentpath",
          "type": "string"
        },
        "sn": {
          "title": "Sn",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "type": "string"
        },
        "stack": {
          "title": "Stack",
          "type": "boolean"
        }
      },
      "required": [
        "children",
        "graphType",
        "id",
        "label",
        "sn",
        "type"
      ]
    },
    "Label": {
      "title": "Label",
      "type": "object",
      "properties": {
        "type": {
          "title": "Type",
          "type": "string"
        },
        "visible": {
          "title": "Visible",
          "type": "boolean"
        },
        "text": {
          "title": "Text",
          "type": "string"
        }
      },
      "required": [
        "type",
        "visible",
        "text"
      ]
    },
    "Labels": {
      "title": "Labels",
      "type": "object",
      "properties": {
        "center": {
          "title": "Center",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Label"
          }
        },
        "source": {
          "title": "Source",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Label"
          }
        },
        "target": {
          "title": "Target",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Label"
          }
        }
      }
    },
    "Style": {
      "title": "Style",
      "type": "object",
      "properties": {
        "color": {
          "title": "Color",
          "type": "string",
          "format": "color"
        },
        "pattern": {
          "title": "Pattern",
          "default": "solid",
          "type": "string"
        },
        "thicknessThresholds": {
          "title": "Thicknessthresholds",
          "default": [
            2,
            4,
            8
          ],
          "type": "array",
          "items": {
            "type": "integer"
          }
        }
      },
      "required": [
        "color"
      ]
    },
    "EdgeSettings": {
      "title": "EdgeSettings",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "visible": {
          "title": "Visible",
          "default": true,
          "type": "boolean"
        },
        "grouped": {
          "title": "Grouped",
          "default": true,
          "type": "boolean"
        },
        "style": {
          "$ref": "#/definitions/Style"
        },
        "type": {
          "title": "Type",
          "type": "string"
        },
        "labels": {
          "title": "Labels",
          "default": [
            "protocols"
          ],
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "id": {
          "title": "Id",
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "name",
        "style",
        "type"
      ]
    },
    "NetworkEdge": {
      "title": "NetworkEdge",
      "type": "object",
      "properties": {
        "direction": {
          "title": "Direction",
          "type": "string"
        },
        "source": {
          "title": "Source",
          "type": "string"
        },
        "target": {
          "title": "Target",
          "type": "string"
        },
        "edgeSettingsId": {
          "title": "Edgesettingsid",
          "type": "string",
          "format": "uuid"
        },
        "id": {
          "title": "Id",
          "type": "string"
        },
        "labels": {
          "$ref": "#/definitions/Labels"
        },
        "edgeSettings": {
          "$ref": "#/definitions/EdgeSettings"
        },
        "circle": {
          "title": "Circle",
          "type": "boolean"
        },
        "children": {
          "title": "Children",
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "direction",
        "source",
        "target",
        "edgeSettingsId",
        "id",
        "labels",
        "circle",
        "children"
      ]
    },
    "Severity": {
      "title": "Severity",
      "type": "object",
      "properties": {
        "0": {
          "title": "0",
          "type": "integer"
        },
        "10": {
          "title": "10",
          "type": "integer"
        },
        "20": {
          "title": "20",
          "type": "integer"
        },
        "30": {
          "title": "30",
          "type": "integer"
        }
      },
      "required": [
        "0",
        "10",
        "20",
        "30"
      ]
    },
    "TrafficScore": {
      "title": "TrafficScore",
      "type": "object",
      "properties": {
        "accepted": {
          "title": "Accepted",
          "type": "integer"
        },
        "dropped": {
          "title": "Dropped",
          "type": "integer"
        },
        "forwarded": {
          "title": "Forwarded",
          "type": "integer"
        },
        "total": {
          "title": "Total",
          "type": "integer"
        }
      },
      "required": [
        "accepted",
        "dropped",
        "forwarded",
        "total"
      ]
    },
    "PathLookupEdge": {
      "title": "PathLookupEdge",
      "type": "object",
      "properties": {
        "direction": {
          "title": "Direction",
          "type": "string"
        },
        "source": {
          "title": "Source",
          "type": "string"
        },
        "target": {
          "title": "Target",
          "type": "string"
        },
        "edgeSettingsId": {
          "title": "Edgesettingsid",
          "type": "string",
          "format": "uuid"
        },
        "id": {
          "title": "Id",
          "type": "string"
        },
        "labels": {
          "$ref": "#/definitions/Labels"
        },
        "edgeSettings": {
          "$ref": "#/definitions/EdgeSettings"
        },
        "nextEdgeIds": {
          "title": "Nextedgeids",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "prevEdgeIds": {
          "title": "Prevedgeids",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "packet": {
          "title": "Packet",
          "type": "array",
          "items": {
            "type": "object"
          }
        },
        "severityInfo": {
          "$ref": "#/definitions/Severity"
        },
        "sourceIfaceName": {
          "title": "Sourceifacename",
          "type": "string"
        },
        "targetIfaceName": {
          "title": "Targetifacename",
          "type": "string"
        },
        "trafficScore": {
          "$ref": "#/definitions/TrafficScore"
        },
        "nextEdge": {
          "title": "Nextedge",
          "type": "array",
          "items": {}
        },
        "prevEdge": {
          "title": "Prevedge",
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "direction",
        "source",
        "target",
        "edgeSettingsId",
        "id",
        "labels",
        "nextEdgeIds",
        "prevEdgeIds",
        "packet",
        "severityInfo",
        "trafficScore"
      ]
    },
    "Checks": {
      "title": "Checks",
      "type": "object",
      "properties": {
        "0": {
          "title": "0",
          "type": "integer"
        },
        "10": {
          "title": "10",
          "type": "integer"
        },
        "20": {
          "title": "20",
          "type": "integer"
        },
        "30": {
          "title": "30",
          "type": "integer"
        }
      },
      "required": [
        "0",
        "10",
        "20",
        "30"
      ]
    },
    "Topics": {
      "title": "Topics",
      "type": "object",
      "properties": {
        "ACL": {
          "$ref": "#/definitions/Checks"
        },
        "FORWARDING": {
          "$ref": "#/definitions/Checks"
        },
        "ZONEFW": {
          "$ref": "#/definitions/Checks"
        }
      },
      "required": [
        "ACL",
        "FORWARDING",
        "ZONEFW"
      ]
    },
    "EventsSummary": {
      "title": "EventsSummary",
      "type": "object",
      "properties": {
        "flags": {
          "title": "Flags",
          "type": "array",
          "items": {}
        },
        "topics": {
          "$ref": "#/definitions/Topics"
        },
        "global": {
          "title": "Global",
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "flags",
        "topics",
        "global"
      ]
    },
    "Decision": {
      "title": "Decision",
      "type": "object",
      "properties": {
        "traces": {
          "title": "Traces",
          "type": "array",
          "items": {}
        },
        "trafficIn": {
          "title": "Trafficin",
          "type": "object",
          "additionalProperties": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "trafficOut": {
          "title": "Trafficout",
          "type": "object",
          "additionalProperties": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      },
      "required": [
        "traces"
      ]
    },
    "Check": {
      "title": "Check",
      "type": "object",
      "properties": {
        "exists": {
          "title": "Exists",
          "type": "boolean"
        }
      },
      "required": [
        "exists"
      ]
    },
    "PathLookup": {
      "title": "PathLookup",
      "type": "object",
      "properties": {
        "eventsSummary": {
          "$ref": "#/definitions/EventsSummary"
        },
        "decisions": {
          "title": "Decisions",
          "type": "object",
          "additionalProperties": {
            "$ref": "#/definitions/Decision"
          }
        },
        "passingTraffic": {
          "title": "Passingtraffic",
          "type": "string"
        },
        "check": {
          "$ref": "#/definitions/Check"
        }
      },
      "required": [
        "eventsSummary",
        "decisions",
        "passingTraffic",
        "check"
      ]
    }
  }
}
"""

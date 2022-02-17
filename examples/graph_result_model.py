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
        "protocol": {
          "title": "Protocol",
          "default": "",
          "type": "string"
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
    "ICMP": {
      "title": "ICMP",
      "type": "object",
      "properties": {
        "icmpCode": {
          "title": "Icmpcode",
          "type": "integer"
        },
        "icmpType": {
          "title": "Icmptype",
          "type": "integer"
        },
        "type": {
          "title": "Type",
          "enum": [
            "icmp"
          ],
          "type": "string"
        }
      },
      "required": [
        "icmpCode",
        "icmpType",
        "type"
      ]
    },
    "UDP": {
      "title": "UDP",
      "type": "object",
      "properties": {
        "src": {
          "title": "Src",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "dst": {
          "title": "Dst",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "type": {
          "title": "Type",
          "enum": [
            "udp"
          ],
          "type": "string"
        }
      },
      "required": [
        "src",
        "dst",
        "type"
      ]
    },
    "TCP": {
      "title": "TCP",
      "type": "object",
      "properties": {
        "src": {
          "title": "Src",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "dst": {
          "title": "Dst",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "flags": {
          "title": "Flags",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "type": {
          "title": "Type",
          "enum": [
            "tcp"
          ],
          "type": "string"
        }
      },
      "required": [
        "src",
        "dst",
        "flags",
        "type"
      ]
    },
    "ipfabric_diagrams__output_models__packet__Ethernet": {
      "title": "Ethernet",
      "type": "object",
      "properties": {
        "src": {
          "title": "Src",
          "type": "string"
        },
        "dst": {
          "title": "Dst",
          "type": "string"
        },
        "etherType": {
          "title": "Ethertype",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "enum": [
            "ethernet"
          ],
          "type": "string"
        }
      },
      "required": [
        "dst",
        "etherType",
        "type"
      ]
    },
    "IP": {
      "title": "IP",
      "type": "object",
      "properties": {
        "src": {
          "title": "Src",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "dst": {
          "title": "Dst",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "fragment offset": {
          "title": "Fragment Offset",
          "type": "integer"
        },
        "protocol": {
          "title": "Protocol",
          "type": "string"
        },
        "ttl": {
          "title": "Ttl",
          "type": "integer"
        },
        "type": {
          "title": "Type",
          "enum": [
            "ip"
          ],
          "type": "string"
        }
      },
      "required": [
        "src",
        "dst",
        "fragment offset",
        "protocol",
        "ttl",
        "type"
      ]
    },
    "ipfabric_diagrams__output_models__packet__MPLS": {
      "title": "MPLS",
      "type": "object",
      "properties": {
        "stack": {
          "title": "Stack",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "type": {
          "title": "Type",
          "enum": [
            "mpls"
          ],
          "type": "string"
        }
      },
      "required": [
        "stack",
        "type"
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
        "protocol": {
          "title": "Protocol",
          "default": "",
          "type": "string"
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
            "anyOf": [
              {
                "$ref": "#/definitions/ICMP"
              },
              {
                "$ref": "#/definitions/UDP"
              },
              {
                "$ref": "#/definitions/TCP"
              },
              {
                "$ref": "#/definitions/ipfabric_diagrams__output_models__packet__Ethernet"
              },
              {
                "$ref": "#/definitions/IP"
              },
              {
                "$ref": "#/definitions/ipfabric_diagrams__output_models__packet__MPLS"
              }
            ]
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
    "PacketDataMatch": {
      "title": "PacketDataMatch",
      "type": "object",
      "properties": {
        "field": {
          "title": "Field",
          "type": "string"
        },
        "value": {
          "title": "Value",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "enum": [
            "packet data match"
          ],
          "type": "string"
        }
      },
      "required": [
        "field",
        "value",
        "type"
      ]
    },
    "RemoveHeader": {
      "title": "RemoveHeader",
      "type": "object",
      "properties": {
        "index": {
          "title": "Index",
          "type": "integer"
        },
        "headerType": {
          "title": "Headertype",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "enum": [
            "remove header"
          ],
          "type": "string"
        }
      },
      "required": [
        "index",
        "headerType",
        "type"
      ]
    },
    "Filter": {
      "title": "Filter",
      "type": "object",
      "properties": {
        "label": {
          "title": "Label",
          "type": "integer"
        },
        "mask": {
          "title": "Mask",
          "type": "integer"
        },
        "vrf": {
          "title": "Vrf",
          "type": "string"
        },
        "prefix": {
          "title": "Prefix",
          "type": "string"
        },
        "ip": {
          "title": "Ip",
          "type": "string"
        }
      }
    },
    "TableEntryMatch": {
      "title": "TableEntryMatch",
      "type": "object",
      "properties": {
        "filter": {
          "$ref": "#/definitions/Filter"
        },
        "table": {
          "title": "Table",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "enum": [
            "table entry match"
          ],
          "type": "string"
        }
      },
      "required": [
        "filter",
        "table",
        "type"
      ]
    },
    "ipfabric_diagrams__output_models__trace__Ethernet": {
      "title": "Ethernet",
      "type": "object",
      "properties": {
        "dst": {
          "title": "Dst",
          "type": "string"
        },
        "src": {
          "title": "Src",
          "type": "string"
        },
        "etherType": {
          "title": "Ethertype",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "enum": [
            "ethernet"
          ],
          "type": "string"
        },
        "vlan": {
          "title": "Vlan",
          "type": "integer"
        }
      },
      "required": [
        "dst",
        "src",
        "etherType",
        "type"
      ]
    },
    "ipfabric_diagrams__output_models__trace__MPLS": {
      "title": "MPLS",
      "type": "object",
      "properties": {
        "stack": {
          "title": "Stack",
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "type": {
          "title": "Type",
          "enum": [
            "mpls"
          ],
          "type": "string"
        }
      },
      "required": [
        "stack",
        "type"
      ]
    },
    "InsertHeader": {
      "title": "InsertHeader",
      "type": "object",
      "properties": {
        "header": {
          "title": "Header",
          "discriminator": {
            "propertyName": "type",
            "mapping": {
              "ethernet": "#/definitions/ipfabric_diagrams__output_models__trace__Ethernet",
              "mpls": "#/definitions/ipfabric_diagrams__output_models__trace__MPLS"
            }
          },
          "anyOf": [
            {
              "$ref": "#/definitions/ipfabric_diagrams__output_models__trace__Ethernet"
            },
            {
              "$ref": "#/definitions/ipfabric_diagrams__output_models__trace__MPLS"
            }
          ]
        },
        "headerType": {
          "title": "Headertype",
          "type": "string"
        },
        "index": {
          "title": "Index",
          "type": "integer"
        },
        "type": {
          "title": "Type",
          "enum": [
            "insert header"
          ],
          "type": "string"
        }
      },
      "required": [
        "header",
        "headerType",
        "index",
        "type"
      ]
    },
    "Patch": {
      "title": "Patch",
      "type": "object",
      "properties": {
        "stack": {
          "title": "Stack",
          "type": "array",
          "items": {
            "type": "integer"
          }
        },
        "ttl": {
          "title": "Ttl",
          "type": "integer"
        }
      }
    },
    "PatchHeader": {
      "title": "PatchHeader",
      "type": "object",
      "properties": {
        "patch": {
          "$ref": "#/definitions/Patch"
        },
        "index": {
          "title": "Index",
          "type": "integer"
        },
        "type": {
          "title": "Type",
          "enum": [
            "patch header"
          ],
          "type": "string"
        }
      },
      "required": [
        "patch",
        "index",
        "type"
      ]
    },
    "SeverityInfo": {
      "title": "SeverityInfo",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "severity": {
          "title": "Severity",
          "type": "integer"
        },
        "topic": {
          "title": "Topic",
          "type": "string"
        },
        "details": {
          "title": "Details",
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "name",
        "severity",
        "topic"
      ]
    },
    "DropPacket": {
      "title": "DropPacket",
      "type": "object",
      "properties": {
        "type": {
          "title": "Type",
          "enum": [
            "drop packet"
          ],
          "type": "string"
        },
        "reason": {
          "title": "Reason",
          "type": "string"
        },
        "severityInfo": {
          "$ref": "#/definitions/SeverityInfo"
        }
      },
      "required": [
        "type",
        "reason",
        "severityInfo"
      ]
    },
    "Trace": {
      "title": "Trace",
      "type": "object",
      "properties": {
        "chain": {
          "title": "Chain",
          "type": "string"
        },
        "phase": {
          "title": "Phase",
          "type": "string"
        },
        "events": {
          "title": "Events",
          "type": "array",
          "items": {
            "anyOf": [
              {
                "$ref": "#/definitions/PacketDataMatch"
              },
              {
                "$ref": "#/definitions/RemoveHeader"
              },
              {
                "$ref": "#/definitions/TableEntryMatch"
              },
              {
                "$ref": "#/definitions/InsertHeader"
              },
              {
                "$ref": "#/definitions/PatchHeader"
              },
              {
                "$ref": "#/definitions/DropPacket"
              }
            ]
          }
        }
      },
      "required": [
        "chain",
        "phase",
        "events"
      ]
    },
    "Traces": {
      "title": "Traces",
      "type": "object",
      "properties": {
        "severityInfo": {
          "$ref": "#/definitions/Checks"
        },
        "sourcePacketId": {
          "title": "Sourcepacketid",
          "type": "string"
        },
        "targetPacketId": {
          "title": "Targetpacketid",
          "type": "string"
        },
        "trace": {
          "title": "Trace",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Trace"
          }
        }
      },
      "required": [
        "severityInfo",
        "sourcePacketId",
        "targetPacketId",
        "trace"
      ]
    },
    "Decision": {
      "title": "Decision",
      "type": "object",
      "properties": {
        "traces": {
          "title": "Traces",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Traces"
          }
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

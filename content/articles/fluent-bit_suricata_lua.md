Title: Suricata log enrichment for Fluent Bit using Lua
Author: Maciej
Date: 2025-10-23 20:40
Category: blog
Tags: markdown, blog, lua, cybersecurity, fluent-bit, suricata

# Suricata log enrichment for Fluent Bit using Lua

At work, I've been using Fluent Bit to collect logs and ship them to our OpenSearch cluster. This has been working great! However, I needed to normalize some of the Suricata alerts for our student analysts. This was done using Fluent Bit's Lua filters. 

You can find the example in the repository here: [fluent-bit-suricata-enrichment](https://github.com/Xata/fluent-bit-suricata-enrichment)

## What does the script do?

The example Lua script will:

- **Normalize severity alerts**: Converts Suricata's numeric severity (1/2/3) to descriptive levels (critical/high/medium/low/) for humans to read.
- **Category Mapping**: Gives an example way to change verbose Suricata categories to short names.
- **Critical Alert Flagging**: Adds `alert.is_critical` boolean for priority-based alerting based on Suricata's numeric severity (1/2/3).
- **ECS Compatibility**: Adds `event.category` and `event.severity` fields compatible with Elastic Common Schema. 

## Example Transformation

Basically this is what is happening to the ```eve.json``` logs:

**Before:**

```json
{"timestamp":"2024-10-23T14:34:20.789012+0000","flow_id":123456791,"event_type":"alert","src_ip":"172.16.5.10","src_port":22,"dest_ip":"203.0.113.99","dest_port":55123,"proto":"TCP","alert":{"action":"allowed","gid":1,"signature_id":2024003,"signature":"ET SCAN Potential SSH Scan","category":"Network Scan","severity":3}}
```

**After:**

```json
{
  "event_type": "alert",
  "alert": {
    "signature": "ET SCAN Potential SSH Scan",
    "category": "Network Scan",
    "severity": 3,
    "is_critical": false,
    "readable_category": "malware"
  },
  "event": {
    "severity": "medium",
    "category": "reconnaissance"
  }
}
```


Notice the new fields:

- `alert.is_critical: false`: Not a critical alert (severity 3)
- `alert.readable_category: "reconnaissance"`: Mapped from "Network Scan"
- `event.severity: "medium"`: Human-readable severity
- `event.category: "reconnaissance"`: ECS-compatible categorization

## Impact

This enrichment happens in real-time as logs flow through Fluent Bit, with minimal overhead. Our student analysts can now:

- Quickly identify critical alerts without memorizing numeric codes
- Filter and search using standardized category names
- Build better dashboards and alerts in OpenSearch

## Link to the repository

You can find the example in the repository here: [fluent-bit-suricata-enrichment](https://github.com/Xata/fluent-bit-suricata-enrichment)

## Contributing

This project is open source and welcomes contributions! If you have additional Suricata category mappings or improvements, check out the [contributing guidelines](https://github.com/Xata/fluent-bit-suricata-enrichment/blob/main/CONTRIBUTING.md).

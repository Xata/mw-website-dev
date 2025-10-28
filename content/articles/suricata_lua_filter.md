Title: Suricata Log Enrichment for Fluent Bit
Author: Maciej
Date: 2025-10-28 17:12
Category: blog
Tags: markdown, blog, fluentbit, lua, suricata

# Lua Filter for Suricata Logs

I built a Lua filter for Fluent Bit that makes Suricata alerts actually readable for our student Cybersecurity analysts on the Centurion Secured project.

Suricata uses numeric severity codes (1/2/3) and super verbose category names like: A Network Trojan was detected. You might be thinking, "Wow, but I can tell what that is." And yes, you might be right, but I made it shorter for students to quickly see what is going on. 

Real-time log enrichment now does the following:

1. Severity 3 to "medium"
2. "Network Scan" to "reconnaissance"
3. Adds a is_critical flag for priority alerts
4. Makes everything ECS-compatible for OpenSearch

Our student analysts can now spot alerts immediately without decoding numbers or parsing verbose text.

I have a repository with examples and a Docker test setup:

- https://github.com/Xata/fluent-bit-suricata-enrichment

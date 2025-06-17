Title: SOFA Architecture Summary - OpenSearch
Author: Maciej
Date: 2025-06-17 12:47
Category: blog
Tags: markdown, blog, sofa, cybersecurity, IT, security

OpenSearch is an open-source, enterprise-grade search and observability suite that brings order to unstructured data at scale. OpenSearch was forked from Elasticsearch 7.10.2 in 2021. The project is released under the Apache License 2.0, which keeps it truly open source. 

### OpenSearch's Role
OpenSearch is a distributed search and analytics engine built upon Apache Lucene. It's great for ingesting the JSON output from Suricata. OpenSearch serves as the central data store and search engine for the security logs in SOFA. It ingests the structured log data from Apache Kafka, indexes it for really fast searching (or slow if you have 100 people trying to use a single-node cluster), and provides the backend for OpenSearch Dashboards where student analysts can create visualizations and perform the actual security analysis. You can think of OpenSearch as the "database" that holds onto your security data.

### Why OpenSearch?
It's not Elasticsearch. Back in 2023, Elasticsearch hid their LDAP integration behind a paywall. I needed to manage users from across different institutions in Colorado. I was doing so, originally, with FreeIPA before moving on to GLAuth. Elastic decided that they were going to hide the ability to integrate account management with LDAP behind a paywall. So I used OpenSearch instead.
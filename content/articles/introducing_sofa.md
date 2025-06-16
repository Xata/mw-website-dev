Title: Introducing the SOFA Stack!
Author: Maciej
Date: 2025-06-16 15:54
Category: blog
Tags: markdown, blog, sofa, cybersecurity, IT, security

![The SOFA Stack]({static}/img/sofa_on_sofa.jpg)

Introducing **the SOFA stack**!! The SOFA stack is a simple security monitoring platform built using free and open source software. While maybe SOFA is not a complete SIEM, it provides a security data platform for you to monitor network traffic in your organization or home. This is the project that I've been working on here at the Cybersecurity Center at MSU Denver. I started getting a lot of questions about this after being on a panel at NICE 2025.

I’m assuming that you’re curious to know what the SOFA stack is exactly?
Right, well the SOFA stack is made up of Suricata, OpenSearch, FluentBit,
and Apache Kafka. No, I’m not dropping the Apache part. I want the
acronym to be SOFA. I find it really amusing to talk to stakeholders about
it. Mentioning the word sofa makes some people giggle. Anyway, here is the
breakdown of the components of SOFA:

- **Suricata**: High-performance network security monitoring engine that
provides real-time intrusion detection, network security monitoring,
and inline intrusion prevention capabilities.

- **OpenSearch**: Distributed search and analytics engine that enables
fast querying, visualization, and analysis of large volumes of security
data with powerful aggregation capabilities.

- **FluentBit**: Lightweight, high-performance log processor and forwarder
that efficiently collects, processes, and routes data from multiple sources
with minimal resource overhead.

- **Apache Kafka**: Distributed streaming platform that provides reliable,
scalable message buffering and enables decoupling of data producers
from consumers while ensuring data durability and replay capabilities.

A how-to guide (minus all the Centurion Secured bits) is coming soon!
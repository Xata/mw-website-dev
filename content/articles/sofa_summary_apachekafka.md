Title: SOFA Architecture Summary - Apache Kafka
Author: Maciej
Date: 2025-06-17 12:55
Category: blog
Tags: markdown, blog, sofa, cybersecurity, IT, security

Apache Kafka is a distributed streaming platform that acts as the central message broker in SOFA. Apache Kafka is designed to handle high-throughput, fault-tolerant streaming of data between systems. Do we need all the fancy fault-tolerant features of Apache Kafka? Probably not. However, it is a great learning experience for students that work with SOFA. 

Originally, the SOFA stack was the SOF stack, if we're going by acronyms. However, as Centurion Secured started to introduce more community partners with 10 gigabit connections we started getting errors in OpenSearch. The single-node cluster of the original deployment could not keep up. In the new deployment, I introduced Apache Kafka in between the physical collectors and OpenSearch. I think this really matured the pipeline. We were finally able to ingest multiple community partners who had 10 gigabit connections at their organizations.

### Apache Kafka's Role
Earlier I mentioned that Centurion Secured ran into an issue when the project started onboarding more 10 gigabit connections. Apache Kafka is a platform that acts as the central message broker in a SOFA deployment. In the SOFA stack, Apache Kafka effectively serves as a buffer and distribution hub between FluentBit and OpenSearch. FluentBit parses Suricata's output, sends them to Apache Kafka, while OpenSearch consumes these messages for indexing and storage. This decoupling allows each component to operate at its own pace.

Apache Kafka guarantees that once a log is sent to Kafka, it won't be lost even if the individual collector goes down later. It also provides durability guarantees, a lot of the community partners that are a part of the Centurion Secured project are located in some very remote areas. Internet connectivity would be considered mid by people younger than me. That sort of functionality is crucial for security data where losing events could mean missing critical threats.

### Why Apache Kafka?
Apache Kafka lends itself to make the acronym amusing. SOFA is more fun to say than SOFK. This acronym is also catchier. 
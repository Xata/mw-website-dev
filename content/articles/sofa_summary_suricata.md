Title: SOFA Architecture Summary - Suricata
Author: Maciej
Date: 2025-06-17 10:36
Category: blog
Tags: markdown, blog, sofa, cybersecurity, IT, security

SOFA is made up of a few components: A machine running OpenSearch, a machine running OpenSearch Dashboards, a machine running Apache Kafka, and a separate machine/device that runs Suricata and FluentBit. These can be combined or split up in different ways but the simplest SOFA is made up of two physical machines: one running virtual machines that run OpenSearch, OpenSearch Dashboards, and Apache Kafka and then another machine that does the actual traffic inspection with Suricata and log packaging with FluentBit. Let’s look at the different software components and their uses next. In this post we'll go over Suricata or the S part of SOFA.

## Suricata
Suricata is self-described as a high performance, open source network analysis and threat detection software. I,personally, was exposed to Suricata when I was deploying OPNsense at my house. You don’t care about that, you’re reading this because you want to deploy a SOFA in your environment. Sorry. In the SOFA guide (COMING SOON!), I will go over how to deploy Suricata onto a physical machine running Debian.

### Suricata's Role
Suricata’s role in an environment is in an Intrusion Detection System (IDS) or an Intrusion Prevention System (IPS) capacity. The difference between an IDS and an IPS is literally a few lines within Suricata’s configuration. We run Suricata as an IDS passively. We don’t want to interrupt a customer’s business operations or business continuity. If Suricata experiences issues, crashes, or needs any maintenance, your customer’s network operations continue uninterrupted. An IPS deployment, while offering the ability to actively block threats for customers, introduces a potential single point of failure that could disrupt business critical operations. For Centurion Secured, the detection and alerting capabilities of Suricata’s IDS mode, combined with the comprehensive logging we’ll feed into the analytics pipeline, provide a decent enough visibility without the operational risk.

### Why Suricata?
Suricata was specifically chosen for SOFA because of its deployment simplicity. Also, it’s free and open-source under the GNU General Public License. While this is anecdotal, I find that community driven projects really do drive innovation. People are friendly and they really like your contributions to their community. There is an active rule development community that continuously releases rulesets for anyone to use with their Suricata deployment. This is nice because you won’t need to monitor logs yourself and make custom rules for your everything in your environment. You can, but this is
outside the scope of this guide. Beyond the community aspects, Suricata’s multi-threaded architecture makes it very suited for modern hardware. The Centurion Secured project at MSU Denver uses Raspberry Pis to passively inspect traffic on customers’ networks for example. The JSON output format integrates really easily with FluentBit and Apache Kafka, eliminating the need for any complex log parsing. This combination of performance, flexibility, and community support makes it an ideal foundation for SOFA.



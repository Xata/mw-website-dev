Title: SOFA Architecture Summary - FluentBit
Author: Maciej
Date: 2025-06-17 12:52
Category: blog
Tags: markdown, blog, sofa, cybersecurity, IT, security

FluentBit is a super fast, lightweight, and highly scalable logging, metrics, and traces processor and forwarder. FluentBit is also a Cloud Native Computing Foundation (CNCF) graduated project. This is a really useful piece of software. The community made it easy to define the input of whatever you what to forward. Does your Python app export to a .txt file? Cool, FluentBit can forward the contents of that .txt file to a variety of destinations. 

### FluentBit's Role
FluentBit's role in SOFA is to read the JSON output from Suricata and forward it to Apache Kafka. It monitors Suricata's log files and parses the JSON. FluentBit handles the reliable delivery of that data to the rest of the SOFA. Did I mention that it is really simple to define your configuration files? This makes it easier to explain to students what is going on.

### Why FluentBit?
I chose FluentBit because of its efficiency and simplicity. Just kidding, I chose FluentBit because I couldn't find another alternative to LogStash. It's a great choice though, because FluentBit is really simple to use and very efficient. FluentBit is also used by a lot of organizations. This is nice for students because they can add a project from the Cloud Native Computing Foundation to their resumes, as SOFA was originally created to help teach students about security and observability. 
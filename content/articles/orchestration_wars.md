Title: The Orchestration Wars (Or: When Everyone Had Their Own Container Thing)
Author: Maciej
Date: 2025-10-09 16:30
Category: blog
Tags: kubernetes, docker, containers, orchestration, history, nostalgia
Summary: A quick trip down memory lane to when container orchestration wasn't a settled question

# The Orchestration Wars (Or: When Everyone Had Their Own Container Thing)

I've been thinking about the mid-2010s lately. Not because I miss it, but because it's wild how fast things changed in the container orchestration space. For a brief moment in tech history, there were like half a dozen serious contenders for "the way" to run containers in production. Now? It's basically just Kubernetes.

## Why Am I Thinking About This?

Work has been political lately, and it got me thinking about how technology choices eventually just... resolve themselves. Back in 2014-2016, people were having heated arguments about which orchestrator to bet on. Docker Swarm vs Kubernetes vs Mesos vs whatever else was flavor of the month. Now that question seems almost quaint.

But there were some really interesting projects that just didn't make it. Here's a few I remember.

## Docker Swarm

This one actually had a shot. Docker Swarm was Docker's official orchestration solution, and for a while it seemed like the obvious choice. If you were already using Docker (which everyone was), why not just use their built-in clustering?

Swarm was *simple*. That was its whole selling point. You could turn a bunch of Docker hosts into a swarm with like two commands. No YAML manifests, no complex abstractions. Just `docker service create` and you're running distributed containers.

The problem? Kubernetes was more powerful. And once Google threw its weight behind K8s and the CNCF formed, Swarm's simplicity started looking more like "limited features" than "elegant design."

Docker Inc. eventually added Kubernetes support directly into Docker Desktop. Swarm still exists, but it's mostly faded into the background.

## Kontena

I barely remember this one, but Kontena was a Finnish startup's attempt at container orchestration. Their pitch was that they were "developer-friendly" - easier than Kubernetes but more feature-complete than Swarm.

They had some cool ideas. Built-in load balancing, secrets management, and a CLI that didn't make you want to throw your laptop out a window. They even had a nice dashboard before K8s dashboards were really a thing.

Kontena shut down in 2019. The team open-sourced everything and moved on. I think some of them ended up working on k3s or other Kubernetes distributions, which is kind of poetic.

## Tutum

Tutum was a container management platform acquired by Docker in 2015. It was supposed to be this easy "Docker in the cloud" solution. You could deploy containers to AWS or Digital Ocean without thinking too hard about infrastructure.

Docker rebranded it as "Docker Cloud" after the acquisition. Then they killed Docker Cloud in 2018. The whole thing just kind of... evaporated.

I never actually used Tutum myself, but I remember seeing their landing page and thinking "oh that's neat." Then they were gone.

## Singularity by HubSpot

Wait, HubSpot made a container orchestrator? Yeah. For a brief moment, HubSpot (the marketing automation company) built their own container orchestration platform called Singularity.

It was based on Apache Mesos and was actually pretty sophisticated. HubSpot ran their entire production infrastructure on it. They open-sourced it in 2014 and even had some external adoption.

But here's the thing: maintaining an orchestration platform is *hard*. Like, really hard. You need a dedicated team just to keep up with feature requests, bugs, and integration issues. HubSpot eventually migrated to Kubernetes like everyone else and deprecated Singularity.

The repo is still on GitHub if you want to see what could have been.

## What Happened?

Kubernetes won. That's what happened.

It wasn't because K8s was the easiest to use (it definitely wasn't). It wasn't because it had the smoothest developer experience either. It won because:

1. **Google's backing** - Having Google's infrastructure experience behind it was huge
2. **The CNCF** - Neutral governance meant companies could trust the project's long-term stability
3. **Ecosystem** - Once the ecosystem rallied around K8s, the network effects were unstoppable
4. **Extensibility** - K8s is complex, but that complexity is actually powerful if you need it

By 2018-2019, the question wasn't "which orchestrator?" anymore. It was "which Kubernetes distribution?"

## Why This Matters

I think about these projects sometimes when I'm making technology decisions at work. Choosing the "safe" option isn't always wrong. Sometimes the boring choice is boring because it *works* and everyone else figured that out already.

Docker Swarm was simpler. Kontena had better UX. Singularity had some really clever ideas. But Kubernetes had momentum, and in infrastructure tooling, momentum matters more than elegance.

Also, it's a reminder that even huge companies (Docker Inc., HubSpot) had to adapt and change direction. Technology moves fast. What seems like the future one year can become a deprecated GitHub repo the next.

## Conclusion

Anyway, I've been writing a lot of YAML lately and it made me nostalgic for a time when we *almost* had simpler alternatives. But here we are. Kubernetes won the orchestration wars, and now we all write manifests and debug CNI plugins.

I think there's something valuable about remembering these projects though. They pushed the ecosystem forward and experimented with ideas that sometimes found their way into K8s itself. Innovation happens through competition, even if only one project ultimately wins.

Thanks for reading!

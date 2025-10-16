Title: The Orchestration Wars (Or: When Everyone Had Their Own Container Thing)
Author: Maciej
Date: 2025-10-09 16:30
Category: blog
Tags: kubernetes, docker, containers, orchestration, history, nostalgia
Summary: A quick trip down memory lane to when container orchestration wasn't a settled question

# The Orchestration Wars (Or: When Everyone Had Their Own Container Thing)

I've been thinking about the mid-2010s lately. Not because I miss it, but because it's wild how fast things ended up changing in the container orchestration space. For a very brief moment in tech history, there were like half a dozen serious contenders for "the way" to run containers in production. Now? It's basically just Kubernetes.

Still, some IT administrators cringe at the word Kubernetes. However, I don't know if any of them will remember these next few projects (I had to look some of these up):

## Docker Swarm

Docker Swarm was Docker's official orchestration solution. If you were already using Docker (which everyone was at the time), why not just use their built-in clustering?

Swarm was *simple*. That was its whole selling point. You could turn a bunch of Docker hosts into a swarm with like two commands. No YAML manifests, no complex abstractions. Just `docker service create` and you're running distributed containers.

The problem? Kubernetes was more powerful. And once Google threw its weight behind K8s and the CNCF formed, Swarm's simplicity started looking more like "limited features" than "elegant design."

Docker Inc. eventually added Kubernetes support directly into Docker Desktop. Swarm still exists, but it's mostly faded into the background. I wonder when this will eventually fade away from memory (and support)?

## Tutum

Tutum was a container management platform acquired by Docker in 2015. It was supposed to be this easy "Docker in the cloud" solution. You could deploy containers without thinking too hard about infrastructure.

Docker rebranded it as "Docker Cloud" after the acquisition. Then they killed Docker Cloud in 2018. The whole thing just kind of evaporated.

I never actually used Tutum myself (I was too young and trying to do game dev), but I remember seeing their landing page and thinking "oh that's neat." Then they were gone.

## What Happened?

Kubernetes won. That's what happened. I wonder if people wanting to work at Google had anything to do with it?

## Conclusion

Anyway, I've been writing a lot of YAML lately. Kubernetes won the orchestration wars, and now we all write manifests and debug CNI plugins.

I think there's something valuable about remembering these projects though. They pushed the ecosystem forward and experimented with ideas that sometimes found their way into K8s itself. Innovation happens through competition, even if only one project ultimately wins.

Thanks for reading!

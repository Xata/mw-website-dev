Title: Crow SBOM Generation Documentation
Author: Maciej
Date: 2026-04-03 13:23
Category: blog
Tags: markdown, blog, crow, c++, docs, opensource, axios

The Axios supply chain attack this week was a good reminder that knowing what's in your dependency tree isn't optional. A North Korean threat actor hijacked the lead maintainer's npm account and pushed two malicious versions of a library with 100M+ weekly downloads. The poisoned packages dropped a cross-platform RAT and self-destructed after execution.

I've been using Crow (C++ micro web framework) for some personal projects, and after the Axios news I started automating SBOM generation in my CI pipelines with GitHub Actions. Turns out Crow already had SBOM generation built into its CMake config, but it was completely undocumented. There was an open issue from last August with no takers, so I wrote the guide and got it merged.

## Links
- Link to the pull request: https://github.com/CrowCpp/Crow/pull/1172
- Docs page link: https://crowcpp.org/master/guides/sbom/
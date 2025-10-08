Title: Technical Deep Dive: Optimizing Ubiquitous Cube Game
Author: Maciej
Date: 2025-10-07 16:00
Category: blog
Tags: python, opengl, performance, optimization, game-engine, numba, moderngl

![Ubiquitous Cube Game world]({static}/img/cube-game-screenshot-00.jpg)

## Performance is king

I've been working on optimizing the voxel engine for Ubiquitous Cube Game and wanted to share some of the technical decisions that went into making it run at 100+ FPS. When you're rendering thousands of voxels in real-time, every optimization matters. Here's what I learned about squeezing performance out of Python and OpenGL.

## The JIT compilation breakthrough

One of the biggest wins came from using Numba's `@njit` decorator on the hot paths. The mesh building and terrain generation code gets called constantly, so I needed them to run at C-like speeds. Numba's JIT compilation takes Python code and compiles it to native machine code at runtime. For the greedy meshing algorithm alone, I saw a 10x speedup.

Here's the key: you have to design your data structures with Numba in mind. That means using flat NumPy arrays instead of nested Python data structures. Cache efficiency matters when you're processing thousands of chunks.

## Greedy meshing and why it matters

The greedy meshing algorithm is probably the most important optimization in the whole engine. Instead of drawing a cube for every single voxel, we only generate geometry for faces that are adjacent to empty space. If a voxel is completely surrounded by other voxels, we don't waste GPU resources rendering it.

The algorithm "greedily" combines adjacent faces of the same type into larger quads. This reduces the vertex count dramatically. A 32x32x32 chunk could theoretically have 32,768 voxels, but with greedy meshing we're only rendering the surfaces.

## Packing vertex data tight

Memory bandwidth is expensive. I pack 7 vertex attributes into a single `uint32` per vertex. This includes position, normal, texture coordinates, and ambient occlusion data. The GPU unpacks these in the vertex shader using bit manipulation.

```glsl
// Unpack position from packed data
vec3 position = vec3(
    float((packedData >> 0) & 0x3F),
    float((packedData >> 6) & 0x3F),
    float((packedData >> 12) & 0x3F)
);
```

Tighter data means better cache utilization, both on the CPU and GPU sides.

## Chunk system and frustum culling

The world is divided into 32³ voxel chunks. Each chunk gets its own mesh, model matrix, and an "empty" flag for quick rejection. I have 27,000 total chunks managed by the world container (30×3×30 chunks).

But here's the thing: we don't render all 27,000 chunks every frame. Frustum culling tests which chunks are actually visible to the camera using sphere-AABB intersection tests. Only visible chunks get submitted to the GPU. This easily cuts rendering work by 70-80% depending on where you're looking.

## Two-pass rendering for transparency

Water is transparent, but transparency in 3D rendering is tricky. You need to render opaque objects first (with depth writing enabled), then render transparent objects sorted back-to-front (with depth testing but no depth writing).

I implemented a two-pass pipeline:
1. First pass: solid geometry with full depth buffer writes
2. Second pass: transparent water with depth test only

The water shader has some nice effects too - Fresnel reflections, animated wave ripples using time-based UV offsets, and volumetric fog that gets denser with depth. All running in GLSL.

## Cross-platform pain points

Getting this to work on both Windows and macOS was interesting. macOS caps OpenGL at 4.1, which is already deprecated by Apple. Some features I wanted to use just aren't available. I had to create a compatibility layer that works with the lowest common denominator while still using modern OpenGL features like VAOs and VBOs.

Also, ModernGL makes cross-platform development way easier than raw PyOpenGL. I just had to point it at the right OpenGL version and it handles the context creation.

## Why this matters for platform engineering

You might be wondering what a voxel game engine has to do with infrastructure work. Here's the thing: performance optimization is performance optimization. Whether you're optimizing render loops or optimizing Kubernetes resource allocation, the principles are the same:

- Profile first, optimize second. Don't guess where the bottlenecks are.
- Memory layout matters. Cache-friendly data structures make everything faster.
- Batch operations when possible. The GPU wants large batches, and so does your database.
- Spatial partitioning works for voxels and for distributed systems.

I've used the same performance mindset when optimizing Fluent-bit configurations and tuning OpenSearch cluster performance at work. The tools change but the thinking doesn't.

## What's next

Right now I'm working on adding an entity system for dropped items. When you break a block, it should drop as an entity that you can pick up. I also need to add a proper inventory system and a pause menu.

The code is up on GitHub if you want to check it out: [ubiquitous-cube-game](https://github.com/Xata/ubiquitous-cube-game)

Anyway, that's the breakdown. Performance optimization is fun when you can actually see the FPS counter go up. ᕕ( ᐛ )ᕗ

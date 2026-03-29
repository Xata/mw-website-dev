Title: Adding Frutiger Aero Vibes to My Personal Site
Author: Maciej
Date: 2026-03-29
Category: blog
Tags: css, design, nostalgia, frutiger-aero

I've been feeling really nostalgic lately.

I was looking at references for older websites when I stumbled upon [Frutiger Aero Archive](https://frutigeraeroarchive.org/). The site is dedicated to being a digital museum to that glossy, optimistic design language that really dominated the mid-2000s. Everything looked like it was rendered on a translucent surface floating above a nature photograph.

The term "Frutiger Aero" was coined retroactively in 2017 by Sofi Xian of the Consumer Aesthetics Research Institute. Back when the style was actually everywhere, nobody had a name for it. The name combines Adrian Frutiger (whose typeface inspired the humanist sans-serifs of the era, like Segoe UI) with Windows Aero, Microsoft's glossy visual design system for Vista and 7.

There's something genuinely warm (or just nostalgic) about Frutiger Aero. All of the skeuomorphism, the gradients that made buttons feel like physical objects, the way everything had this subtle depth to it. It felt *human* in a way that the recent flat design era intentionally stripped away.

So naturally I wanted to bring some of that vibe to my personal site.

## What I Changed

The site was already pretty minimal: Inter font, clean layout, lots of whitespace. I didn't want to go full 2006 MySpace on it, just wanted to add some subtle Aero touches. Here's everything that I did:

### Glossy Header

The header block now has a layered gradient background with an `::after` pseudo-element acting as a gloss layer: a white-to-transparent fade across the top half. Combined with an inset box-shadow highlight on the top edge and a subtle aqua border, it reads as a glass panel.

### Aqua Gradient Dividers

Every `<hr>` and the header/footer borders use the same gradient:
```css
background: linear-gradient(to right,
    rgba(147,206,222,0) 0%,
    rgba(147,206,222,1) 15%,
    rgba(117,189,209,1) 50%,
    rgba(73,165,191,1) 85%,
    rgba(73,165,191,0) 100%
);
```

The fade-to-transparent at both edges gives it that floating toolbar separator look.

### Pill Nav Buttons

The navigation links are styled as little glossy pill buttons with the same gradient + inset highlight treatment. On hover they shift from neutral glass into an aqua tint.

### Dark Mode

Everything translates to dark mode with dialed-down opacity and muted tones. The gradients go from bright aqua glass to subtle steel-blue surfaces with just enough glow to read as glass without blowing out on a dark background.

## Why?

Honestly? It's just fun. The flat design consensus of the last decade produced clean, readable interfaces, but it also made everything look the same. There's a certain joy in glossy buttons that flat design deliberately killed.

I'm not arguing we should go back to the skeuomorphic leather textures of iOS 6. But a little gloss, a little depth, a little warmth? That feels right for a personal site. This isn't a SaaS dashboard, it should have some personality (although maybe it would be interesting to see a SaaS dashboard with this look).

If you want to go down the rabbit hole yourself, the [Frutiger Aero Archive](https://frutigeraeroarchive.org/) is a fantastic starting point.
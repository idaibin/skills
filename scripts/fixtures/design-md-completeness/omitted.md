---
name: Omitted Example
description: Sanitized omission fixture
omitted:
  - section: spacing
    reason: "This identity has no shared spacing scale; each accepted feature owns layout spacing."
  - section: rounded
    reason: "All shared surfaces are square, so the shared system defines no corner-radius scale."
  - section: components
    reason: "This boundary has no shared component consumers; features own all component styling."
colors:
  primary: "#1A1C1E"
typography:
  body:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
---

## Overview

This deliberately small identity governs only shared color and typography semantics
for otherwise independent feature surfaces.

## Colors

The `primary` token applies to core text and the sole shared emphasis role; feature
owners may not reinterpret it as a status color.

## Typography

The `body` token applies to normal interface copy and establishes the only shared
type contract for this boundary.

## Layout

This identity has no shared spacing scale; each accepted feature owns layout spacing.
The statement limits authority rather than allowing agents to invent a global scale.

## Elevation & Depth

Features may define local depth only through their accepted contracts; this shared
identity does not add a competing elevation vocabulary.

## Shapes

All shared surfaces are square, so the shared system defines no corner-radius scale.
Feature-local shapes remain bounded by their own approved contracts.

## Components

This boundary has no shared component consumers; features own all component styling.
Any future shared consumer must replace this omission with component token entries.

## Do's and Don'ts

Do keep the two shared token groups authoritative. Do not treat omissions as permission
to infer new shared values from implementation adapters.

---
name: Complete Example
description: Sanitized first-adoption fixture
colors:
  primary: "#1A1C1E"
  surface: "#F7F5F2"
typography:
  body:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
spacing:
  sm: 8px
  md: 16px
rounded:
  sm: 4px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
---

## Overview

This restrained system supports dense operational work while preserving a calm,
high-contrast hierarchy for repeated daily use.

## Colors

The `primary` token owns core text and primary-action backgrounds; `surface` owns the
default page and inverse button text so their roles remain stable across surfaces.

## Typography

The `body` token applies to normal interface copy and table content, preserving one
readable family, size, weight, and line-height contract.

## Layout

The `sm` spacing token separates tightly related controls, while `md` separates
independent groups and establishes the shared page rhythm.

## Elevation & Depth

Hierarchy relies on border and color contrast rather than ambient shadows, keeping
dense operational surfaces clear and predictable.

## Shapes

The `sm` rounded token applies to interactive controls and compact containers; larger
surfaces do not invent additional radius values.

## Components

The `button-primary` component entry owns the shared primary action surface, text,
and corner treatment across every consumer and state variant.

## Do's and Don'ts

Do preserve the named semantic roles across surfaces. Do not derive new target values
from current CSS, screenshots, or component defaults without approval.

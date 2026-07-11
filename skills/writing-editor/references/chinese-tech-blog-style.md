# Chinese Personal Technical Blog Style

## Preferred Voice

Use direct, restrained judgment:

```text
我不太建议一开始就上这套。
```

```text
这个方案能跑，但后面会比较难维护。
```

```text
我更倾向先做一个小闭环，而不是把架构一次性铺满。
```

```text
这里真正的问题不是性能，而是边界不清楚。
```

## Preferred Structure

For personal technical posts, prefer:

```text
问题是什么
我试过什么
哪里不舒服
最后怎么选
这个选择的代价
后面怎么扩展
```

Do not default to:

```text
背景
现状
方案
优势
总结
展望
```

Use the second structure only when the user is writing a formal solution document or tutorial.

## Tone Boundary

Allowed:

- Direct
- Restrained
- Opinionated
- Tradeoff-aware
- Project-contextual

Avoid:

- Inspirational ending
- Official-report tone
- Marketing phrasing
- Over-literary prose
- Public-account style uplift

## Useful Editing Moves

- Replace "这个方案可以提升可维护性" with the maintenance boundary only when the source states or proves that boundary; otherwise delete or flag it.
- Replace "具有重要意义" with what the author explicitly says they would do differently; do not invent a preference from the empty phrase.
- Replace broad "AI 能提高效率" claims with the concrete task AI handled.
- Keep uncertainty when uncertainty is real.
- Keep "I did not choose X" when it explains the author's judgment.

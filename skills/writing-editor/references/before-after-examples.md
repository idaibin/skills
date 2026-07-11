# Before And After Examples

These examples include their allowed source context. Do not reuse an `After`
claim when an input draft does not contain equivalent evidence.

## Unsupported Abstract Claim

Source context: none beyond the sentence.

Before:

```text
这个方案可以提升系统的可维护性和扩展性。
```

After: delete the sentence and add no replacement. The source does not identify
which boundary changed or provide maintenance-cost evidence.

## Supported Maintenance Boundary

Source context: the draft states that every new handler currently modifies the
central dispatch branch, while the proposed registry lets handlers register
without changing that branch.

Before:

```text
这个方案可以提升系统的可维护性和扩展性。
```

After:

```text
改成注册表后，新增处理器不再需要修改中央分发分支。
```

## Empty Importance Claim Without Evidence

Source context: none beyond the sentence.

Before:

```text
这在实际项目中具有重要意义。
```

After: delete the sentence and add no replacement. The editor cannot infer what
the author cares about from this sentence.

## Supported AI Product Reflection

Source context: the author's notes explicitly say, `我想验证的是 AI 能不能持续维护这个信息流产品，而不只是生成一篇文章。`

Before:

```text
AI 的发展为信息流产品带来了新的可能性，也为内容生产和分发提供了新的思路。
```

After:

```text
我想验证的是，AI 能不能持续维护这个信息流产品，而不只是生成一篇文章。
```

## Forced Conclusion

Source context: the body contains no resulting judgment or next-step decision.

Before:

```text
综上所述，这次实践让我对 AI 工作流有了更深入的理解，也为后续探索奠定了基础。
```

After: delete the sentence and add no replacement. A template conclusion cannot
support a new author judgment.

## Rewrite Notes

Good edits usually:

- Remove the frame sentence.
- Keep the author's specific problem.
- Turn abstract value into an operational judgment only when the source provides that judgment or its concrete evidence.
- Delete unsupported claims instead of inventing a stronger replacement.
- Avoid adding drama.
- Avoid polishing away technical constraints.

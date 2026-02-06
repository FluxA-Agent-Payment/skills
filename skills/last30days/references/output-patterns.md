# Output Patterns

## Synthesis Guidelines

Ground synthesis in ACTUAL research content, not pre-existing knowledge:
- Use exact product/tool names from sources
- Cite specific quotes and insights
- Match what sources actually say

## Output by Query Type

### RECOMMENDATIONS ("best X", "top X")

Extract SPECIFIC NAMES, not generic patterns:

```
Most mentioned:
1. [Specific name] - mentioned {n}x (r/sub, @handle, blog.com)
2. [Specific name] - mentioned {n}x (sources)
3. [Specific name] - mentioned {n}x (sources)

Notable mentions: [other items with 1-2 mentions]
```

### PROMPTING/NEWS/GENERAL

Show synthesis and patterns:

```
What I learned:

[2-4 sentences synthesizing key insights FROM THE ACTUAL RESEARCH OUTPUT.]

KEY PATTERNS I'll use:
1. [Pattern from research]
2. [Pattern from research]
3. [Pattern from research]
```

## Stats Footer

### Full Mode (with x402 payment)

```
---
All agents reported back!
- Reddit: {n} threads | {sum} upvotes | {sum} comments
- X: {n} posts | {sum} likes | {sum} reposts
- Web: {n} pages | {domains}
- Top voices: r/{sub1}, r/{sub2} | @{handle1}, @{handle2}
```

### Web-Only Mode

```
---
Research complete!
- Web: {n} pages | {domains}
- Top sources: {author1} on {site1}, {author2} on {site2}
```

## Prompt Writing

Match FORMAT that research recommends:
- Research says "JSON prompts" -> Write AS JSON
- Research says "structured parameters" -> Use key: value format
- Research says "natural language" -> Use prose
- Research says "keyword lists" -> Use comma-separated keywords

Format:
```
Here's your prompt for {TARGET_TOOL}:

---

[The actual prompt IN THE FORMAT THE RESEARCH RECOMMENDS]

---

This uses [1-line explanation of research insight applied].
```

---
name: extract-linkedin-leads
description: Extracts LinkedIn profiles of professionals based on search criteria like company, role, industry, or keywords.
parameters:
  type: object
  properties:
    query:
      type: string
      description: |
        The search criteria. Can be:
        - A company name (e.g., "SpaceX", "OpenAI")
        - A role/title (e.g., "AI automation specialist", "software engineer")
        - An industry (e.g., "AI automation", "fintech")
        - A combination (e.g., "machine learning engineer at Google")
  required:
    - query
---

# LinkedIn Lead Extraction Skill

This skill extracts publicly-indexed LinkedIn profile information using web search. It does NOT require LinkedIn login and only accesses information that search engines have indexed.

## How It Works

1. Perform multiple targeted web searches using `site:linkedin.com/in` queries
2. Extract profile information from search result snippets
3. Compile results into a structured Markdown table

## Search Strategy

Run **2-3 parallel searches** with different query patterns to maximize results:

### For Company-Based Searches (e.g., "SpaceX")
```
site:linkedin.com/in "CompanyName" engineer manager director
site:linkedin.com/in "works at CompanyName" OR "working at CompanyName"
site:linkedin.com/in CompanyName "Senior Engineer" OR "Principal Engineer" OR "Lead"
```

### For Role/Industry Searches (e.g., "AI automation")
```
site:linkedin.com/in "AI automation" specialist consultant founder
site:linkedin.com/in "AI automation agency" founder CEO
site:linkedin.com/in "AI automation" engineer developer
```

### For Specific Role + Company
```
site:linkedin.com/in "Role" "Company"
site:linkedin.com/in "Role" at "Company"
```

## Output Format

Present results in a Markdown table with these columns:

| Name | Title/Role | Company | LinkedIn Profile |
|------|-----------|---------|------------------|
| John Doe | Senior Engineer | SpaceX | [Profile](URL) |

## Additional Sections to Include

1. **Summary stats** - Total leads found
2. **Departments/Focus areas** - Group by team or specialty if applicable
3. **Former employees** - Separate table if relevant profiles show they've moved on
4. **Follow-up suggestions** - Offer to search specific sub-niches

## Limitations

- Only returns publicly-indexed information (no emails, phone numbers)
- Limited to ~10-20 results per search query
- Cannot access private profiles or connection-only information
- Results depend on what LinkedIn exposes to search engines

## Example Usage

```
/linkedin-lead-extractor:extract-linkedin-leads query="SpaceX"
/linkedin-lead-extractor:extract-linkedin-leads query="AI automation specialist"
/linkedin-lead-extractor:extract-linkedin-leads query="software engineer at Stripe"
```

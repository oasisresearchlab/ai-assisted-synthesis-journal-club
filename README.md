# ai-assisted-synthesis-journal-club
Prototyping an AI-assisted synthesis journal club

General flow:
1. Define research question
2. Collect relevant papers. This can be sped up with AI tools like Elicit to get a first pass at relevant papers. Getting this into the repo is a manual step for now, into a csv. Later we can automate this more with APIs like [Asta](https://allenai.org/asta/resources/mcp).
3. Extract candidate discourse nodes (claims, evidence, patterns, artifacts) from paper abstracts that might be relevant to the research question. Current script: `scripts/extract-claims-evidence-from-abstracts.py` - this uses an LLM to extract relevant nodes from abstracts based on predefined node types, that are defined by the user with the [Discourse Graph plugin](https://discoursegraphs.com/docs/obsidian/getting-started) for Obsidian, stored in `.obsidian/plugins/discourse-graph/data.json`.
4. Verify and formalized candidate nodes. This is currently a primarily manual step, using the Discourse Graph plugin UI. There is some experimental support for using LLMs to help verify and formalize claims via API connections to a local Zotero library, see `scripts/verify-and-formalize-claims.py`. 
5. Synthesize high-level claims and patterns across papers. This is the journal club step! :) The idea is for participants to do step 3 and 4 for a set of papers, then bring the resulting nodes to a synthesis journal club where they can discuss and collaboratively synthesize high-level claims and patterns across papers, e.g., using the Discourse Graph plugin canvas.

See more plans in `plan.md`
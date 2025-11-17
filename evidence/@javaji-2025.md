# Can AI Validate Science? Benchmarking LLMs for Accurate Scientific Claim → Evidence Reasoning

**Authors:** Shashidhar Reddy Javaji, Yupeng Cao, Haohang Li, Yangyang Yu, Nikhil Muralidhar, Zining Zhu
**Year:** 2025
**DOI:** 10.48550/arXiv.2506.08235
**Citation Count:** 1

## Evidence Items

- Closed-source models (GPT-4 and Claude) consistently outperformed open-source models in both precision and recall metrics for scientific claim-evidence identification tasks #evd-candidate ^evd-001
	- **What**: Precision and recall scores for claim-evidence identification tasks across different model types
	- **How**: Comparative evaluation across six diverse LLMs using systematic benchmarking on scientific content
	- **Who**: GPT-4, Claude (closed-source) vs. open-source counterparts evaluated on CLAIM-BENCH dataset
- Strategically designed three-pass and one-by-one prompting approaches significantly improved LLMs' abilities to accurately link dispersed evidence with claims #evd-candidate ^evd-002
	- **What**: Performance improvements in accuracy of linking evidence to claims using different prompting strategies
	- **How**: Three divide-and-conquer inspired prompting approaches tested: three-pass and one-by-one methods compared against baseline
	- **Who**: Six diverse LLMs tested on over 300 claim-evidence pairs across multiple research domains
- LLMs demonstrated significant limitations in processing complex scientific content across multiple research domains #evd-candidate ^evd-003
	- **What**: Performance deficits and failure modes when handling complex scientific argumentation and content
	- **How**: Comprehensive benchmark evaluation measuring claim-evidence extraction and validation capabilities
	- **Who**: Six LLMs evaluated on CLAIM-BENCH containing over 300 claim-evidence pairs from multiple research domains
- Advanced prompting strategies improved performance but came at increased computational cost #evd-candidate ^evd-004
	- **What**: Trade-off between improved accuracy metrics and computational resource requirements
	- **How**: Comparison of computational costs between standard prompting and strategically designed three-pass/one-by-one approaches
	- **Who**: LLMs tested using different prompting strategies on scientific claim-evidence tasks
- Model-specific strengths and weaknesses in scientific comprehension were identified through systematic comparison #evd-candidate ^evd-005
	- **What**: Differential performance patterns and capability profiles across different LLM architectures
	- **How**: Systematic comparison using three divide-and-conquer inspired approaches across diverse model types
	- **Who**: Six diverse LLMs including both closed-source (GPT-4, Claude) and open-source models
- The ability to understand intricate relationships within complex research papers, specifically logical links between claims and supporting evidence, remains largely unexplored territory for current LLMs #evd-candidate ^evd-006
	- **What**: Gap in current LLM capabilities for processing complex logical relationships in scientific literature
	- **How**: Evaluation of LLMs' performance on tasks requiring deep comprehension of scientific argumentation structure
	- **Who**: Current state-of-the-art LLMs evaluated on scientific papers requiring complex reasoning about claim-evidence relationships

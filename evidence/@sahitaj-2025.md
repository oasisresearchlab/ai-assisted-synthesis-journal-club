# Towards Automated Fact-Checking of Real-World Claims: Exploring Task Formulation and Assessment with LLMs

**Authors:** Premtim Sahitaj, Iffat Maab, Junichi Yamagishi, Jawan Kolanowski, Sebastian Möller, Vera Schmitt
**Year:** 2025
**DOI:** 10.48550/arXiv.2502.08909
**Citation Count:** 5

## Evidence Items

- Larger LLMs consistently outperformed smaller LLMs in both classification accuracy and justification quality, with statistical significance confirmed by Friedman tests (p < 0.05) across model sizes #evd-candidate ^evd-001
	- **What**: Classification accuracy (F1 scores), justification quality (TIGERScore), statistical significance tests
	- **How**: Comparative evaluation across three classification schemes (binary, 3-class, 5-class), Friedman tests with Conover's post-hoc tests, three-run majority voting for stochastic outputs
	- **Who**: Llama-3 models of varying sizes (3B, 8B, 70B parameters) tested on 17,856 PolitiFact claims from 2007-2024
- Evidence integration significantly improved performance across all models (p < 0.01), with larger models benefiting most despite smaller models showing relatively greater proportional gains #evd-candidate ^evd-002
	- **What**: F1 score improvements and TIGERScore gains when adding retrieved evidence to claim-only inputs
	- **How**: Paired t-tests comparing with/without evidence conditions across all classification schemes, web search evidence retrieval excluding known fact-checking sites
	- **Who**: All Llama-3 model sizes (3B, 8B, 70B) evaluated on political claims from PolitiFact dataset
- Smaller LLMs (3B parameters) in one-shot scenarios provided comparable performance to fine-tuned Small Language Models, while larger LLMs (70B) consistently surpassed fine-tuned baselines #evd-candidate ^evd-003
	- **What**: Classification accuracy and F1 scores comparing instruction-tuned LLMs vs fine-tuned ModernBERT-large (395M trainable parameters)
	- **How**: Baseline comparison using fine-tuned ModernBERT-large across four input configurations (claim-only, +context, +source, +evidence) vs one-shot LLM performance
	- **Who**: Llama-3 series models vs ModernBERT-large trained on PolitiFact claims with different input feature combinations
- Binary classification achieved highest overall performance across all models, while distinguishing between nuanced labels in 5-class schemes remained challenging with lower accuracy scores #evd-candidate ^evd-004
	- **What**: Comparative accuracy and F1 scores across binary, 3-class, and 5-class labeling schemes
	- **How**: Friedman test across three classification schemes showing significant differences (p < 0.05), with structured JSON output parsing for verdicts
	- **Who**: All tested models evaluated on PolitiFact claims using original PolitiFact label definitions aggregated into different schemes
- The 3B model struggled to outperform baselines significantly, indicating limited capacity for complex automated fact-checking tasks compared to larger variants #evd-candidate ^evd-005
	- **What**: Classification performance metrics and statistical comparisons against baseline performance
	- **How**: Performance evaluation across multiple labeling schemes with baseline comparisons and significance testing
	- **Who**: Llama-3.2-3B model tested on PolitiFact political claims dataset
- TIGERScore gains from evidence integration were statistically significant (p < 0.05) for justification quality, while F1 score gains showed no significant difference (p = 0.167) across model sizes #evd-candidate ^evd-006
	- **What**: TIGERScore values for justification quality and F1 score improvements when adding evidence
	- **How**: Friedman tests on performance gains, three-run averaging for TIGERScore due to generative metric variability
	- **Who**: All Llama-3 model sizes evaluated using 13B TIGERScore model with default hyperparameters
- Evidence retrieval provided the most significant performance improvements across all label schemes, with moderate benefits from speaker information and minimal gains from contextual information #evd-candidate ^evd-007
	- **What**: Incremental performance gains measured across different input feature combinations
	- **How**: Sequential addition of features (context, source entity, evidence) with performance measurement at each step
	- **Who**: Fine-tuned ModernBERT-large models trained on PolitiFact dataset with systematic feature ablation
- LLM-based systems showed susceptibility to hallucinations in generated justifications, requiring extensive evaluation for reliable deployment #evd-candidate ^evd-008
	- **What**: Qualitative observations of hallucinated content in model-generated explanations and reasoning
	- **How**: Analysis of generated JSON outputs containing reasoning, verdict, and explanation components
	- **Who**: All tested Llama-3 models generating structured justifications for political fact-checking claims

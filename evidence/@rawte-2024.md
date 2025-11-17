# FACTOID: FACtual enTailment fOr hallucInation Detection

**Authors:** Vipula Rawte, S. M. Towhidul, Islam Tonmoy, Krishnav Rajbangshi, Shravani Nag, Aman Chadha, Amit P. Sheth, Amitava Das, Joe Biden
**Year:** 2024
**DOI:** 10.48550/arXiv.2403.19113
**Citation Count:** 7

## Evidence Items

- A multi-task learning framework for Factual Entailment achieved 40% improvement in accuracy over state-of-the-art textual entailment methods #evd-candidate ^evd-001
	- **What**: Accuracy improvement percentage comparing factual entailment vs traditional textual entailment methods
	- **How**: Multi-task learning framework incorporating long text embeddings (e5-mistral-7b-instruct, GPT-3, SpanBERT, RoFormer) evaluated against existing TE baselines
	- **Who**: FACTOID benchmark dataset containing 2 million text pairs for claim-evidence evaluation
- Factual entailment scored 0.665 average performance compared to 0.32 for traditional entailment across hallucination types #evd-candidate ^evd-002
	- **What**: Performance scores on hallucination detection across different categories (number-related, time-related, location-related)
	- **How**: Comparative evaluation measuring factual entailment performance against traditional textual entailment methods
	- **Who**: HiLT dataset containing 7,275 number-related, 7,500 time-related, and 13,000 location-related hallucination sentences
- 15 modern large language models were ranked using an automated Hallucination Vulnerability Index across 2,500 test prompts #evd-candidate ^evd-003
	- **What**: Hallucination vulnerability rankings and automated HVI_auto scores for each LLM
	- **How**: Automated assessment using factual entailment method on standardized prompt set, replacing manual annotation approach
	- **Who**: 15 LLMs including GPT-4, GPT-3.5, Falcon, LLaMA, BLOOM, Alpaca, Vicuna, and others tested on HiLT dataset prompts
- Temporal hallucination classification achieved only 66% performance, representing the most challenging hallucination type #evd-candidate ^evd-004
	- **What**: Classification accuracy scores for different hallucination categories with temporal issues showing lowest performance
	- **How**: Category-specific performance analysis within the factual entailment framework
	- **Who**: Time-related hallucination subset from HiLT dataset containing approximately 7,500 sentences from Time Wrap category
- Long text embeddings with 8K to 32K token limits were successfully integrated into the multi-task learning architecture #evd-candidate ^evd-005
	- **What**: Token processing capacity and embedding integration success rates in the MTL framework
	- **How**: Implementation of state-of-the-art long text embedding models within multi-task learning architecture using cross-entropy and dice loss functions
	- **Who**: Various embedding models including e5-mistral-7b-instruct, GPT-3, SpanBERT, and RoFormer tested on factual entailment tasks
- FACTOID dataset extended HiLT with synthetic expansion from 129K annotated hallucination sentences to 2 million text pairs #evd-candidate ^evd-006
	- **What**: Dataset size scaling metrics and synthetic data generation ratios for training factual entailment models
	- **How**: Synthetic extension methodology applied to existing HiLT dataset, expanding factually correct sentences alongside hallucination examples
	- **Who**: Original HiLT dataset with 492K total sentences (129K hallucination-annotated, 364K factually correct) expanded to create FACTOID benchmark

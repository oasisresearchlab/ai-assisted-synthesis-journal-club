# Surprising Efficacy of Fine-Tuned Transformers for Fact-Checking over Larger Language Models

**Authors:** Vinay Setty
**Year:** 2024
**DOI:** 10.1145/3626772.3661361
**Citation Count:** 13

## Evidence Items

- Fine-tuned XLM-RoBERTa-Large outperformed large language models (GPT-4, GPT-3.5-Turbo, Mistral-7b) for claim detection and veracity prediction across most languages, achieving superior performance in 37 out of 48 tested languages. #evd-candidate ^evd-001
	- **What**: Macro-F1 and Micro-F1 scores for claim detection and veracity prediction tasks across multiple languages
	- **How**: Comparative evaluation using fine-tuned transformer models against LLMs with prompt engineering across 90+ languages
	- **Who**: XLM-RoBERTa-Large, GPT-4, GPT-3.5-Turbo, and Mistral-7b models tested on Factiverse dataset translated into 114 languages
- GPT-3.5-Turbo demonstrated superior performance compared to GPT-4 and other models in question decomposition tasks for evidence retrieval, outperforming even the more advanced GPT-4 model. #evd-candidate ^evd-002
	- **What**: Performance scores for question decomposition effectiveness in generating queries for evidence retrieval
	- **How**: Comparison of generative task performance across different models using question decomposition evaluation
	- **Who**: GPT-3.5-Turbo, GPT-4, Mistral-7b, and fine-tuned T5-3b model evaluated on evidence retrieval query generation
- FinQA-RoBERTa-Large, specialized for numerical reasoning, outperformed general models including XLM-RoBERTa-Large for verifying numerical claims in fact-checking tasks. #evd-candidate ^evd-003
	- **What**: Comparative performance metrics for numerical claim verification accuracy
	- **How**: Head-to-head comparison between domain-specialized model and general-purpose fine-tuned model on numerical claims
	- **Who**: FinQA-RoBERTa-Large (fine-tuned on FinQA dataset) vs XLM-RoBERTa-Large tested on numerical claims from Factiverse dataset
- Mistral-7b consistently performed as the worst-performing model overall across claim detection and veracity prediction tasks, while unexpectedly showing better performance than OpenAI models for numerical claim question decomposition. #evd-candidate ^evd-004
	- **What**: Relative ranking performance across different fact-checking subtasks (claim detection, veracity prediction, question decomposition)
	- **How**: Multi-task comparative evaluation measuring performance consistency across different components of fact-checking pipeline
	- **Who**: Mistral-7b compared against GPT-4, GPT-3.5-Turbo, and fine-tuned transformer models on Factiverse multilingual dataset
- Fine-tuned XLM-RoBERTa-Large maintained consistent superior performance across all question generation methods for natural language inference tasks, regardless of how evidence queries were constructed. #evd-candidate ^evd-005
	- **What**: Natural language inference accuracy scores across different evidence retrieval question generation approaches
	- **How**: Systematic evaluation of NLI performance while varying the method used to generate evidence-gathering questions
	- **Who**: XLM-RoBERTa-Large NLI model tested against multiple question generation methods (GPT-3.5-Turbo, GPT-4, Mistral-7b, T5-3b) on claim-evidence pairs
- GPT-4 achieved best performance in only 3 specific languages (Swedish, Albanian, and Georgian) out of the 48 languages tested, despite being the most advanced LLM in the comparison. #evd-candidate ^evd-006
	- **What**: Language-specific performance rankings and win rates across multilingual fact-checking tasks
	- **How**: Language-by-language comparative analysis of model performance using Macro-F1 scores across 90+ languages
	- **Who**: GPT-4 compared against XLM-RoBERTa-Large and other models on Google Translate-generated multilingual versions of Factiverse dataset
- Class imbalance was observed in both claim detection and veracity prediction tasks, requiring the use of Macro-F1 and Micro-F1 metrics to properly evaluate model performance. #evd-candidate ^evd-007
	- **What**: Distribution of positive/negative classes in claim detection and supported/refuted labels in veracity prediction
	- **How**: Statistical analysis of label distributions necessitating balanced evaluation metrics (Macro-F1 and Micro-F1) instead of simple accuracy
	- **Who**: Factiverse production dataset containing real-world claims with inherent class imbalances in check-worthiness and veracity labels
- The study used real-world production data from Factiverse rather than synthetic datasets, with claims translated across 114 languages using Google Translate API for multilingual evaluation. #evd-candidate ^evd-008
	- **What**: Dataset composition including claim types, language coverage, and translation quality for multilingual fact-checking
	- **How**: Production data collection from live fact-checking system with systematic translation pipeline using Google Translate API
	- **Who**: Factiverse production system users generating real-world claims, with evaluation conducted across 114 language translations

# Are Machines Better at Complex Reasoning? Unveiling Human-Machine Inference Gaps in Entailment Verification

**Authors:** Soumya Sanyal, Tianyi Xiao, Jiacheng Liu, Wenya Wang, Xiang Ren
**Year:** 2024
**DOI:** 10.48550/arXiv.2402.03686
**Citation Count:** 12

## Evidence Items

- GPT-4 achieved the highest overall performance with a macro-F1 score of 0.75 on average across entailment verification tasks, outperforming all other models tested including both task-finetuned and instruction-finetuned alternatives. #evd-candidate ^evd-001
	- **What**: Macro-F1 scores across multiple entailment verification datasets, with GPT-4 scoring 0.75 on average
	- **How**: Binary classification evaluation using macro-F1 metric to handle label imbalances, tested across 10 datasets from NLI, contextual QA, and rationale domains
	- **Who**: GPT-4 compared against RoBERTa, Entailer-11B, Flan-T5-xxl, GPT-3.5, UL2, Codex-001, LaMDA-137B, and ChatGPT on WaNLI, FEVER, ANLI, CosQA, SIQA, DREAM, BoolQ, RACE, Entailer, and ECQA datasets
- Instruction-finetuned models systematically outperformed task-finetuned models on entailment verification, with GPT-4 achieving 0.79 macro-F1 and outperforming the best open-source model Flan-T5-xxl by 0.08 macro-F1 points. #evd-candidate ^evd-002
	- **What**: Comparative macro-F1 performance scores between instruction-finetuned models (rows 3-5) versus task-finetuned models (rows 1-2), with specific 0.08 point advantage
	- **How**: Direct performance comparison using the same evaluation benchmark and metrics across different model training approaches
	- **Who**: Task-finetuned models (RoBERTa, Entailer-11B) versus instruction-finetuned models (Flan-T5-xxl, GPT-3.5, GPT-4) evaluated on the compiled EV benchmark
- AI systems demonstrated superior performance to humans on complex multi-hop reasoning tasks, while humans outperformed AI on simple deductive reasoning requiring substitutions and negations. #evd-candidate ^evd-003
	- **What**: Performance differences between humans and AI across different reasoning complexity levels, with AI excelling at complex reasoning (R2) and humans at simple reasoning (R1)
	- **How**: Human evaluation conducted on 1000 randomly sampled instances (100 per dataset) using Amazon Mechanical Turk, with reasoning complexity categorization and comparative analysis
	- **Who**: Human annotators via MTurk compared against GPT-4, Flan-T5-xxl, and other LLMs on the 10-dataset benchmark spanning multiple reasoning types
- Task-specific finetuned models showed poor generalization across dataset categories, performing well within their training category but failing to transfer to unseen categories. #evd-candidate ^evd-004
	- **What**: Within-category versus cross-category performance metrics showing strong performance degradation when models encounter unseen dataset types
	- **How**: Cross-dataset evaluation comparing model performance on datasets from the same category versus different categories (NLI, contextual QA, rationales)
	- **Who**: Task-finetuned models including RoBERTa and Entailer-11B evaluated across the three dataset categories in the EV benchmark
- Ranking-based finetuning outperformed classification-based finetuning, particularly on contextual QA datasets, by learning softer decision boundaries for entailment verification. #evd-candidate ^evd-005
	- **What**: Performance comparison between two training objective approaches, with ranking-based showing superior results especially in contextual QA domain
	- **How**: Comparative evaluation of Flan-T5-xxl models trained with classification objectives versus ranking objectives that learn to rank most supported hypotheses
	- **Who**: Flan-T5-xxl models with different training approaches evaluated on contextual QA datasets including CosQA, SIQA, DREAM within the EV benchmark
- Finetuned Flan-T5 filtering of inconsistent model-generated explanations resulted in a 6% accuracy improvement on average across three multiple-choice question datasets. #evd-candidate ^evd-006
	- **What**: 6% average accuracy improvement across three MCQ datasets when using entailment verification to filter unfaithful explanations
	- **How**: Self-consistency decoding enhanced with finetuned Flan-T5 model filtering out non-entailed reasoning chains before prediction aggregation
	- **Who**: Three multiple-choice question datasets with model-generated explanations filtered using the ranking-finetuned Flan-T5-xxl model
- Humans outperformed all baseline LLMs except GPT-4 on the entailment verification benchmark, with four datasets (ANLI, CosQA, SIQA, Entailer) showing >0.1 absolute macro-F1 difference between humans and models. #evd-candidate ^evd-007
	- **What**: Macro-F1 performance scores showing human superiority over most LLMs, with >0.1 absolute difference on 4 out of 10 datasets
	- **How**: Direct performance comparison using macro-F1 scores between human annotations and model predictions on the same 1000-instance subset
	- **Who**: Human annotators via Amazon Mechanical Turk compared against RoBERTa, Entailer-11B, Flan-T5-xxl, GPT-3.5, and other baseline LLMs on ANLI, CosQA, SIQA, and Entailer datasets
- GPT-4 demonstrated superior performance on entity-grounded reasoning and complex deductive reasoning tasks, while humans showed greater consistency on commonsense reasoning scenarios. #evd-candidate ^evd-008
	- **What**: Task-specific performance differences with GPT-4 excelling in entity-grounded knowledge tasks and humans performing better on commonsense reasoning
	- **How**: Reasoning type categorization and analysis comparing human versus GPT-4 performance across different reasoning complexity levels (R1-R4)
	- **Who**: GPT-4 versus human annotators evaluated on reasoning tasks categorized as simple reasoning (R1), complex reasoning (R2), commonsense reasoning (R3), and entity-grounded reasoning (R3 ANLI)

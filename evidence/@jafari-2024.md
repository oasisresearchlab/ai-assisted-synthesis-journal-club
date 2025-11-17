# Robust Claim Verification Through Fact Detection

**Authors:** Nazanin Jafari, James Allan
**Year:** 2024
**DOI:** 10.48550/arXiv.2407.18367
**Citation Count:** 2

## Evidence Items

- FactDetect improves supervised claim verification models by 15% on F1 score across challenging scientific datasets #evd-candidate ^evd-001
	- **What**: F1 score improvements of 15% when FactDetect is incorporated into supervised models
	- **How**: Multi-task learning approach with FactDetect for short fact generation, evaluated across multiple runs with cross-entropy loss optimization
	- **Who**: Transformer-based encoders (≤1B parameters) tested on SciFact, HealthVer, and SciFact-Open scientific claim verification datasets
- AugFactDetect shows 17.3% average performance gain over baselines in zero-shot settings with statistical significance #evd-candidate ^evd-002
	- **What**: Average 17.3% performance improvement in F1 scores with statistical significance across three datasets
	- **How**: Zero-shot prompting strategy using in-context learning with LLMs, comparing AugFactDetect against baseline prompting methods
	- **Who**: FlanT5-XXL and GPT-3.5 models evaluated on SciFact, SciFact-Open, and HealthVer datasets
- Longformer + FactDetect achieves 32.7% F1 improvement on HealthVer in few-shot settings but only 3.0% on SciFact #evd-candidate ^evd-003
	- **What**: F1 score improvements of 32.7% for HealthVer and 3.0% for SciFact when combining Longformer with FactDetect
	- **How**: Few-shot learning (k=5) with multi-task training approach, comparing performance with and without FactDetect integration
	- **Who**: Longformer encoder model tested on HealthVer (COVID-19 claims) and SciFact (biomedical literature claims) datasets
- AugFactDetect produces differential improvements across LLMs: 28.1% for Llama2-13B, 12.7% for Mistral-7B, and 11.3% for GPT-3.5 #evd-candidate ^evd-004
	- **What**: F1 score gains varying significantly by model: 28.1% (Llama2-13B), 12.7% (Mistral-7B), 11.3% (GPT-3.5)
	- **How**: Zero-shot prompting evaluation comparing AugFactDetect against best-performing baseline strategies across different LLM architectures
	- **Who**: Three different LLMs (Llama2-13B, Mistral-7B, GPT-3.5) tested on SciFact, SciFact-Open, and HealthVer datasets
- SciFact-Open dataset shows lower overall performance compared to other datasets due to increased complexity #evd-candidate ^evd-005
	- **What**: Consistently lower performance metrics across all models when evaluated on SciFact-Open compared to SciFact and HealthVer
	- **How**: Zero-shot evaluation using models trained on SciFact training data, comparing performance across three different scientific claim verification datasets
	- **Who**: All tested models evaluated on SciFact-Open dataset containing claims with both supporting and contradicting evidence sentences
- Longformer + FactDetect achieves best performance across all three datasets in full training setup, matching MULTIVERS baseline #evd-candidate ^evd-006
	- **What**: Highest F1 scores, accuracy, and AUC metrics achieved when FactDetect is integrated with Longformer encoder in supervised settings
	- **How**: Full supervised training with multi-task learning approach, comparing integrated FactDetect models against state-of-the-art MULTIVERS baseline
	- **Who**: Longformer encoder with FactDetect integration tested against MULTIVERS baseline on SciFact, HealthVer, and SciFact-Open datasets
- Models with parameters not exceeding 1 billion show competitive performance when enhanced with FactDetect approach #evd-candidate ^evd-007
	- **What**: Performance metrics (F1, accuracy, AUC) from models constrained to ≤1B parameters showing competitive results with FactDetect enhancement
	- **How**: Supervised training on NVIDIA RTX8000 GPU with learning rate 2e-5 over 25 epochs, comparing enhanced smaller models against larger baselines
	- **Who**: Transformer-based encoders with ≤1B parameters trained and evaluated on three scientific claim verification datasets
- Zero-shot claim verification through LLMs shows significant improvement when augmented with short fact generation compared to standard prompting #evd-candidate ^evd-008
	- **What**: Macro F1 scores, accuracy, and AUC measurements showing superior performance of AugFactDetect over other prompting strategies
	- **How**: In-context learning evaluation using multiple prompting strategies, with results averaged over 5 runs for statistical reliability
	- **Who**: Large Language Models (FlanT5-XXL, GPT-3.5) evaluated on expert-annotated scientific claims from biomedical literature and COVID-19 domains

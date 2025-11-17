# Improving the fact-checking performance of language models by relying on their entailment ability

**Authors:** Gaurav Kumar, Debajyoti Mazumder, Ayush Garg, Jasabanta Patro
**Year:** 2025
**DOI:** 10.48550/arXiv.2505.15050
**Citation Count:** 0

## Evidence Items

- Training language models with entailed justifications (TBE-3) significantly outperformed baseline models, achieving improvements of up to 28.57% on LIAR-RAW and 44.26% on RAW-FC datasets in macro-F1 scores. #evd-candidate ^evd-001
	- **What**: Macro-F1 performance improvements measured as percentage gains over baseline models
	- **How**: Three-step training approach: evidence classification as supporting/refuting, justification generation, then fine-tuning models on claims with generated justifications using LoRA and LoRA+ adapters
	- **Who**: Multiple AI systems (RoBERTa, XLNet, Mistral, Llama, Gemma, Qwen, Falcon) tested on LIAR-RAW and RAW-FC English fact-checking datasets
- Training with prompted claim-evidence understanding (TBE-2) showed moderate effectiveness, registering improvements up to 16.39% over baselines on the RAW-FC dataset. #evd-candidate ^evd-002
	- **What**: Macro-F1 score improvements measured as percentage gains compared to baseline performance
	- **How**: Training approach using prompted understanding of claim-evidence relationships before veracity prediction, compared against existing baseline models
	- **Who**: Encoder-based language models (ELMs) like RoBERTa, XLNet and generative language models (GLMs) like Mistral, Llama tested on RAW-FC dataset
- Training with raw evidence sentences produced smaller but measurable improvements, achieving up to 8.20% improvement in macro-F1 over baselines on the RAW-FC dataset. #evd-candidate ^evd-003
	- **What**: Macro-F1 performance scores showing modest percentage improvements over baseline models
	- **How**: Direct training approach using unprocessed evidence sentences without additional prompting or justification generation steps
	- **Who**: Language models trained and evaluated on RAW-FC dataset containing news claims with associated evidence
- Ablation studies revealed that both supporting and refuting justifications are crucial for maintaining model performance, with removal of either type adversely affecting accuracy scores. #evd-candidate ^evd-004
	- **What**: Performance degradation measured when individual justification components were systematically removed from the model
	- **How**: Controlled ablation experiments removing supporting justifications, refuting justifications, or both, then measuring resulting performance changes
	- **Who**: Models trained using the TBE-3 approach tested on LIAR-RAW and RAW-FC datasets
- Linguistic analysis demonstrated that encoder-based language models (ELMs) focused more accurately on important factual words and signals indicating claim support or contradiction. #evd-candidate ^evd-005
	- **What**: Attention pattern analysis showing model focus on factually relevant linguistic elements
	- **How**: Attention visualization and analysis to identify which words and phrases models weighted most heavily during entailment decisions
	- **Who**: ELMs (RoBERTa, XLNet) analyzed on samples from LIAR-RAW and RAW-FC datasets
- Human evaluation of Llama-generated explanations found them to be informative, readable, and logically structured across five assessment dimensions. #evd-candidate ^evd-006
	- **What**: Qualitative ratings on informativeness, accuracy, readability, objectivity, and logicality of AI-generated explanations
	- **How**: Three independent human annotators evaluated 40 randomly selected samples using standardized assessment criteria
	- **Who**: Llama model explanations evaluated by human annotators on samples from both LIAR-RAW and RAW-FC datasets
- Inference-based experiments (IBEs) using direct prompting of generative language models for veracity prediction showed effectiveness but performed less well than training-based approaches. #evd-candidate ^evd-007
	- **What**: Comparative performance scores between inference-based prompting and training-based fine-tuning approaches
	- **How**: Four inference-based experiments prompting GLMs directly for veracity prediction without additional training, compared against training-based experimental results
	- **Who**: Generative language models (Mistral, Llama, Gemma, Qwen, Falcon) tested via prompting on LIAR-RAW and RAW-FC datasets
- The proposed approach achieved superior performance compared to existing state-of-the-art models including HiSS, FactLLaMa, RAFTS, and L-Defence on standard fact-checking benchmarks. #evd-candidate ^evd-008
	- **What**: Macro-F1 scores comparing the new approach against established baseline models in the fact-checking domain
	- **How**: Direct performance comparison using identical evaluation metrics and datasets against previously published results from competing approaches
	- **Who**: Multiple language model architectures compared against HiSS, FactLLaMa, RAFTS, and L-Defence models on LIAR-RAW and RAW-FC datasets

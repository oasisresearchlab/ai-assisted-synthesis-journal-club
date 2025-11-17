# WiCE: Real-World Entailment for Claims in Wikipedia

**Authors:** Ryo Kamoi, Tanya Goyal, Juan Diego Rodriguez, Greg Durrett
**Year:** 2023
**DOI:** 10.48550/arXiv.2303.01432
**Citation Count:** 109

## Evidence Items

- T5-3B trained on ANLI achieved 64.3 F1 score at claim-level entailment classification, substantially lower than human performance of 83.3 F1 #evd-candidate ^evd-001
	- **What**: F1 scores for claim-level entailment classification performance
	- **How**: Comparative evaluation of fine-tuned T5-3B model against human annotators on three-way classification (SUPPORTED, PARTIALLY-SUPPORTED, NOT-SUPPORTED)
	- **Who**: T5-3B model fine-tuned on ANLI dataset vs. human annotators on 50 randomly selected test claims from WICE dataset
- GPT-4 demonstrated stronger entailment classification performance than the best fine-tuned subclaim-level models, but struggled with claim-level classification even with oracle retrieval #evd-candidate ^evd-002
	- **What**: Comparative performance scores between GPT-4 and fine-tuned models on subclaim vs. claim-level tasks
	- **How**: Few-shot prompting evaluation on oracle retrieval dataset with structured XML output format
	- **Who**: GPT-4-0613 model tested on first 100 claims/subclaims of oracle retrieval dataset from WICE
- Chunk-level T5-3B model fine-tuned on WICE after ANLI training achieved best performance at both claim and subclaim granularity levels #evd-candidate ^evd-003
	- **What**: Performance metrics (F1, accuracy) across different model configurations and granularity levels
	- **How**: Sequential fine-tuning approach with chunk-level document processing (256 token partitions) and comparative evaluation
	- **Who**: T5-3B models tested on WICE dataset with various fine-tuning configurations (ANLI+WICE vs. WICE-only)
- Models fine-tuned with evidence context (128 additional tokens) significantly outperformed those without context in retrieve-then-predict strategies #evd-candidate ^evd-004
	- **What**: Performance improvements measured through F1 scores and accuracy metrics
	- **How**: Ablation study comparing models with and without evidence context in format 'claim <SEP> evidence-context <SEP> evidence-sentence'
	- **Who**: T5 models evaluated on WICE dataset using retrieval-based approach with BM25 retrieval system
- Off-the-shelf NLI models (RoBERTa-Large, ALBERT-xLarge, T5-Large, T5-3B) showed poor performance when applied to real-world Wikipedia claims using stretching paradigm #evd-candidate ^evd-005
	- **What**: F1 scores, accuracy, and AUROC metrics for multiple transformer models
	- **How**: Stretching technique evaluation where models trained on short-paragraph datasets (SNLI, MNLI, DocNLI, ANLI) were applied to document-level entailment
	- **Who**: Pre-trained transformer models tested on WICE dataset derived from Wikipedia claims and cited web articles
- Oracle retrieval experiments revealed large performance gaps, suggesting that better retrieval systems could substantially improve entailment classification performance #evd-candidate ^evd-006
	- **What**: Performance differential measurements between oracle (perfect) retrieval and actual retrieval system results
	- **How**: Controlled comparison using oracle chunks containing all gold supporting sentences vs. BM25-based retrieval system
	- **Who**: Various models tested on oracle retrieval dataset constructed from WICE with balanced number of oracle chunks per claim
- Models demonstrated significant domain shift challenges when moving from existing NLI datasets to real-world Wikipedia claims, with substantial performance drops #evd-candidate ^evd-007
	- **What**: Cross-dataset performance comparisons and generalization metrics
	- **How**: Comparative evaluation of models trained on synthetic datasets (FEVER, VitaminC) against real-world claims in WICE
	- **Who**: Multiple NLI models evaluated across WICE dataset containing naturally-occurring Wikipedia claims vs. synthetic negative examples from other datasets
- Including evidence context in sentence-level processing improved retrieval performance significantly compared to models without contextual information #evd-candidate ^evd-008
	- **What**: Retrieval accuracy and downstream entailment classification performance metrics
	- **How**: Ablation study comparing sentence-level models with 128-token evidence context vs. models processing evidence sentences in isolation
	- **Who**: T5 models evaluated on WICE evidence retrieval task using both sentence-level and chunk-level processing approaches

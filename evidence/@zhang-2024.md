# Reinforcement Retrieval Leveraging Fine-grained Feedback for Fact Checking News Claims with Black-Box LLM

**Authors:** Xuan Zhang, Wei Gao
**Year:** 2024
**DOI:** 10.48550/arXiv.2404.17283
**Citation Count:** 15

## Evidence Items

- FFRR (Fine-grained Feedback with Reinforcement Retrieval) achieved significant improvements over both LLM-enabled and non-LLM baselines in news claim verification with statistical significance (p < 0.01) #evd-candidate ^evd-001
	- **What**: Macro-average precision, recall, and F1 scores across different model variants, with statistical significance testing
	- **How**: Comparative evaluation using 8/1/1 train/validation/test split with macro-average metrics and statistical significance testing
	- **Who**: FFRR variants tested against baselines on RAWFC (Snopes-based, 3-class) and LIAR-RAW (PolitiFact-based, 6-class) datasets
- Simple zero-shot prompting with LLMs showed competitive performance, with Direct Prompting lagging behind end-to-end optimized SOTA by only 7.0% in F1 score #evd-candidate ^evd-002
	- **What**: F1 score gap of 7.0% between zero-shot LLM prompting and specialized non-LLM fact-checking models
	- **How**: Direct comparison of zero-shot prompting approach against end-to-end optimized baseline using macro-average F1 scores
	- **Who**: GPT-3.5 API text-davinci-003 evaluated on news claim verification datasets
- Tunable retrieval models with FFRR consistently outperformed frozen retrieval models, with improvements of 1.7%, 5.3%, and 12.5% in F1 score for document-level, question-level, and hybrid variants respectively #evd-candidate ^evd-003
	- **What**: F1 score improvements: 1.7% (document-level), 5.3% (question-level), and 12.5% (hybrid) when comparing tunable vs frozen retrieval
	- **How**: Ablation study comparing FFRR variants with tunable parameters against frozen baseline versions using the same evaluation metrics
	- **Who**: FFRR variants tested on RoBERTa-based dense retrieval models across both RAWFC and LIAR-RAW datasets
- Document mismatch was identified as the most prevalent failure mode, comprising 48% of error cases in the retrieval process #evd-candidate ^evd-004
	- **What**: Error categorization showing 48% of failures attributed to document mismatch issues
	- **How**: Manual error analysis of retrieval failures categorized by type of retrieval problem
	- **Who**: Error analysis conducted on FFRR model failures across the news claim verification datasets
- Retrieval-augmented LLM approaches consistently improved performance over direct prompting methods across different numbers of retrieved documents (K=1 to K=5) #evd-candidate ^evd-005
	- **What**: Performance improvements measured across different values of K (number of retrieved documents) from 1 to 5
	- **How**: Systematic evaluation varying the number of retrieved documents while measuring macro-average precision, recall, and F1
	- **Who**: FFRR variants (document-level, question-level, and hybrid) tested on both RAWFC and LIAR-RAW test sets
- FFRR outperformed REPLUG because REPLUG was unable to flexibly explore and exploit all retrieved documents, being limited to only top-K results #evd-candidate ^evd-006
	- **What**: Comparative performance metrics showing FFRR superiority over REPLUG in document utilization flexibility
	- **How**: Head-to-head comparison of retrieval strategies, with analysis of how each method utilizes retrieved documents
	- **Who**: FFRR and REPLUG systems compared on the same news claim verification benchmarks
- Ground truth leak detection and removal affected 4.7% of documents in RAWFC and 2.4% of documents in LIAR-RAW, indicating data contamination issues in fact-checking datasets #evd-candidate ^evd-007
	- **What**: Percentage of documents removed due to ground truth leaks: 4.7% (RAWFC) and 2.4% (LIAR-RAW)
	- **How**: Application of Glockner et al. (2022) detection method to identify and remove documents containing leaked ground truth information
	- **Who**: RAWFC and LIAR-RAW datasets used for news claim verification experiments
- LLM limitations in understanding specific contexts and language nuances directly impacted the accuracy of retrieval models and verification results #evd-candidate ^evd-008
	- **What**: Qualitative assessment of how LLM contextual understanding gaps affect downstream verification accuracy
	- **How**: Analysis of model performance limitations attributed to inherent LLM capabilities and biases from training data
	- **Who**: GPT-3.5 API text-davinci-003 used as the black-box LLM in the FFRR framework

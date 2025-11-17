# Evaluating open-source Large Language Models for automated fact-checking

**Authors:** Nicoló Fontana, Francesco Corso, Enrico Zuccolotto, Francesco Pierri
**Year:** 2025
**DOI:** 10.48550/arXiv.2503.05565
**Citation Count:** 3

## Evidence Items

- Llama3-70B achieved F1 scores of approximately 0.9 for claim-article semantic relationship identification, outperforming all other tested models including fine-tuned RoBERTa #evd-candidate ^evd-001
	- **What**: F1 scores measuring binary classification performance on identifying semantic relationships between claims and fact-checking articles
	- **How**: Comparative evaluation across 24 different prompt configurations using precision, recall, F1 score, and ROC AUC metrics with 0.95 confidence intervals
	- **Who**: Four LLMs (Mistral-7B, Mixtral-8x7B, Llama3-8B, Llama3-70B) and fine-tuned RoBERTa tested on 60,000 English claims from Fact-Check Insights dataset
- LLMs significantly underperformed fine-tuned RoBERTa (0.95 F1) in verifying true news claims, with Llama3-70B achieving only approximately 0.9 F1 score in the best case #evd-candidate ^evd-002
	- **What**: F1 scores for positive class (true claims) classification performance showing performance gaps between model types
	- **How**: Binary classification evaluation with disaggregated metrics by class (true vs false claims) using claim-article pairs
	- **Who**: Same four LLMs compared against fine-tuned RoBERTa baseline on dataset with 90% false claims and 10% true claims
- Mixtral-8x7B was the weakest performing LLM with average F1 scores of 0.65 and performance occasionally dropping below random threshold of 0.5 #evd-candidate ^evd-003
	- **What**: F1 scores and frequency of below-chance performance indicating systematic failure cases
	- **How**: Averaged performance across multiple prompt configurations with confidence intervals and threshold comparison analysis
	- **Who**: Mixtral-8x7B-Instruct-v0.1 model evaluated on the 60,000 claim fact-checking dataset
- External knowledge integration from Google and Wikipedia sources did not significantly enhance LLM performance in claim verification tasks #evd-candidate ^evd-004
	- **What**: Comparative F1 scores between models with and without external knowledge augmentation showing no significant improvement
	- **How**: Controlled comparison testing LLMs in three conditions: no context, Wikipedia context, and Google search context using neutral prompts
	- **Who**: All four LLMs tested on complete 60,000 claim dataset with external knowledge from Google search results and Wikipedia articles
- LLMs showed approximately linear relationship between positive and negative class F1 scores, indicating balanced performance maintenance across claim types #evd-candidate ^evd-005
	- **What**: Correlation analysis of F1 scores between true and false claim classification performance
	- **How**: Statistical analysis plotting F1 scores for positive vs negative classes to assess performance balance
	- **Who**: Three main LLMs (excluding fine-tuned RoBERTa) evaluated on claim-article semantic relationship task
- Llama3-70B generated the fewest faulty responses (failures to provide scores or adhere to expected output format) compared to smaller models #evd-candidate ^evd-006
	- **What**: Frequency counts of model failures including inability to provide classification scores or follow output formatting requirements
	- **How**: Error rate analysis tracking instances where models failed to produce valid responses across different prompting strategies
	- **Who**: All four LLMs tested across the three experimental tasks with particular focus on output format compliance
- Models performed significantly better when provided with structured summaries of search results rather than full web pages or isolated snippets #evd-candidate ^evd-007
	- **What**: Comparative performance metrics across different external content presentation formats
	- **How**: Controlled experiment varying the format of external knowledge (snippets vs summaries vs full articles) while keeping content source constant
	- **Who**: LLMs tested on fact-checking task with external knowledge from Google and Wikipedia in different presentation formats
- Class imbalance significantly impacted evaluation with 90% false claims creating pronounced performance gaps between positive and negative classes across all models including fine-tuned RoBERTa #evd-candidate ^evd-008
	- **What**: Disaggregated precision, recall, and F1 scores showing differential performance on minority (true) vs majority (false) classes
	- **How**: Class-stratified evaluation metrics analysis accounting for severe imbalance in ground truth labels
	- **Who**: All tested models evaluated on Fact-Check Insights dataset with 54,000 false claims and 6,000 true claims

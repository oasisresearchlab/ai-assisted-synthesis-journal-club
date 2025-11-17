# Step-by-Step Fact Verification System for Medical Claims with Explainable Reasoning

**Authors:** Juraj Vladika, Ivana Hacajov'a, Florian Matthes
**Year:** 2025
**DOI:** 10.48550/arXiv.2502.14765
**Citation Count:** 6

## Evidence Items

- Step-by-step LLM verification systems significantly outperformed traditional three-part pipeline approaches across all medical datasets, with F1 score improvements of +4.3 on HealthFC, +3.4 on CoVERT, and +4.9 on SciFact. #evd-candidate ^evd-001
	- **What**: Binary classification F1 scores, precision, and recall metrics for SUPPORTED vs REFUTED claim verification
	- **How**: Comparative evaluation between multi-step LLM systems using question generation and evidence synthesis versus traditional document retrieval + evidence extraction + DeBERTa classification pipeline
	- **Who**: Three medical fact-checking datasets: SCIFACT (693 claims), HEALTHFC (327 claims), and COVERT (264 claims) with real-world biomedical and health claims
- GPT-4o-mini consistently achieved the highest performance among tested LLMs for medical claim verification across all datasets and experimental conditions. #evd-candidate ^evd-002
	- **What**: Comparative F1 scores, precision, and recall metrics across different language models
	- **How**: Direct performance comparison using identical prompting strategies, temperature settings (0), and maximum token limits (512) across models via API calls
	- **Who**: Three LLMs tested: GPT-4o-mini, Mixtral 8x7B, and LLaMa 3.1 (70B) on medical claim datasets
- External web search using DuckDuckGo improved performance specifically for SciFact biomedical claims but showed mixed results for common health claims where internal LLM knowledge sometimes outperformed web search. #evd-candidate ^evd-003
	- **What**: F1 score differences between internal knowledge-only versus web search-augmented verification approaches
	- **How**: Ablation study comparing same LLM system with and without DuckDuckGo web search integration for evidence gathering
	- **Who**: SCIFACT dataset (expert-written biomedical claims from medical papers) versus HEALTHFC and COVERT (common health claims)
- Incorporating first-order logic predicates into the reasoning process achieved the best overall performance for HealthFC with 81.7 F1 score, representing a +5.2 improvement over baseline and +1.0 over non-predicate approaches. #evd-candidate ^evd-004
	- **What**: Binary classification F1 scores comparing structured logic-based reasoning versus standard natural language reasoning
	- **How**: Experimental comparison of GPT-4o-mini system with and without first-order logic predicate integration for claim verification reasoning
	- **Who**: HEALTHFC dataset (327 health-related claims) tested with structured versus unstructured reasoning approaches
- The step-by-step approach showed particularly strong improvements in precision values compared to recall across all three medical datasets. #evd-candidate ^evd-005
	- **What**: Precision and recall metrics showing asymmetric performance gains favoring precision over recall
	- **How**: Detailed breakdown analysis of binary classification performance metrics comparing traditional pipeline versus multi-step LLM approaches
	- **Who**: All three medical datasets (SCIFACT, HEALTHFC, COVERT) with varying claim types from formal biomedical to informal social media health claims
- Traditional three-part pipeline using DeBERTa achieved baseline performance levels that were consistently exceeded by all LLM-based approaches across different knowledge sources (PubMed, Wikipedia, online search). #evd-candidate ^evd-006
	- **What**: Baseline F1, precision, and recall scores from encoder-only transformer model fine-tuned on NLI datasets
	- **How**: Standard three-stage pipeline evaluation: document retrieval, evidence extraction, then DeBERTa-v3 classification for veracity prediction
	- **Who**: Same three medical datasets used as benchmark comparison, with DeBERTa-v3 model fine-tuned on various Natural Language Inference datasets
- Real-world Twitter-sourced health claims (COVERT dataset) with informal language presented additional verification challenges compared to expert-written biomedical claims, but still showed significant improvement with step-by-step approaches. #evd-candidate ^evd-007
	- **What**: Performance differences between formal expert-written claims versus informal social media claims, measured by F1 scores
	- **How**: Cross-dataset performance comparison analyzing how language formality and claim source affected verification accuracy
	- **Who**: COVERT dataset (264 causative health claims from Twitter) versus SCIFACT dataset (693 expert-written biomedical claims from paper abstracts)
- The multi-step question generation and evidence synthesis approach produced measurable improvements despite acknowledged limitations in question quality and reasoning chain accuracy. #evd-candidate ^evd-008
	- **What**: Overall system performance gains measured against qualitative analysis of generated follow-up questions and evidence snippets
	- **How**: Combined quantitative performance evaluation with qualitative analysis of intermediate outputs including generated questions and evidence quality
	- **Who**: All tested medical claim datasets with particular focus on question generation patterns for medical terms, diseases, symptoms, and drug definitions

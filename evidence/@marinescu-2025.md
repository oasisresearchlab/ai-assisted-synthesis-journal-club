# FactReasoner: A Probabilistic Approach to Long-Form Factuality Assessment for Large Language Models

**Authors:** Radu Marinescu, D. Bhattacharjya, Junkyu Lee, Tigran Tchrakian, Javier Carnerero-Cano, Yufang Hou, Elizabeth Daly, Alessandra Pascale
**Year:** 2025
**DOI:** 10.48550/arXiv.2502.18573
**Citation Count:** 0

## Evidence Items

- FactReasoner significantly outperformed state-of-the-art prompt-based approaches on labeled datasets with near-zero p-values for F1 and MAE metrics #evd-candidate ^evd-001
	- **What**: F1 scores, Mean Absolute Error (MAE), statistical significance testing with p-values approaching zero
	- **How**: Comparative evaluation using standard statistical testing between FactReasoner's probabilistic graphical model approach versus traditional prompt-based factuality assessment methods
	- **Who**: Biographies dataset (157 ChatGPT-generated biographies) tested with granite-3.0-8b-instruct, llama-3.1-70b-instruct, and mixtral-8x22b-instruct models
- FactReasoner achieved well-calibrated predictions with a mean Brier score of 0.18 (±0.10) indicating good probability calibration #evd-candidate ^evd-002
	- **What**: Brier scores measuring calibration quality of probabilistic predictions, with perfect calibration corresponding to score of 0
	- **How**: Calibration analysis comparing predicted posterior marginal probabilities against actual factuality outcomes using standard Brier score calculation
	- **Who**: llama-3.1-70b-instruct model tested across multiple benchmark datasets for long-form factuality assessment
- FactReasoner performed comparably to DeepSeek-v3 (a very powerful open model) on unlabeled datasets despite showing superior performance on labeled data #evd-candidate ^evd-003
	- **What**: Factual precision and F1@K scores comparing FactReasoner against DeepSeek-v3 performance
	- **How**: Comparative evaluation using the same evaluation metrics and procedures across labeled versus unlabeled dataset conditions
	- **Who**: AskHistorians, ELI5, FreshBooks, and LongFact-Objects unlabeled datasets tested with DeepSeek-v3 and FactReasoner models
- The Weighted Mini-Buckets inference algorithm solved all probabilistic reasoning instances in under 0.05 seconds with i-bound parameter of 6 #evd-candidate ^evd-004
	- **What**: Computational performance metrics measuring inference time and accuracy for probabilistic graphical model reasoning
	- **How**: Empirical timing analysis of the WMB algorithm across all inference problems in the benchmark datasets with controlled i-bound parameter setting
	- **Who**: All benchmark datasets (Biographies, AskHistorians, ELI5, FreshBooks, LongFact-Objects) processed through the FactReasoner pipeline
- FactReasoner showed improved factual precision and recall compared to prompt-based approaches across both labeled and unlabeled benchmark datasets #evd-candidate ^evd-005
	- **What**: Factual precision scores and recall measurements comparing different factuality assessment approaches
	- **How**: Systematic evaluation using consistent decomposition into atomic units, evidence retrieval from Wikipedia and Google Search, and standardized scoring metrics
	- **Who**: Five benchmark datasets (Biographies, AskHistorians, ELI5, FreshBooks, LongFact-Objects) evaluated with open-source LLMs from IBM Granite, Meta Llama, and MistralAI families
- The computational overhead scales differently across FactReasoner versions: FR3 requires O(n•m + m²) prompts, FR2 requires O(n•m) prompts, while prompt-based assessors only require O(n) prompts #evd-candidate ^evd-006
	- **What**: Computational complexity measurements in terms of number of prompts required for different algorithmic approaches
	- **How**: Algorithmic analysis counting prompt requirements where n=number of atomic units, m=total non-duplicated contexts, k=maximum contexts per atom
	- **Who**: Comparison across FactReasoner variants (FR1, FR2, FR3) versus traditional prompt-based factuality assessors
- LLM-based relation models successfully extracted atom-context and context-context relationships required for constructing the probabilistic graphical model #evd-candidate ^evd-007
	- **What**: Relationship extraction accuracy and graphical model construction success rates for entailment/contradiction detection
	- **How**: Empirical evaluation of the relation model's ability to identify logical relationships using white-box uncertainty quantification from 'entailment' or 'contradiction' token logits
	- **Who**: Same LLMs used throughout pipeline (granite-3.0-8b-instruct, llama-3.1-70b-instruct, mixtral-8x22b-instruct) tested on atomic units from all benchmark datasets
- The system maintained consistent performance when decomposing responses into atomic units using llama-3.3-70b-instruct across all datasets #evd-candidate ^evd-008
	- **What**: Consistency metrics for atomic unit decomposition and revision quality across different dataset types and domains
	- **How**: Standardized decomposition and revision process using the same model (llama-3.3-70b-instruct) with cached contextual information from Wikipedia and Google Search
	- **Who**: All generated responses from Biographies, AskHistorians, ELI5, FreshBooks, and LongFact-Objects datasets processed through identical pipeline stages

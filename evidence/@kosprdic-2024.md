# Scientific Claim Verification with Fine-Tuned NLI Models

**Authors:** Milos Kosprdic, Adela Ljajic, Darija Medvecki, Bojana Bašaragin, Nikola Milosevic
**Year:** 2024
**DOI:** 10.5220/0012900000003838
**Citation Count:** 0

## Evidence Items

- DeBERTa achieved the highest F1 score of 88% on scientific claim verification, outperforming seven other transformer models including RoBERTa Large and XLM RoBERTa Large. #evd-candidate ^evd-001
	- **What**: F1 scores across eight different fine-tuned transformer models, with DeBERTa achieving 88% and DeBERTa SQuAD achieving 87%
	- **How**: Three-class classification task (support/contradict/no evidence) using fine-tuned models on concatenated claim-evidence pairs, evaluated with precision, recall, F1-score and accuracy metrics
	- **Who**: Eight transformer models (RoBERTa Large, XLM RoBERTa Large, DeBERTa, DeBERTa SQuAD variants) trained and tested on SciFact dataset containing biomedical claim-evidence pairs
- Fine-tuned DeBERTa model demonstrated superior performance with a 7% absolute increase in F1 score compared to the best-performing GPT-4 model in zero-shot evaluation. #evd-candidate ^evd-002
	- **What**: Comparative F1 scores between fine-tuned DeBERTa and GPT-4 models (GPT-4, GPT-4 Turbo, GPT-4o), showing 7% absolute improvement for DeBERTa
	- **How**: Zero-shot evaluation of GPT-4 models using structured prompts versus fine-tuned evaluation of DeBERTa, both tested on the same 122-example test set
	- **Who**: DeBERTa fine-tuned model versus GPT-4, GPT-4 Turbo, and GPT-4o models evaluated on 10% subset of transformed SciFact dataset (122 examples across three classes)
- On out-of-domain evaluation using HealthVer dataset, the best DeBERTa model achieved F1 score of 48%, outperforming previous state-of-the-art models by more than 12% and showing 8% absolute improvement over prior BERT-base results. #evd-candidate ^evd-003
	- **What**: F1 scores on external validation dataset: DeBERTa achieved 48% F1, compared to previous BERT-base model's 36% F1 and 39% accuracy
	- **How**: External validation testing on HealthVer dataset (different from training data) to assess generalization, with further 4% improvement achieved when retraining on 90% of SciFact data
	- **Who**: DeBERTa model trained on SciFact dataset and evaluated on HealthVer dataset, compared against previous BERT-base model results from Sarrouti et al. (2021)
- The CONTRADICT class posed the most significant classification challenge, representing only 22% of the dataset and resulting in frequent misclassifications to other classes. #evd-candidate ^evd-004
	- **What**: Class distribution analysis showing CONTRADICT class comprises 22% of dataset, with higher misclassification rates for this underrepresented class
	- **How**: Error analysis examining misclassification patterns across the three classes (support/contradict/no evidence), identifying class imbalance effects on model performance
	- **Who**: All fine-tuned models evaluated on SciFact dataset, with detailed error analysis conducted on misclassified claims in the in-domain evaluation subset
- Numerical data, abbreviations, and complex scientific concepts were identified as primary sources of misclassification, particularly causing SUPPORT claims to be misclassified as NO EVIDENCE. #evd-candidate ^evd-005
	- **What**: Qualitative analysis of misclassification patterns, identifying specific linguistic and content features that led to errors (numerical data, abbreviations, biological processes, chemical reactions)
	- **How**: Manual error analysis examining misclassified claims to identify common failure modes and patterns in model predictions across different scientific content types
	- **Who**: Misclassified examples from the transformed SciFact dataset test subset, analyzed across all model predictions with focus on biomedical domain complexity
- Models demonstrated particular difficulty with nuanced contradictions and temporal alignment issues, struggling to distinguish surface-level similarities from underlying semantic relationships. #evd-candidate ^evd-006
	- **What**: Specific error types including failure to recognize temporal misalignments and inability to detect subtle contradictions masked by shared keywords and phrases
	- **How**: Detailed analysis of CONTRADICT to SUPPORT misclassifications and CONTRADICT to NO EVIDENCE errors, examining semantic versus surface-level feature processing
	- **Who**: Fine-tuned models evaluated on SciFact dataset examples containing complex scientific claims with temporal elements and nuanced contradictory relationships
- The claim verification task achieved effective performance as a three-class natural language inference problem, with successful application of transformer-based sequence classification approach. #evd-candidate ^evd-007
	- **What**: Successful reformulation of claim verification as NLI task with three output classes, demonstrating viability of concatenated claim-evidence input format for entailment assessment
	- **How**: Conceptual framework treating claim verification as multi-class classification using concatenation of claims with PubMed abstracts as evidence, implemented through transformer sequence classification
	- **Who**: All eight transformer models applied to SciFact dataset pairs of claims and evidence from biomedical domain literature

# Clemson NLP at SemEval-2023 Task 7: Applying GatorTron to Multi-Evidence Clinical NLI

**Authors:** Ahamed Alameldin, Ashton Williamson
**Year:** 2023
**DOI:** 10.18653/v1/2023.semeval-1.220
**Citation Count:** 2

## Evidence Items

- GatorTron-based ensemble system achieved F1-scores of 0.705 for entailment determination and 0.806 for evidence retrieval on clinical trial data #evd-candidate ^evd-001
	- **What**: F1-scores measuring precision and recall balance for binary classification tasks
	- **How**: Fine-tuned GatorTron-BERT models evaluated on held-out test set using ensemble approach combining evidence retrieval and entailment classification
	- **Who**: 1,000 English-language breast cancer clinical trial reports with 500 test statements annotated by clinical domain experts
- Evidence extraction approach improved entailment performance by 0.059 F1-score points compared to using full clinical trial reports #evd-candidate ^evd-002
	- **What**: Absolute F1-score improvement of 0.059 when using extracted relevant sections versus complete documents
	- **How**: Comparative evaluation between models using full CTR premises versus models using only extracted relevant sections identified by evidence retrieval system
	- **Who**: Same clinical trial dataset with statement-premise pairs for textual entailment task
- Domain adaptation provided minimal but consistent performance gains of 0.009 F1-score for entailment and 0.019 for evidence retrieval #evd-candidate ^evd-003
	- **What**: Small absolute F1-score improvements (0.009 and 0.019) from continued pre-training on target domain data
	- **How**: Comparison between base fine-tuned models and models with additional domain adaptation training on clinical trial data
	- **Who**: GatorTron-BERT models tested on breast cancer clinical trial reports dataset
- Model achieved 0.584 F1-score when given only statements without premises, indicating presence of annotation artifacts #evd-candidate ^evd-004
	- **What**: F1-score of 0.584 for classification using statements alone, substantially above 0.502 baseline
	- **How**: Ablation study testing model performance with statement-only input versus term frequency-inverse document frequency baseline
	- **Who**: Clinical trial entailment dataset with statements designed to require premise information for correct classification
- System struggled with numerical reasoning tasks, identified as a key limitation through validation set analysis #evd-candidate ^evd-005
	- **What**: Qualitative error analysis revealing systematic failures on numerical reasoning components
	- **How**: Manual inspection of validation set predictions to identify error patterns and failure modes
	- **Who**: Breast cancer clinical trial dataset containing numerical information requiring quantitative reasoning
- Increased model size alone was insufficient for strong performance, requiring domain adaptation and architectural strategies #evd-candidate ^evd-006
	- **What**: Performance comparisons showing model size increases did not proportionally improve task performance
	- **How**: Analysis of different model configurations and sizes with and without domain-specific adaptations
	- **Who**: GatorTron models of varying sizes tested on clinical trial natural language inference tasks
- System ranked 7th out of participating teams for entailment task and 6th for evidence retrieval in competitive evaluation #evd-candidate ^evd-007
	- **What**: Relative performance rankings among multiple competing systems in shared task evaluation
	- **How**: Official SemEval-2023 Task 7 competition evaluation with standardized test set and evaluation metrics
	- **Who**: Multiple research teams' systems evaluated on same clinical trial dataset with expert annotations

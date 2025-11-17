# DeFactoNLP: Fact Verification using Entity Recognition, TFIDF Vector Comparison and Decomposable Attention

**Authors:** Aniketh Janardhan Reddy, Gil Rocha, Diego Esteves
**Year:** 2018
**DOI:** 10.18653/v1/W18-5522
**Citation Count:** 12

## Evidence Items

- The DeFactoNLP system achieved moderate performance on fact verification with 51.36% label accuracy and 38.33% FEVER score on a large-scale dataset #evd-candidate ^evd-001
	- **What**: Label accuracy of 0.5136, FEVER score of 0.3833, evidence F1-score of 0.4277
	- **How**: Evaluated on blind test set using standard FEVER shared task metrics including evidence precision/recall and final classification accuracy
	- **Who**: DeFactoNLP system tested on FEVER 2018 dataset with 19,998 claims from Wikipedia
- The AI system ranked in the middle tier (5th-12th place) among 24 participating systems across different evaluation metrics #evd-candidate ^evd-002
	- **What**: Comparative rankings: 5th in evidence F1 score, 11th in label accuracy, 12th in FEVER score out of 24 systems
	- **How**: Head-to-head comparison with other AI systems in shared task competition using standardized evaluation protocol
	- **Who**: 24 participating AI systems in FEVER 2018 shared task evaluated on same test set
- Fine-tuning a pre-trained RTE model on domain-specific data significantly improved generalization for claim verification tasks #evd-candidate ^evd-003
	- **What**: Improved performance after fine-tuning (specific metrics referenced in Table 2 but not provided in extract)
	- **How**: Created FEVER SNLI-style dataset and fine-tuned decomposable attention model originally trained on SNLI corpus
	- **Who**: Decomposable attention model tested on FEVER dataset before and after domain-specific fine-tuning
- The system showed better evidence retrieval capabilities than baseline but poor final classification reliability #evd-candidate ^evd-004
	- **What**: Evidence F1 score significantly better than baseline, but label accuracy only marginally better than baseline
	- **How**: Direct comparison with baseline system performance across evidence retrieval and final classification metrics
	- **Who**: DeFactoNLP system compared against FEVER shared task baseline system
- Evidence retrieval showed high precision but low recall (precision: 51.91%, recall: 36.36%) #evd-candidate ^evd-005
	- **What**: Evidence precision of 0.5191 and evidence recall of 0.3636, resulting in F1-score of 0.4277
	- **How**: Measured ability to correctly identify and retrieve supporting/refuting evidence sentences from Wikipedia
	- **Who**: DeFactoNLP system evaluated on FEVER test set with ground truth evidence annotations
- AI system failed on multi-sentence claims due to architectural limitations of pairwise entailment models #evd-candidate ^evd-006
	- **What**: Inability to handle claims requiring multiple sentences for verification, contributing to low recall and accuracy
	- **How**: Qualitative analysis of system failures revealed RTE module limitation to sentence-pair entailment detection
	- **Who**: DeFactoNLP system analyzed on FEVER dataset containing complex multi-sentence verification claims
- Named entity disambiguation errors led to systematic misclassification of claims #evd-candidate ^evd-007
	- **What**: Incorrect labeling due to confusion between entities with similar names (e.g., movie 'Soul Food' vs soundtrack 'Soul Food')
	- **How**: Post-hoc error analysis identifying cases where system retrieved evidence from wrong Wikipedia pages
	- **Who**: DeFactoNLP system errors analyzed on FEVER claims containing named entities with potential ambiguity
- Coreference resolution limitations caused the AI system to miss relevant evidence in Wikipedia articles #evd-candidate ^evd-008
	- **What**: Missed evidence detection due to inability to resolve pronouns and references within articles
	- **How**: Error analysis identified cases where RTE module failed to assess sentences containing coreference
	- **Who**: DeFactoNLP system analyzed on Wikipedia articles from FEVER dataset containing coreference structures

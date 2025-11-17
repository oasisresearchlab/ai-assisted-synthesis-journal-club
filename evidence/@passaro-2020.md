# UNIPI-NLE at CheckThat! 2020: Approaching Fact Checking from a Sentence Similarity Perspective Through the Lens of Transformers

**Authors:** Lucia C. Passaro, Alessandro Bondielli, Alessandro Lenci, F. Marcelloni
**Year:** 2020
**DOI:** -
**Citation Count:** 17

## Evidence Items

- A fine-tuned Sentence-BERT model achieved 0.91 MAP@5 performance on verified claim retrieval task #evd-candidate ^evd-001
	- **What**: MAP@5 (Mean Average Precision at 5) score of 0.91 on binary classification of claim-evidence pairs
	- **How**: Two-step cascade fine-tuning applied to pre-trained Sentence-BERT model with probability-based ranking for pair classification
	- **Who**: Sentence-BERT transformer model tested on CheckThat! 2020 fact-checking dataset
- Hybrid approach combining Information Extraction and Deep Learning outperformed single-method approaches for claim verification #evd-candidate ^evd-002
	- **What**: System performance using combined IE module for entity/keyphrase matching plus deep learning for text similarity refinement
	- **How**: Two-stage pipeline: first filtering pairs by shared entities/keyphrases, then applying fine-tuned transformer for similarity classification
	- **Who**: Tweet-claim pairs from fact-checking dataset, processed through hybrid UNIPI-NLE system
- AI system effectiveness depends on claims and evidence sharing entities/keyphrases and having similar semantic meaning #evd-candidate ^evd-003
	- **What**: System performance correlation with presence of shared named entities, keywords, and semantic similarity between tweet-claim pairs
	- **How**: Information Extraction module used to identify shared entities/keyphrases as filtering criterion before deep learning classification
	- **Who**: Tweet-claim pairs where claims are expected to mention same entities and have similar meaning to verification tweets
- Fine-tuned transformer models can effectively perform claim verification through sentence similarity estimation #evd-candidate ^evd-004
	- **What**: Binary classification accuracy for determining correct matches between claims and evidence tweets
	- **How**: Sentence-BERT model fine-tuned specifically for text similarity computation and classification of claim-evidence pairs
	- **Who**: Pre-trained Sentence-BERT model adapted for fact-checking domain through cascade fine-tuning process

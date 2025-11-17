# Multi-hop Evidence Pursuit Meets the Web: Team Papelo at FEVER 2024

**Authors:** Christopher Malon
**Year:** 2024
**DOI:** 10.18653/v1/2024.fever-1.2
**Citation Count:** 4

## Evidence Items

- Multi-hop evidence pursuit strategy achieved 0.045 higher label accuracy and 0.155 higher AVeriTeC score compared to generating all questions at once #evd-candidate ^evd-001
	- **What**: Label accuracy differences and AVeriTeC scores (METEOR-based evidence adequacy metric)
	- **How**: Comparative evaluation between iterative multi-hop questioning versus simultaneous question generation approaches
	- **Who**: FEVER 2024 (AVeriTeC) dataset with 3,068 training claims, tested on GPT-4o and T5-large hybrid system
- Hybrid Seq+LLM approach (T5 for first questions, GPT-4o for follow-ups) outperformed both LLM+LLM and Seq+Seq variants in claim verification #evd-candidate ^evd-002
	- **What**: Performance degradation measurements when using single model types versus hybrid approach
	- **How**: Ablation study comparing different combinations of sequence-to-sequence models and LLMs for question generation components
	- **Who**: Same FEVER 2024 dataset, comparing T5-large fine-tuned model against GPT-4o across different system configurations
- System achieved 0.510 AVeriTeC score on development set and 0.477 on test set for 4-class claim verification #evd-candidate ^evd-003
	- **What**: AVeriTeC scores measuring both classification accuracy and evidence quality on standard benchmark
	- **How**: End-to-end evaluation using METEOR scores between gold and predicted question-answer evidence pairs
	- **Who**: FEVER 2024 shared task dataset with real-world web disinformation claims
- Removing paraphrasing had minimal effect on label accuracy but reduced AVeriTeC score to less than half of the full system #evd-candidate ^evd-004
	- **What**: Label accuracy maintenance but dramatic evidence quality score reduction (>50% drop in AVeriTeC)
	- **How**: Ablation study removing paraphrasing component while maintaining other system features
	- **Who**: FEVER 2024 evaluation set using GPT-4o/T5 hybrid system
- Including metadata about evidence sources improved both label accuracy and AVeriTeC scores compared to no-metadata variant #evd-candidate ^evd-005
	- **What**: Performance improvements in classification accuracy and evidence adequacy when source information is provided
	- **How**: Controlled comparison between system variants with and without document source metadata in LLM prompts
	- **Who**: FEVER 2024 dataset claims processed through web search with GPT-4o for final verdict generation
- Multi-document processing (using all 10 search hits) achieved very similar label accuracy to single-document focused approach #evd-candidate ^evd-006
	- **What**: Comparable classification performance between multi-document and single-document processing strategies
	- **How**: Ablation comparing LLM processing of all search results simultaneously versus selecting best single document
	- **Who**: Web search results from Google for FEVER 2024 claims, processed by GPT-4o
- System failed to accurately predict 'Not Enough Evidence' and 'Conflicting Evidence/Cherrypicking' classes, with LLMs tending to over-select 'Not Enough Evidence' #evd-candidate ^evd-007
	- **What**: Poor classification performance on two of four target classes, with systematic bias toward 'Not Enough Evidence' predictions
	- **How**: Analysis of confusion matrices and class-specific accuracy across 4-class classification task
	- **Who**: FEVER 2024 real-world disinformation claims requiring nuanced evidence assessment
- 297 out of 500 development set claims had gold documents with empty extracted text, indicating significant data quality issues #evd-candidate ^evd-008
	- **What**: 59.4% of development claims lacked proper text extraction from reference documents
	- **How**: Analysis of gold standard document text extraction success rates in the provided dataset
	- **Who**: FEVER 2024 development set of 500 claims with associated gold standard evidence documents

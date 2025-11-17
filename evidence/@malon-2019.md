# Team Papelo: Transformer Networks at FEVER

**Authors:** Christopher Malon
**Year:** 2019
**DOI:** 10.18653/v1/W18-5517
**Citation Count:** 43

## Evidence Items

- Transformer networks substantially outperformed baseline entailment models, achieving 61.08% label accuracy compared to 50.5% for Decomposable Attention and 58.6% for Enhanced ESIM #evd-candidate ^evd-001
	- **What**: Label accuracy scores: Transformer (61.08%), Extended ESIM (58.6%), ESIM (56.1%), Decomposable Attention (50.5%)
	- **How**: Comparative evaluation using 3-class classification (supported/refuted/not enough information) on claim-evidence pairs from Wikipedia
	- **Who**: FEVER dataset test set with three different neural network architectures (Decomposable Attention, ESIM, Transformer with pre-trained weights)
- Transformer networks demonstrated superior robustness on imbalanced datasets, achieving performance beyond majority class baseline without requiring class reweighting techniques #evd-candidate ^evd-002
	- **What**: Performance above 93% majority class baseline on highly imbalanced dataset without artificial reweighting; Cohen's Kappa 68% higher than ESIM
	- **How**: Natural learning without class reweighting compared to ESIM which required reweighting; Cohen's Kappa statistical measure for agreement
	- **Who**: FEVER One dataset with 93% neutral statements, comparing Transformer vs ESIM models
- The complete system achieved a FEVER score of 0.5736 with evidence F1 of 0.6485, ranking fourth in FEVER score and first in evidence F1 in preliminary standings #evd-candidate ^evd-003
	- **What**: FEVER score: 0.5736, Label accuracy: 0.6108, Evidence F1: 0.6485, Evidence recall: 0.5002
	- **How**: End-to-end evaluation requiring both correct claim classification and correct evidence retrieval on official FEVER shared task test set
	- **Who**: FEVER shared task test set using transformer-based system with Wikipedia evidence sources
- Evaluating evidence statements separately rather than concatenated together improved system performance across all metrics #evd-candidate ^evd-004
	- **What**: Performance comparison between separate vs. concatenated evidence evaluation approaches
	- **How**: Ablation study comparing three approaches: five statements together, five statements separately, and entire articles separately
	- **Who**: FEVER dataset comparing different evidence aggregation strategies using the same transformer-based entailment classifier
- Named entity recognition significantly improved evidence retrieval rates from baseline to 80.8% while less than doubling processing time #evd-candidate ^evd-005
	- **What**: Evidence retrieval rate increased to 80.8% with named entity recognition vs. lower baseline rates
	- **How**: Comparison of retrieval strategies with and without named entity recognition, measuring retrieval accuracy and processing time
	- **Who**: FEVER dataset claims requiring Wikipedia evidence retrieval, focusing on named entity resolution
- Retrieving entire articles yielded better overall performance than retrieving only five statements (FEVER score 0.5736 vs 0.5539) #evd-candidate ^evd-006
	- **What**: FEVER scores: entire articles (0.5736) vs five statements (0.5539); Label accuracy: 0.6108 vs 0.5754
	- **How**: Direct comparison between two retrieval strategies using the same transformer-based entailment classification system
	- **Who**: FEVER shared task test set comparing different evidence retrieval scope strategies
- Transformer networks showed resistance to oracle label overfitting, maintaining genuine entailment reasoning rather than simple guessing strategies #evd-candidate ^evd-007
	- **What**: Maintained entailment performance without benefiting from oracle guessing that helped other models
	- **How**: Analysis of model behavior when trained on oracle labels that could enable guessing rather than true entailment understanding
	- **Who**: Transformer network compared to other models on FEVER dataset with oracle label availability
- The system demonstrated effectiveness on challenging Wikipedia domain text with longer sentences (31 vs 14 words average), abstract vocabulary, and high prevalence of named entities #evd-candidate ^evd-008
	- **What**: Successfully processed sentences averaging 31 words with abstract vocabulary and high named entity frequency
	- **How**: Domain-specific evaluation on Wikipedia text comparing sentence length and vocabulary complexity to standard entailment datasets
	- **Who**: FEVER dataset sourced from Wikipedia articles compared to typical textual entailment datasets

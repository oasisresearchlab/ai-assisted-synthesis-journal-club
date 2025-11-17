# A Fact Checking and Verification System for FEVEROUS Using a Zero-Shot Learning Approach

**Authors:** Orkun Temiz, Oz Kilic, Arif Ozan Kızıldağ, Tugba Taskaya Temizel
**Year:** 2021
**DOI:** 10.18653/v1/2021.fever-1.13
**Citation Count:** 2

## Evidence Items

- A zero-shot learning pipeline combining BERT-large-cased, XLNET, and Anserini achieved a FEVEROUS score of 0.06 and label accuracy of 0.39 on claim verification tasks #evd-candidate ^evd-001
	- **What**: FEVEROUS score of 0.06, label accuracy of 0.39, evidence F1 score of 0.06, recall of 0.10, precision of 0.05
	- **How**: Zero-shot learning approach using document retrieval (Anserini), question answering (BERT-large-cased), and natural language inference (XLNET) without additional training
	- **Who**: FEVEROUS dataset with 87,026 Wikipedia claims requiring 3-class classification (Support, Contradict, Neutral)
- The zero-shot approach significantly underperformed compared to a fine-tuned baseline system, achieving 0.06 vs 0.18 FEVEROUS score (67% lower performance) #evd-candidate ^evd-002
	- **What**: Comparative FEVEROUS scores: proposed system 0.06 vs baseline ~0.18, label accuracy: 0.39 vs 0.48
	- **How**: Head-to-head comparison between zero-shot pipeline and fine-tuned RoBERTa-based baseline system on same evaluation metrics
	- **Who**: FEVEROUS challenge dataset with Wikipedia articles as evidence sources
- The AI system demonstrated severe bias toward predicting 'NOT ENOUGH INFO', with 2858 claims labeled as such compared to expected 501 (5.7x overrepresentation) #evd-candidate ^evd-003
	- **What**: Confusion matrix showing 2858 'NOT ENOUGH INFO' predictions vs expected 501, with only 208 true positives
	- **How**: Analysis of prediction distribution across three classes using confusion matrix on development set
	- **Who**: FEVEROUS development set claims with ground truth labels
- Evidence retrieval performance was extremely poor with only 0.06 F1 score, indicating the system struggled to identify correct supporting evidence #evd-candidate ^evd-004
	- **What**: Evidence F1 score of 0.06, recall of 0.10, precision of 0.05 for evidence identification
	- **How**: Evaluation of evidence retrieval accuracy using F1, precision, and recall metrics against gold standard evidence
	- **Who**: FEVEROUS dataset requiring both claim classification and correct evidence identification
- Multiple pre-trained transformer models (BERT-large-cased, XLNET, TAPAS) were successfully integrated in a zero-shot pipeline without requiring additional training #evd-candidate ^evd-005
	- **What**: Successful deployment of BERT for question answering, XLNET for NLI, and TAPAS for table parsing in unified pipeline
	- **How**: Integration of models pre-trained on different datasets (SNLI, MultiNLI, FEVER, ANLI) using zero-shot capabilities
	- **Who**: Models trained on established NLI datasets applied to FEVEROUS Wikipedia claim verification task
- The system achieved consistent performance across dataset splits, with development set results (FEVEROUS score 0.0642, accuracy 0.3867) closely matching test results #evd-candidate ^evd-006
	- **What**: Test set: FEVEROUS score 0.06, accuracy 0.39; Development set: FEVEROUS score 0.0642, accuracy 0.3867
	- **How**: Performance evaluation on both development and test splits to assess generalization and dataset balance
	- **Who**: FEVEROUS dataset splits designed for claim verification evaluation
- High precision-recall imbalance (0.05 precision vs 0.10 recall) indicated the system generated significantly more false positives than false negatives #evd-candidate ^evd-007
	- **What**: Precision of 0.05 and recall of 0.10, indicating 2:1 ratio favoring false positives over false negatives
	- **How**: Analysis of error types through precision and recall metrics to identify systematic biases
	- **Who**: FEVEROUS dataset claims evaluated for evidence identification accuracy
- Computational complexity emerged as a practical limitation, with inference time becoming considerable due to the multi-model pipeline architecture #evd-candidate ^evd-008
	- **What**: Reported significant inference time delays affecting practical deployment
	- **How**: Qualitative assessment of computational requirements across the multi-stage pipeline (retrieval, QA, NLI)
	- **Who**: Real-world deployment considerations for the integrated AI system pipeline

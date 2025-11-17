# Fact or Fiction: Verifying Scientific Claims

**Authors:** David Wadden, Kyle Lo, Lucy Lu Wang, Shanchuan Lin, Madeleine van Zuylen, Arman Cohan, Hannaneh Hajishirzi
**Year:** 2020
**DOI:** 10.18653/v1/2020.emnlp-main.609
**Citation Count:** 538

## Evidence Items

- Oracle rationale replacement improved AI entailment performance by approximately 20 F1 points, demonstrating that rationale selection is a major bottleneck in scientific claim verification systems. #evd-candidate ^evd-001
	- **What**: 20-point improvement in Sentence Selection+Label F1 score when gold rationales were provided instead of predicted ones
	- **How**: Ablation study comparing pipeline system performance with oracle rationales versus predicted rationales using micro-F1 evaluation
	- **Who**: VERISCI system tested on SCIFACT dataset (1,409 scientific claims)
- Transfer learning from large general datasets to domain-specific data significantly improved AI entailment performance, with FEVER pretraining followed by SCIFACT fine-tuning achieving best results. #evd-candidate ^evd-002
	- **What**: Superior performance scores for models trained on FEVER then fine-tuned on SCIFACT compared to models trained only on individual datasets
	- **How**: Comparative evaluation across four training approaches: FEVER-only, UKP Snopes-only, SCIFACT-only, and FEVER+SCIFACT sequential training
	- **Who**: RoBERTa-large model evaluated on SCIFACT scientific claim verification dataset
- AI systems achieved 64% success rate (23/36 claims) on real-world COVID-19 claim verification when evaluated by medical expert, showing practical applicability but limited reliability. #evd-candidate ^evd-003
	- **What**: 23 out of 36 COVID-19 claims were deemed to have plausible evidence retrieval and classification by medical student annotator
	- **How**: Expert evaluation of claim-evidence pairs where success required non-empty evidence set with reasonable rationales and labels for at least half of retrieved abstracts
	- **Who**: VERISCI system tested on 36 expert-written COVID-19 claims against CORD-19 corpus, evaluated by medical student
- Claim-only models exhibited very poor performance while abstract-only models also performed poorly, demonstrating that effective AI entailment requires access to both claim and evidence components. #evd-candidate ^evd-004
	- **What**: Poor F1 scores for both claim-only and abstract-only model variants compared to full claim-abstract models
	- **How**: Ablation study testing model performance with restricted inputs using RoBERTa-large encoder on SCIFACT dataset
	- **Who**: RoBERTa-large models trained on SCIFACT with artificially restricted input conditions
- Domain-specific AI models showed mixed advantages, with RoBERTa-large outperforming specialized models like SCIBERT and BioMedRoBERTa on label prediction but SCIBERT showing slight edge on rationale selection. #evd-candidate ^evd-005
	- **What**: Comparative F1 scores across different pre-trained models, with RoBERTa-large achieving highest label prediction performance and SCIBERT showing best rationale selection performance
	- **How**: Head-to-head comparison of fine-tuned models (SCIBERT, BioMedRoBERTa, RoBERTa-base, RoBERTa-large) on both label prediction and rationale selection tasks
	- **Who**: Multiple BERT-family models evaluated on SCIFACT dataset for scientific claim verification
- Statistical bootstrap analysis confirmed that observed AI performance differences were robust and not due to random dataset variation, with standard deviations reported for all F1 scores. #evd-candidate ^evd-006
	- **What**: Standard deviations of F1 scores computed across 10,000 bootstrap resampled versions of test set, confirming statistical significance of performance differences
	- **How**: Bootstrap resampling methodology generating 10,000 test set variants to assess statistical robustness of reported performance metrics
	- **Who**: All model variants tested on SCIFACT dataset with bootstrap statistical validation
- Pipeline decomposition revealed that abstract retrieval, rationale selection, and label prediction components contributed roughly equally to overall AI system errors in entailment tasks. #evd-candidate ^evd-007
	- **What**: Similar error contributions from three main pipeline components: abstract retrieval, rationale selection, and label prediction modules
	- **How**: Oracle replacement analysis systematically substituting perfect components to isolate error sources in pipeline architecture
	- **Who**: VERISCI pipeline system analyzed on SCIFACT dataset with component-wise oracle substitution
- Access to in-domain training data clearly improved AI entailment performance compared to out-of-domain training, though the specific magnitude of improvement varied by model component. #evd-candidate ^evd-008
	- **What**: Performance improvements when models had access to SCIFACT domain-specific training data versus training only on general datasets like FEVER
	- **How**: Comparative evaluation of models trained on different dataset combinations measuring abstract-level and sentence-level F1 scores
	- **Who**: Multiple AI models (RoBERTa variants, SCIBERT, BioMedRoBERTa) evaluated across FEVER, UKP Snopes, and SCIFACT training configurations

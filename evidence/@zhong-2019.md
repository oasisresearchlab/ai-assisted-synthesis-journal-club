# Reasoning Over Semantic-Level Graph for Fact Checking

**Authors:** Wanjun Zhong, Jingjing Xu, Duyu Tang, Zenan Xu, Nan Duan, M. Zhou, Jiahai Wang, Jian Yin
**Year:** 2019
**DOI:** 10.18653/v1/2020.acl-main.549
**Citation Count:** 175

## Evidence Items

- The DREAM system achieved state-of-the-art performance on the FEVER dataset with 76.85% label accuracy and 70.60% FEVER score for fact-checking entailment tasks #evd-candidate ^evd-001
	- **What**: Label accuracy of 76.85% and FEVER score of 70.60% on 3-class classification (SUPPORTED, REFUTED, NOT ENOUGH INFO)
	- **How**: Evaluated using official FEVER evaluation protocol comparing claim verification predictions against ground truth labels on blind test set
	- **Who**: FEVER dataset with 185,445 verified claims and Wikipedia evidence sentences, tested on DREAM system combining XLNet with graph-based reasoning
- Graph-based reasoning modules provided substantial performance improvements over baseline transformer models, with 3.76% accuracy gain when both modules were incorporated #evd-candidate ^evd-002
	- **What**: 3.76% improvement in label accuracy when combining graph-based distance and reasoning modules with XLNet baseline
	- **How**: Ablation study comparing full DREAM system against XLNet-only baseline on development set
	- **Who**: FEVER development set using XLNet as backbone model with and without graph convolutional network and graph attention network components
- The graph-based reasoning component alone contributed 2.04% accuracy improvement, demonstrating its effectiveness for structural information processing #evd-candidate ^evd-003
	- **What**: 2.04% drop in label accuracy when graph-based reasoning module (GCN and GAN components) was removed
	- **How**: Component ablation analysis measuring performance degradation when specific modules were eliminated from full system
	- **Who**: FEVER development set comparing full DREAM system against version without graph convolutional and attention network modules
- Graph-based distance redefinition provided measurable but smaller improvements of 0.81% accuracy over standard word positioning #evd-candidate ^evd-004
	- **What**: 0.81% decrease in label accuracy when graph-based relative distance mechanism was removed
	- **How**: Ablation study isolating the contribution of semantic structure-based word distance calculation versus standard positional encoding
	- **Who**: FEVER development set testing DREAM system with and without graph-structure-informed relative distance calculations
- RoBERTa demonstrated competitive performance as an evidence selection model in the multi-stage fact-checking pipeline #evd-candidate ^evd-005
	- **What**: Evidence selection performance scores (specific metrics not provided) using RoBERTa for ranking evidence sentences
	- **How**: Comparative evaluation of RoBERTa versus XLNet for evidence selection component, with final system using RoBERTa for leaderboard submission
	- **Who**: FEVER dataset evidence selection task comparing pre-trained transformer models RoBERTa and XLNet
- The system significantly outperformed previous state-of-the-art approaches on the competitive FEVER leaderboard across both official metrics #evd-candidate ^evd-006
	- **What**: Comparative performance showing superior results on both label accuracy and FEVER score metrics versus baseline systems
	- **How**: Benchmark comparison against three top-performing FEVER shared task systems, GEAR system, and concurrent work by Liu et al. on public leaderboard
	- **Who**: FEVER blind test set comparing DREAM against established baselines including shared task winners and recent competitive systems
- Error analysis revealed specific failure modes where semantic meaning matching and misleading evidence caused incorrect entailment predictions #evd-candidate ^evd-007
	- **What**: Qualitative error categories: failure to match semantic meanings of equivalent phrases and errors from misleading information in retrieved evidence
	- **How**: Manual error analysis examining incorrect predictions to identify systematic failure patterns in claim-evidence entailment assessment
	- **Who**: FEVER dataset error cases from DREAM system predictions, focusing on misclassified instances
- The evidence selection component was identified as critically important, with irrelevant evidence leading to different and potentially incorrect verification predictions #evd-candidate ^evd-008
	- **What**: Qualitative finding that irrelevant or poorly selected evidence causes downstream errors in claim verification accuracy
	- **How**: Analysis of system pipeline showing evidence selection impact on final verification performance, with recommendation for joint training approaches
	- **Who**: FEVER dataset multi-component pipeline analysis examining document retrieval, evidence selection, and claim verification stages

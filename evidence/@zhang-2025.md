# Enhancing Health Fact-Checking with LLM-Generated Synthetic Data

**Authors:** Jingze Zhang, Jiahe Qian, Yiliang Zhou, Yifan Peng
**Year:** 2025
**DOI:** -
**Citation Count:** 0

## Evidence Items

- BERT-based fact-checking models showed improved performance when trained with LLM-generated synthetic data, achieving F1 score improvements of 0.019 on PubHealth dataset #evd-candidate ^evd-001
	- **What**: F1 score improvement of 0.019 compared to baseline models trained only on original data
	- **How**: Fine-tuned BERT-based models using combination of original training data plus synthetic data generated through LLM pipeline, evaluated against baseline models trained only on original data
	- **Who**: BERT-based fact-checking models evaluated on PubHealth dataset for health-related claim verification
- BERT-based fact-checking models demonstrated larger performance gains on SciFact dataset with F1 score improvements of 0.049 when augmented with synthetic training data #evd-candidate ^evd-002
	- **What**: F1 score improvement of 0.049 compared to models trained without synthetic data augmentation
	- **How**: Comparative evaluation between models fine-tuned with synthetic data pipeline versus models trained only on original dataset
	- **Who**: BERT-based fact-checking models tested on SciFact dataset containing scientific health claims
- LLM-driven synthetic data generation pipeline successfully created sentence-fact entailment tables that improved fact-checking model performance across multiple datasets #evd-candidate ^evd-003
	- **What**: Performance improvements demonstrated across two independent health fact-checking datasets (PubHealth and SciFact)
	- **How**: Multi-step synthetic data generation process: document summarization, atomic fact decomposition, LLM-based entailment table construction, and binary label generation
	- **Who**: Large language models used to generate synthetic training data for BERT-based fact-checking models on health-related content
- AI systems showed consistent effectiveness gains in health-related entailment tasks when synthetic data augmentation addressed limited annotated training data availability #evd-candidate ^evd-004
	- **What**: Consistent F1 score improvements across different health fact-checking datasets when using synthetic data augmentation
	- **How**: Baseline comparison experimental design testing models with and without synthetic data pipeline augmentation
	- **Who**: Health-related fact-checking models evaluated on publicly available PubHealth and SciFact datasets
- LLMs demonstrated capability to construct meaningful sentence-fact entailment relationships for binary veracity classification in health domain #evd-candidate ^evd-005
	- **What**: Binary veracity labels generated from LLM-constructed sentence-fact entailment tables
	- **How**: LLM-based pipeline decomposing health documents into atomic facts and creating entailment relationships between sentences and facts
	- **Who**: Large language models processing health-related source documents to generate synthetic text-claim pairs

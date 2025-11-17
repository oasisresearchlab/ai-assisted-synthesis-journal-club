# Evidence-backed Fact Checking using RAG and Few-Shot In-Context Learning with LLMs

**Authors:** Ronit Singhal, Pransh Patwa, Parth Patwa, Aman Chadha, Amitava Das
**Year:** 2024
**DOI:** 10.48550/arXiv.2408.12060
**Citation Count:** 22

## Evidence Items

- LLM-powered RAG systems achieved an Averitec score of 0.33, representing a 22% absolute improvement over the baseline BERT-based system for claim verification with evidence extraction. #evd-candidate ^evd-001
	- **What**: Averitec scores measuring correct veracity predictions when evidence quality meets threshold (Q+A Hungarian METEOR ≥ 0.25)
	- **How**: Comparative evaluation using RAG pipeline with few-shot in-context learning versus baseline system using fine-tuned BERT models
	- **Who**: Averitec dataset with 2,215 test instances of real-world claims, primarily politics and COVID-19 related
- Model size correlates with better performance, with Mixtral 8*22B achieving the highest Averitec score while Llama 3.1 achieved the highest accuracy among tested LLMs. #evd-candidate ^evd-002
	- **What**: Averitec scores and accuracy metrics across different model sizes and architectures
	- **How**: Cross-model comparison using identical few-shot ICL approach with 4-bit quantized versions
	- **Who**: Five LLMs tested: Phi-3-medium, InternLM2.5, Llama-3.1, Qwen2, and Mixtral 8*22B
- Class-specific performance varies significantly, with 'Refuted' claims being easiest to predict while 'Not Enough Evidence' and 'Conflicting Evidence/Cherrypicking' classes present greater challenges across all models. #evd-candidate ^evd-003
	- **What**: Class-wise F1 scores and confusion matrix data showing differential performance across four veracity categories
	- **How**: Analysis of per-class performance metrics and confusion matrices on development set
	- **Who**: Top three performing models (Mixtral, Llama 3.1, Qwen2) evaluated on imbalanced dataset with more 'Refuted' examples
- No single LLM excels across all veracity classes, with Qwen2 outperforming others in all classes except 'Refuted', while Mixtral achieved highest macro F1 score without leading any individual class. #evd-candidate ^evd-004
	- **What**: Per-class performance metrics showing model-specific strengths and weaknesses across four veracity categories
	- **How**: Comparative class-wise analysis of precision, recall, and F1 scores across multiple models
	- **Who**: Development set evaluation comparing Mixtral, Qwen2, and other top-performing models on Averitec dataset
- Significant confusion exists between 'Supported' and 'Refuted' classes, and both 'Not Enough Evidence' and 'Conflicting Evidence' classes are equally likely to be misclassified as either 'Supported' or 'Refuted'. #evd-candidate ^evd-005
	- **What**: Confusion matrix data showing specific misclassification patterns between veracity classes
	- **How**: Analysis of Mixtral 8*22B confusion matrix on development set to identify systematic classification errors
	- **Who**: Mixtral 8*22B model evaluated on Averitec development set with four-class veracity labels
- The LLM-based system outperformed the baseline across all three evaluation metrics: question generation quality, question+answer quality, and final veracity prediction accuracy. #evd-candidate ^evd-006
	- **What**: Hungarian METEOR scores for questions only, questions+answers, and Averitec scores for veracity predictions
	- **How**: Multi-metric evaluation comparing RAG+ICL approach against baseline using Bloom+fine-tuned BERT architecture
	- **Who**: Averitec test set with 2,215 instances comparing proposed system versus official baseline system
- The fact-checking task demonstrates substantial complexity with significant room for improvement, as evidenced by the best system achieving only 0.33 Averitec score despite representing state-of-the-art performance. #evd-candidate ^evd-007
	- **What**: Absolute performance ceiling of 0.33 Averitec score representing current state-of-the-art
	- **How**: Evaluation using strict metric requiring both correct veracity prediction and sufficient evidence quality
	- **Who**: Real-world claims from Averitec dataset spanning politics and COVID-19 domains with average 17-word length
- Few-shot in-context learning approach faces scalability limitations due to prompt size constraints, preventing utilization of large annotated datasets that could potentially improve performance. #evd-candidate ^evd-008
	- **What**: Architectural constraint preventing use of large training datasets due to context window limitations
	- **How**: Implementation using few-shot ICL with limited examples rather than full dataset fine-tuning
	- **Who**: All tested LLMs (Phi-3, InternLM2.5, Llama-3.1, Qwen2, Mixtral) using 4-bit quantized versions via Ollama

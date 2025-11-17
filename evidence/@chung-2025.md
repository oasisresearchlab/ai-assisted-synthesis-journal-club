# VeriFact: Verifying Facts in LLM-Generated Clinical Text with Electronic Health Records

**Authors:** Philip Chung, Akshay Swaminathan, Alex J. Goodell, Yeasul Kim, S. M. Reincke, Lichy Han, Ben Deverett, Mohammad Amin Sadeghi, Abdel-Badih Ariss, Marc Ghanem, David Seong, Andrew A. Lee, Caitlin E. Coombes, Brad Bradshaw, Mahir A. Sufian, Hyo Jung Hong, Teresa P. Nguyen, Mohammad R. Rasouli, K. Kamra, M. Burbridge, James C. McAvoy, R. Saffary, Stephen P. Ma, Dev Dash, James Xie, Ellen Y. Wang, Clifford A. Schmiesing, Nigam H. Shah, N. Aghaeepour
**Year:** 2025
**DOI:** 10.48550/arXiv.2501.16672
**Citation Count:** 9

## Evidence Items

- The VeriFact system achieved up to 92.7% agreement with human clinician ground truth on fact-checking clinical propositions, demonstrating high effectiveness at entailment verification in the medical domain. #evd-candidate ^evd-001
	- **What**: Agreement percentages between AI system and human clinician labels, reaching 92.7% for sentence propositions and 88.8% for atomic claim propositions in LLM-written text
	- **How**: 3-class classification task (Supported, Not Supported, Not Addressed) evaluated using Percentage Agreement and Gwet's Agreement Coefficient 1 (AC1) against denoised human clinician ground truth
	- **Who**: VeriFact system (Llama 3.1 70B + retrieval components) tested on VeriFact-BHC dataset with 13,290 statements from 100 patients from MIMIC-III Clinical Database
- Performance on entailment tasks was critically dependent on retrieval volume, with the number of retrieved facts being identified as the most important hyperparameter affecting system effectiveness. #evd-candidate ^evd-002
	- **What**: Performance metrics across different numbers of retrieved facts, with hardware constraints limiting experiments to 50 facts but showing performance had not yet saturated
	- **How**: Hyperparameter optimization experiments comparing different retrieval configurations (top N facts, retrieval methods) and measuring agreement with ground truth
	- **Who**: VeriFact system tested with various retrieval configurations on clinical propositions from MIMIC-III derived dataset
- The AI system showed strong discriminative ability for supported claims but exhibited systematic bias in distinguishing between 'Not Supported' and 'Not Addressed' categories compared to human judgments. #evd-candidate ^evd-003
	- **What**: Classification performance showing good discrimination of Supported propositions but bias toward assigning 'Not Supported' rather than 'Not Addressed' verdicts when propositions were not supported
	- **How**: Analysis of confusion patterns between AI system predictions and human clinician labels across the 3-class classification scheme
	- **Who**: VeriFact system performance compared against human clinician judgments on clinical propositions from 100 patients
- Binarizing the classification task from 3-class to 2-class improved agreement by 10-15%, indicating better AI performance on simpler entailment decisions. #evd-candidate ^evd-004
	- **What**: 10-15% increase in percentage agreement, plus corresponding increases in sensitivity and positive predictive value when combining negative labels into single category
	- **How**: Comparison of performance metrics between 3-label classification (Supported, Not Supported, Not Addressed) versus 2-label classification (Supported vs. Not Supported or Addressed)
	- **Who**: Same VeriFact system and dataset, with labels reorganized for binary classification analysis
- Advanced retrieval techniques (hybrid and rerank methods) significantly outperformed basic retrieval approaches for entailment verification tasks. #evd-candidate ^evd-005
	- **What**: Performance improvements when using hybrid retrieval with re-ranker model compared to basic retrieval methods
	- **How**: Comparative evaluation of different information retrieval methods (basic vs. hybrid vs. rerank) integrated with the LLM-as-a-Judge approach
	- **Who**: VeriFact system using BAAI/bge-m3 embedding model and BAAI/bge-reranker-v2-m3 cross-encoder, tested on clinical fact-checking dataset
- Expanding the evidence scope from current admission only to entire patient EHR improved entailment verification performance. #evd-candidate ^evd-006
	- **What**: Higher agreement scores when retrieving facts from patient's complete EHR versus limiting retrieval to current hospital admission only
	- **How**: Controlled comparison of retrieval scope as a hyperparameter, measuring agreement with human clinician ground truth under different evidence availability conditions
	- **Who**: Clinical propositions from 100 patients with varying amounts of historical EHR data available for fact retrieval
- The LLM-as-a-Judge component showed insensitivity to temporal ordering and context formatting in the retrieved evidence. #evd-candidate ^evd-007
	- **What**: No significant performance differences between different reference context formats (Absolute Time vs. Relevance Score ordering)
	- **How**: Systematic comparison of different evidence presentation formats to the language model judge, measuring impact on classification accuracy
	- **Who**: Llama 3.1 70B model acting as judge, evaluated on clinical propositions with differently formatted reference contexts
- The system's effectiveness was limited by the quality and completeness of the underlying evidence source, with EHR errors and omissions directly impacting performance. #evd-candidate ^evd-008
	- **What**: Performance degradation and label assignment errors when EHRs contained erroneous information or had missing patient records
	- **How**: Analysis of failure cases where system performance was affected by underlying data quality issues, including misdiagnosis, miscommunication, or copy-pasted outdated information in EHRs
	- **Who**: MIMIC-III dataset with known limitations including de-identification tokens and real-world EHR data quality issues affecting 100 patients

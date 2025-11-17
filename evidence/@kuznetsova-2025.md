# Fact-checking with Generative AI: A Systematic Cross-Topic Examination of LLMs Capacity to Detect Veracity of Political Information

**Authors:** Elizaveta Kuznetsova, Ilaria Vitulano, M. Makhortykh, Martha Stolze, Tomas Nagy, Victoria Vziatysheva
**Year:** 2025
**DOI:** 10.48550/arXiv.2503.08404
**Citation Count:** 1

## Evidence Items

- ChatGPT-4 achieved macro F1 scores of 0.36 for true statements, 0.63 for mixed statements, and 0.77 for false statements, demonstrating strong performance on false claim detection but poor performance on true claim verification. #evd-candidate ^evd-001
	- **What**: Macro F1 scores across three veracity categories (true, mixed, false) with specific numerical values
	- **How**: Systematic evaluation using precision, recall, and F1 metrics with AI auditing methodology comparing LLM outputs to ground truth labels
	- **Who**: ChatGPT-4 model tested on 16,513 fact-checked statements from ClaimsKG dataset sourced from eight fact-checking organizations
- All five tested LLMs (ChatGPT-4, Llama 3 70B, Llama 3.1 405B, Claude 3.5 Sonnet, Google Gemini) consistently performed best at identifying false statements compared to true or mixed statements. #evd-candidate ^evd-002
	- **What**: Comparative performance rankings across veracity categories showing systematic bias toward false statement detection
	- **How**: Cross-model comparison using standardized prompting (temperature 0.1) and 4-class classification (TRUE, FALSE, MIXTURE, N/A)
	- **Who**: Five state-of-the-art LLMs evaluated on the same 16,513 political fact-checking statements
- ChatGPT-4 achieved 80% recall for false statements but LLMs performed particularly poorly on true statements with F1 scores ranging from only 0.25 to 0.36 across all models. #evd-candidate ^evd-003
	- **What**: Recall percentages for false statements and F1 score ranges for true statement detection across all models
	- **How**: Statistical analysis using recall and F1 metrics to measure model ability to correctly identify different veracity categories
	- **Who**: All five LLMs tested (ChatGPT-4, Llama models, Claude 3.5 Sonnet, Google Gemini) on ClaimsKG dataset
- Models showed statistically significantly higher agreement with ground truth on sensitive topics, with ChatGPT-4 showing 133% higher odds of agreement on COVID-19 controversies and 151% higher odds on North American politicians' controversies for false statements. #evd-candidate ^evd-004
	- **What**: Odds ratios showing percentage increases in agreement rates for specific topic categories compared to baseline topics
	- **How**: Logistic regression analysis combined with topic modeling to identify topic-specific performance variations
	- **Who**: ChatGPT-4 model performance analyzed across topic-segmented subsets of the 16,513 statement dataset
- Llama 3.1 405B (larger parameter version) outperformed Llama 3 70B across all statement categories, demonstrating that increased model scale improves fact-checking performance. #evd-candidate ^evd-005
	- **What**: Performance comparisons between two versions of the same model family with different parameter counts (70B vs 405B)
	- **How**: Direct comparison of F1 scores and other metrics between model versions using identical evaluation procedures
	- **Who**: Two Llama model versions (3 70B and 3.1 405B) tested on the same ClaimsKG dataset
- Llama 3 70B achieved the highest precision for false statements (88% probability that statements labeled false by the model were also labeled false by ground truth), while ChatGPT-4 performed best for true and mixed statement precision. #evd-candidate ^evd-006
	- **What**: Precision percentages showing conditional probability of ground truth agreement given model predictions
	- **How**: Precision metric calculation measuring the proportion of model predictions that matched professional fact-checker labels
	- **Who**: Llama 3 70B and ChatGPT-4 models evaluated against ClaimsKG professional fact-checker ground truth labels
- Claude 3.5 Sonnet and Google Gemini achieved better recall performance for mixed statements (0.7 and 0.81 respectively) compared to other models, indicating specialized strengths in detecting partially true claims. #evd-candidate ^evd-007
	- **What**: Recall scores specifically for the mixed/partially true statement category showing model-specific advantages
	- **How**: Recall metric analysis measuring models' ability to correctly identify statements containing both true and false elements
	- **Who**: Claude 3.5 Sonnet and Google Gemini models tested on mixed veracity statements from the ClaimsKG dataset
- Topic modeling revealed that U.S. Social Issues showed 46% higher odds of agreement between Llama 3.1 405B and ground truth compared to the reference topic, demonstrating topic-dependent performance variation. #evd-candidate ^evd-008
	- **What**: Statistically significant odds ratios showing topic-specific performance differences compared to baseline reference topics
	- **How**: Topic modeling combined with logistic regression analysis to quantify performance variations across subject matter categories
	- **Who**: Llama 3.1 405B model performance analyzed across topic-segmented portions of 16,513 political statements

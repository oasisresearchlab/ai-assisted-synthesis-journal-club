# Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition

**Authors:** Majeed Kazemitabaar, Jack Williams, Ian Drosos, Tovi Grossman, Austin Z Henley, Carina Negreanu, Advait Sarkar
**Year:** 2024
**DOI:** N/A
**Citation Count:** 38

## Evidence Items

- No significant differences in task completion time or verification hints between Stepwise, Phasewise, and Conversational baseline systems #evd-candidate ^evidence-000
	- **What**: Task completion time and verification hints usage
	- **How**: Controlled, within-subjects experiment comparing three system conditions
	- **Who**: 18 participants experienced in Python programming and data analysis
- Significant improvements in user control and ease of intervention with Stepwise and Phasewise compared to Conversational baseline #evd-candidate ^evidence-001
	- **What**: User satisfaction metrics for control and ease of intervention
	- **How**: Controlled, within-subjects experiment with satisfaction measurements
	- **Who**: 18 participants experienced in Python programming and data analysis
- Users valued side conversations and found structured approach facilitated verification and control #evd-candidate ^evidence-002
	- **What**: Qualitative user feedback on system features and approach
	- **How**: User feedback collection during controlled experiment
	- **Who**: 18 participants experienced in Python programming and data analysis

### Verification Snippets (evidence-000)

**Text Quotes:**

> Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition UIST ’24, October 13–16, 2024, Pittsburgh, PA, USA Table 2: Final tasks used in the evaluation, including the exact queries for each task, the datasets involved, and issues the AI would encounter without user intervention. Natural Language Query Dataset Issues Task 1: Show me the top five highly...
>
> *— Page 11*

> Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition UIST ’24, October 13–16, 2024, Pittsburgh, PA, USA the two new systems, and found intervention, correction, and veri­ fication easier, compared to the baseline. This paper makes the following contributions: • A formative study that identifies the limitations of “conver­ sational” AI tools in terms...
>
> *— Page 3*

> Improving Steering and Verification in AI-Assisted Data Analysis with Interactive Task Decomposition UIST ’24, October 13–16, 2024, Pittsburgh, PA, USA result first and then trim it”. P18 wanted to “look at the result first and if the result was nonsense then go back”. This was particularly the case in the Phasewise and Stepwise systems, as P4 mentioned that the system made them “go through all...
>
> *— Page 15*

> UIST ’24, October 13–16, 2024, Pittsburgh, PA, USA Kazemitabaar, et al. Very Difficult Very Easy Very Difficult B P S B P S B P S B P S B P S B P S B P S B P S Very Easy Very Difficult Very Easy Very Difficult Very Easy Not at all Completely Not at all Extremely Extremely Not at all Extremely Not at all Q8. To what extent did you feel overwhelmed by the amount of information displayed in the UI...
>
> *— Page 12*

> Abstract LLM-powered tools like ChatGPT Data Analysis, have the potential to help users tackle the challenging task of data analysis program­ ming, which requires expertise in data processing, programming, and statistics. However, our formative study (n=15) uncovered seri­ ous challenges in verifying AI-generated results and steering the AI (i.e., guiding the AI system to produce the desired...
>
> *— Page 2*


**Search Metadata:**
- Verified: 2025-12-10
- Chunks searched: 19
- Relevant snippets found: 5 text

---


## Claim Items

- Task decomposition with editable assumptions enhances user control in AI-assisted data analysis without sacrificing task completion efficiency #clm-candidate ^claim-000
- Providing users with direct control over AI's assumptions and execution plan improves steering and verification capabilities #clm-candidate ^claim-001
- Structured decomposition approaches can facilitate user verification and control while maintaining cognitive manageability #clm-candidate ^claim-002
- Users need necessary controls to make informed decisions and maintain control over AI-assisted data analysis processes #clm-candidate ^claim-003

## Pattern Items

- Interactive task decomposition - breaking complex data analysis tasks into manageable subgoals with user control points #ptn-candidate ^pattern-000
- Steering points pattern - providing specific moments where users can intervene and modify AI assumptions or execution plans #ptn-candidate ^pattern-001
- Progressive disclosure with editable assumptions - revealing AI reasoning incrementally while allowing user modifications #ptn-candidate ^pattern-002
- Dual-modality interaction - combining structured decomposition with flexible conversational elements #ptn-candidate ^pattern-003
- Side conversation pattern - enabling parallel queries and clarifications without disrupting main task flow #ptn-candidate ^pattern-004

## Artifact Items

- Stepwise system - AI assistant that decomposes data analysis tasks into step-by-step subgoals with editable assumptions and code #art-candidate ^artifact-000
- Phasewise system - AI assistant that structures data analysis into three editable phases with user control over assumptions #art-candidate ^artifact-001
- Web application built with TypeScript and React, using Python server for dataset management and GPT-4 Turbo for AI assistance #art-candidate ^artifact-002

## Question Items

- How might we help vernacular software developers comprehend code using AI? ^question-000
- How can task decomposition improve steering and verification in AI-assisted data analysis? ^question-001

## Identified Relations

- Evidence 'Significant improvements in user control and ease ...' **supports** Claim 'Providing users with direct control over AI's assu...'
- Evidence 'Users valued side conversations and found structur...' **supports** Claim 'Structured decomposition approaches can facilitate...'
- Evidence 'No significant differences in task completion time...' **supports** Claim 'Task decomposition with editable assumptions enhan...'
- Evidence 'Significant improvements in user control and ease ...' **supports** Claim 'Task decomposition with editable assumptions enhan...'
- Claim 'Providing users with direct control over AI's assu...' **supports** Claim 'Users need necessary controls to make informed dec...'
- Claim 'Structured decomposition approaches can facilitate...' **supports** Claim 'Task decomposition with editable assumptions enhan...'
- Artifact 'Stepwise system - AI assistant that decomposes dat...' **involves** Pattern 'Interactive task decomposition - breaking complex ...'
- Artifact 'Stepwise system - AI assistant that decomposes dat...' **involves** Pattern 'Progressive disclosure with editable assumptions -...'
- Artifact 'Phasewise system - AI assistant that structures da...' **involves** Pattern 'Interactive task decomposition - breaking complex ...'
- Artifact 'Phasewise system - AI assistant that structures da...' **involves** Pattern 'Progressive disclosure with editable assumptions -...'
- Pattern 'Steering points pattern - providing specific momen...' **informs** Claim 'Providing users with direct control over AI's assu...'
- Pattern 'Interactive task decomposition - breaking complex ...' **informs** Claim 'Structured decomposition approaches can facilitate...'
- Pattern 'Progressive disclosure with editable assumptions -...' **informs** Claim 'Providing users with direct control over AI's assu...'
- Pattern 'Side conversation pattern - enabling parallel quer...' **informs** Claim 'Structured decomposition approaches can facilitate...'
- Artifact 'Stepwise system - AI assistant that decomposes dat...' **informs** Evidence 'Significant improvements in user control and ease ...'
- Artifact 'Phasewise system - AI assistant that structures da...' **informs** Evidence 'Significant improvements in user control and ease ...'
- Artifact 'Stepwise system - AI assistant that decomposes dat...' **informs** Evidence 'No significant differences in task completion time...'
- Artifact 'Phasewise system - AI assistant that structures da...' **informs** Evidence 'No significant differences in task completion time...'

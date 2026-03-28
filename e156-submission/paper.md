Mahmood Ahmad
Tahir Heart Institute
author@example.com

MetaExtract: Browser-Based Effect Estimate Extraction from Clinical Trial Abstracts via Deterministic Pattern Matching

Can a browser-based tool reliably extract structured effect estimates from clinical trial abstracts without server-side processing? We built MetaExtract, a single-file HTML application implementing 18 regex patterns for hazard ratios, odds ratios, risk ratios, mean differences, and numbers needed to treat, with confidence interval parsing and p-value linkage. The extractor applies Unicode normalization, plausibility checks against clinically bounded ranges, and confidence scoring classifying extractions as auto-verified, spot-check, or needs-review based on pattern specificity. Across 50 cardiology and oncology abstracts, MetaExtract sensitivity was 94 percent (95% CI 89 to 99) for reported HR, OR, and RR estimates with confidence intervals, achieving a false-positive rate below 3 percent after plausibility filtering. Integration with ClinicalTrials.gov via NCT identifier enables automated parsing of registry results alongside published abstracts. Deterministic pattern matching with domain-specific plausibility constraints provides practical extraction accuracy for systematic review screening. The regex approach cannot parse estimates in figures or supplementary tables and degrades on non-English language abstracts.

Outside Notes

Type: methods
Primary estimand: Extraction sensitivity for HR, OR, RR (95% CI)
App: MetaExtract v1.0
Data: 50 cardiology and oncology trial abstracts; ClinicalTrials.gov integration
Code: https://github.com/mahmood726-cyber/metaextract
Version: 1.0
Certainty: moderate
Validation: DRAFT

References

1. Reitsma JB, Glas AS, Rutjes AW, et al. Bivariate analysis of sensitivity and specificity produces informative summary measures in diagnostic reviews. J Clin Epidemiol. 2005;58(10):982-990.
2. Macaskill P, Gatsonis C, Deeks JJ, Harbord RM, Takwoingi Y. Cochrane Handbook for Systematic Reviews of Diagnostic Test Accuracy. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.

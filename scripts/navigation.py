# -*- coding: utf-8 -*-
"""
navigation.py - the routing content: which book for which problem, and in what order.

This is the part of the site that neither gradsummit.com nor
researchmadepractical.com can carry. Each of those holds one series, so neither
can route a reader across all four. Only a page that sees the whole library can
say "for that problem, these two books, and read them in this order".

It is also the part that is wholly original — no book description is reproduced,
so none of it competes with the pages it links to.

Entries reference books by slug. build_site.py fails loudly on an unknown slug
rather than silently dropping a recommendation.
"""

# (the situation in the reader's words, what to reach for, [slugs])
CHOOSER = [
    ("I have to pick a research design and do not know where to start",
     "Start with the design guide, then the workbook that makes you write the choice down.",
     ["research-design-simplified", "dissertation", "clinical-research-design-simplified"]),
    ("I am drowning in papers and my literature review has no shape",
     "One book for the method, one workbook for the extraction, one for a deadline.",
     ["literature-review-simplified-2e", "systematic-review",
      "dissertation-literature-review-sprint"]),
    ("I need to run a systematic review or meta-analysis",
     "Protocol first, then the synthesis. The healthcare edition if your evidence is clinical.",
     ["systematic-review", "systematic-reviews-healthcare-simplified"]),
    ("I am about to interview people and have never done it",
     "Protocol design and recruitment first. Coding comes after the data exists.",
     ["interview", "qualitative"]),
    ("I have transcripts and no idea how to code them",
     "The coding workbook for the process; the AI book if you want software help with it.",
     ["qualitative", "qda-with-chatgpt-and-qualcoder"]),
    ("I do not know which statistical test applies to my data",
     "The decision trees, plus the assumption checks that stop a reviewer sending it back.",
     ["statistical-test", "public-health-research-simplified"]),
    ("I have to write a proposal or protocol that gets approved",
     "The proposal book for academic work; the protocol workbook if it is a trial.",
     ["research-proposal-writing-simplified", "clinical-trial-protocol", "grant-writing"]),
    ("I have been told to do an audit or a QI project",
     "One integrated cycle, from a ward problem to a signed-off portfolio entry.",
     ["clinical-audit-quality-improvement"]),
    ("My programme requires an evidence-based practice project",
     "PICO to implemented change, using the appraisal models you are examined on.",
     ["evidence-based-practice-project"]),
    ("I have a case worth reporting and have never written one",
     "Consent and de-identification before drafting, then CARE, then the journal.",
     ["clinical-case-report"]),
    ("Something works but nobody is doing it",
     "Diagnose with CFIR, match ERIC strategies, measure with RE-AIM.",
     ["implementation-science"]),
    ("I need to turn finished work into a published paper",
     "The writing mechanics first, then the submission itself.",
     ["write-and-publish-scientific-paper", "academic-writing"]),
]

# (track name, who it is for, [slugs in reading order])
PATHWAYS = [
    ("The doctorate, start to finish",
     "A PhD or professional doctorate, from first idea to defended thesis.",
     ["phd-journey-simplified", "research-design-simplified", "literature-review-simplified-2e",
      "qualitative", "statistical-test", "academic-writing"]),
    ("The clinician's first project",
     "The order the Clinical Practice series was written in. Each workbook assumes the one "
     "before it, and the implementation workbook is explicitly the step up from the first two.",
     ["clinical-audit-quality-improvement", "evidence-based-practice-project",
      "clinical-case-report", "implementation-science", "clinical-trial-protocol"]),
    ("Evidence synthesis",
     "A systematic review or meta-analysis, academic or clinical.",
     ["literature-review-simplified-2e", "systematic-review",
      "systematic-reviews-healthcare-simplified"]),
    ("First publication",
     "Turning work you have already done into something submittable.",
     ["academic-writing", "write-and-publish-scientific-paper", "clinical-case-report"]),
]

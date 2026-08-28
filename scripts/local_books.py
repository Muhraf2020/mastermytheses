# -*- coding: utf-8 -*-
"""
local_books.py - the eight books whose only web home is this site.

WHY THESE LIVE HERE AND THE OTHER EIGHTEEN DO NOT
-------------------------------------------------
Audited 2026-08-28 across all four repositories: not one of these eight ASINs or
paperback ISBNs appeared anywhere the author publishes. The Mastering Research
series is catalogued on gradsummit.com and the Research Made Practical workbooks
on researchmadepractical.com, but the two clinical series had no web presence at
all.

So this site is their canonical home, and these pages carry full original copy.
The other eighteen books get short cards that link OUT to their existing pages —
see scripts/external_books.py. That split is what keeps this site from competing
with the other two.

COPY IS WRITTEN, NOT COPIED
---------------------------
The blurbs below are original. They are informed by the published descriptions
and are factually faithful to them — template counts, framework names and the
deliverables are checked against the listings — but they are not the Amazon copy
pasted across. Reusing a marketplace description verbatim duplicates against a
listing that already ranks, which costs the page its own chance to.

AUDIENCE
--------
These two series are written for clinicians — foundation doctors, residents,
nurses, allied-health professionals, DNP/DrPH students. That is a different
reader from the generic graduate researcher the other two sites serve, and a
different search vocabulary (clinical audit, EBP project, CARE, SPIRIT, CFIR),
which is the second reason these pages cannot cannibalise the others.
"""

SERIES_CLINICAL = "Clinical Practice & Applied Research Workbooks"
SERIES_HEALTHCARE = "Healthcare Research Simplified"

# Shelf keys, shared with external_books.py so the library groups cleanly:
# plan / evidence / fieldwork / analysis / writing / clinical.
LOCAL_BOOKS = [
    {
        "slug": "clinical-audit-quality-improvement",
        "series": SERIES_CLINICAL,
        "order": 1,
        "title": "The Clinical Audit & Quality Improvement Project Workbook",
        "short": "Clinical Audit & QI",
        "tagline": "From a problem you noticed on the ward to a signed-off, portfolio-ready project.",
        "templates": 60,
        "asin": "B0H5R9LMYQ",
        "paperback_isbn": "9199132257",
        "stages": ["clinical"],
        "audience": "Foundation doctors, residents, nurses, allied health",
        "frameworks": ["HQIP", "IHI Model for Improvement", "SQUIRE 2.0"],
        "problem": (
            "Every doctor in training has to complete an audit or quality-improvement "
            "project. The requirement is clear; the help is not. What is usually on offer "
            "is a dense guideline that explains the theory and leaves you looking at a "
            "blank page a week before your ARCP."
        ),
        "approach": (
            "This workbook treats audit and quality improvement as one integrated cycle "
            "rather than two separate worlds, and carries a single worked project from "
            "first idea to portfolio entry while you build your own alongside it."
        ),
        "outcomes": [
            "A correctly classified, registered project on the right governance route, with the ethics question settled",
            "A SMART aim with a number and a date, resting on a defensible baseline",
            "A driver diagram and root-cause analysis explaining why the gap exists",
            "A PDSA improvement ramp and a run chart that distinguish real change from noise",
            "A like-for-like re-audit that closes the loop",
            "A SQUIRE 2.0 write-up, an abstract and poster, and a supervisor-signed portfolio entry mapped to your curriculum",
        ],
    },
    {
        "slug": "evidence-based-practice-project",
        "series": SERIES_CLINICAL,
        "order": 2,
        "title": "The Evidence-Based Practice Project Workbook",
        "short": "Evidence-Based Practice",
        "tagline": "Take a clinical question from PICO to an implemented, evaluated change in practice.",
        "templates": 58,
        "asin": "B0H5RR5P97",
        "paperback_isbn": "9199132265",
        "stages": ["clinical", "evidence"],
        "audience": "Nursing and allied-health students, DNP candidates",
        "frameworks": ["Johns Hopkins", "Melnyk", "Iowa", "CASP", "JBI", "GRADE"],
        "problem": (
            "An EBP project is a course requirement across nearly every nursing and "
            "allied-health programme, and the standard text is a reference work rather "
            "than a hand-rail. Students read hundreds of pages and still cannot produce "
            "the artefacts they are actually graded on."
        ),
        "approach": (
            "Built on the appraisal models clinicians are examined against, and holding one "
            "line bright throughout: evidence-based practice uses existing evidence to change "
            "care. It is not research, and it usually needs no ethics review — a distinction "
            "that saves weeks."
        ),
        "outcomes": [
            "A searchable PICO(T) question and a justified EBP model",
            "A documented, reproducible search and a screened evidence set",
            "Every study levelled, appraised, and synthesised into a graded recommendation",
            "An approvable change proposal, a pilot, and an implementation that checks fidelity",
            "Outcome, process and balancing measures that show whether it worked",
            "A rubric map, a reflective entry and faculty sign-off, ready for a portfolio or capstone",
        ],
    },
    {
        "slug": "clinical-case-report",
        "series": SERIES_CLINICAL,
        "order": 3,
        "title": "The Clinical Case Report & Case Series Workbook",
        "short": "Case Report & Case Series",
        "tagline": "From consent and de-identification to a CARE-ready, submittable case report.",
        "templates": 52,
        "asin": "B0H5TKFCYK",
        "paperback_isbn": "9199132273",
        "stages": ["clinical", "writing"],
        "audience": "Clinicians writing their first publication",
        "frameworks": ["CARE", "ICMJE", "COPE", "DOAJ"],
        "problem": (
            "Most clinicians meet a case worth reporting long before they know how to write "
            "one. Consent, de-identification, the CARE checklist, the timeline figure, the "
            "right journal — get any of them wrong and the work is desk-rejected before a "
            "reviewer reads it, or a patient is identifiable in print."
        ),
        "approach": (
            "Patient confidentiality comes first, the way a journal treats it: the consent and "
            "de-identification chapters sit before you write a word, and the worked example "
            "models the standard it teaches throughout."
        ),
        "outcomes": [
            "A case-worthiness decision and a single, sharp teaching point",
            "Documented consent and a de-identification standard a journal will accept",
            "Your case mapped to the CARE checklist before you draft",
            "A clean timeline figure — the element trainees most often get wrong",
            "Every section written: presentation, findings, assessment, intervention, outcomes",
            "A screened, indexed journal match and a complete submission package",
        ],
    },
    {
        "slug": "implementation-science",
        "series": SERIES_CLINICAL,
        "order": 4,
        "title": "The Implementation Science Workbook",
        "short": "Implementation Science",
        "tagline": "Get a proven practice adopted, measured and sustained across a system.",
        "templates": 52,
        "asin": "B0H5WQRNK3",
        "paperback_isbn": "9199132281",
        "stages": ["clinical"],
        "audience": "Clinical leads, improvement teams, grant applicants",
        "frameworks": ["CFIR", "TDF", "ERIC", "Proctor", "RE-AIM", "EPIS", "StaRI"],
        "problem": (
            "Implementation science has powerful frameworks and a well-documented habit of "
            "being misapplied: a framework named but never used, barriers matched to "
            "strategies with no stated logic, a study that measures only the clinical outcome "
            "and so cannot explain why it failed."
        ),
        "approach": (
            "You do not read about CFIR here, you complete a CFIR assessment; you do not cite "
            "ERIC, you match and specify strategies. The step up from a local audit or EBP "
            "project to something that holds across a system."
        ),
        "outcomes": [
            "A classified project and a quantified know-do gap",
            "A completed CFIR determinant assessment and a prioritised barrier register",
            "ERIC strategies matched to your barriers and specified so others can replicate them",
            "Proctor implementation outcomes measured alongside the clinical one",
            "A RE-AIM evaluation across all five dimensions, not effectiveness alone",
            "A hybrid design, an EPIS phasing plan, and a sustainability and de-implementation plan",
            "A StaRI-structured report and a fundable implementation section for a grant",
        ],
    },
    {
        "slug": "clinical-trial-protocol",
        "series": SERIES_CLINICAL,
        "order": 5,
        "title": "The Clinical Trial Protocol & Regulatory Workbook",
        "short": "Trial Protocol & Regulatory",
        "tagline": "Build a SPIRIT-2025-complete, GCP-ready protocol your ethics committee will approve.",
        "templates": 63,
        "asin": "B0H5VT2TZJ",
        "paperback_isbn": "919913229X",
        "stages": ["clinical", "plan"],
        "audience": "First-time investigators, trial coordinators",
        "frameworks": ["SPIRIT 2025", "ICH-GCP", "CONSORT 2025", "TIDieR", "ICH E9(R1)"],
        "problem": (
            "The SPIRIT checklist is free, and it tells you what a protocol must contain — not "
            "how to write one. Framing an estimand, laying out a schedule of assessments, "
            "justifying a sample size to a committee, running a consent process rather than "
            "collecting a signature: none of that is in the checklist."
        ),
        "approach": (
            "Built on the SPIRIT 2025 skeleton with the regulatory-operations layer that pure "
            "design books leave out — consent, delegation, safety reporting, monitoring, "
            "registration and the trial master file."
        ),
        "outcomes": [
            "A classified trial and a SPIRIT-2025-mapped protocol under version control",
            "Clear objectives, a defined estimand (ICH E9 R1) and an endpoint hierarchy",
            "A design, randomisation, allocation-concealment and blinding plan",
            "Eligibility criteria that actually recruit, and a TIDieR intervention description",
            "A sample-size justification, an analysis-plan skeleton, a CRF and data-management plan",
            "A plain-language consent package, a GCP safety and monitoring plan, and a registration and submission package",
        ],
    },
    {
        "slug": "clinical-research-design-simplified",
        "series": SERIES_HEALTHCARE,
        "order": 1,
        "title": "Clinical Research Design Simplified",
        "short": "Clinical Research Design",
        "tagline": "A step-by-step guide for nurses, physicians and allied-health researchers.",
        "templates": None,
        "asin": "B0GHPD1XZC",
        "paperback_isbn": None,
        "stages": ["plan"],
        "audience": "Clinicians designing their first study",
        "frameworks": ["PICOT", "FINER"],
        "problem": (
            "Clinicians see the problem on the ward every day and know there should be a "
            "better way. Turning that observation into a study that survives an IRB and holds "
            "up under scrutiny is a different skill, and it is rarely taught to people who "
            "already have a full clinical job."
        ),
        "approach": (
            "Written for practising healthcare professionals rather than methodologists: no "
            "prior research background assumed, and no statistics degree required to follow it."
        ),
        "outcomes": [
            "Clinical questions turned into researchable ones using PICOT and FINER",
            "A study design matched to the question rather than to habit",
            "A protocol that anticipates what an ethics committee will ask",
            "Sampling, measurement and analysis planned before data collection starts",
        ],
    },
    {
        "slug": "public-health-research-simplified",
        "series": SERIES_HEALTHCARE,
        "order": 2,
        "title": "Public Health Research Simplified",
        "short": "Public Health Research",
        "tagline": "Plan, collect, analyse and communicate public-health research end to end.",
        "templates": None,
        "asin": "B0G6LNMMS3",
        "paperback_isbn": None,
        "stages": ["plan", "analysis"],
        "audience": "Public health students and practitioners",
        "frameworks": ["R", "Python"],
        "problem": (
            "Population-level work has its own constraints — equity, ethics, messy secondary "
            "data, and findings that have to persuade programme and policy audiences rather "
            "than only reviewers. A general methods textbook does not cover that."
        ),
        "approach": (
            "Ethics-first and equity-centred, following one workflow from problem to question "
            "to design to data to analysis to reporting, with checklists, decision trees and "
            "runnable code in R and Python rather than pseudocode."
        ),
        "outcomes": [
            "Community and system problems turned into precise research questions",
            "The right design chosen across cross-sectional, cohort, trial, qualitative and mixed methods",
            "An ethics and data-governance plan appropriate to population data",
            "Analysis you can actually run, and reporting aimed at programmes and policy",
        ],
    },
    {
        "slug": "systematic-reviews-healthcare-simplified",
        "series": SERIES_HEALTHCARE,
        "order": 3,
        "title": "Systematic Reviews and Meta-Analysis in Healthcare Simplified",
        "short": "Systematic Reviews in Healthcare",
        "tagline": "From protocol to publication, without a statistics PhD.",
        "templates": None,
        "asin": "B0GHP6BZ12",
        "paperback_isbn": None,
        "stages": ["evidence", "analysis"],
        "audience": "DNP, dissertation and guideline-development teams",
        "frameworks": ["PICO", "PRISMA", "GRADE"],
        "problem": (
            "A committee asks for a systematic review, or a DNP project requires one, and the "
            "only models available are finished Cochrane reviews running to fifty pages. They "
            "show the destination and nothing of the route."
        ),
        "approach": (
            "The whole sequence in order — question, protocol, search, screening, extraction, "
            "appraisal, synthesis, and the meta-analysis itself — at a level that assumes "
            "clinical training rather than research training."
        ),
        "outcomes": [
            "A focused, answerable review question and a registered protocol",
            "A reproducible search strategy and a documented screening process",
            "Extraction and risk-of-bias appraisal you can defend",
            "A synthesis, and a meta-analysis where the data support one",
            "A PRISMA-compliant manuscript ready to submit",
        ],
    },
]

# -*- coding: utf-8 -*-
"""
book_detail.py - the long-form content for the eight books published here.

WHY THIS IS SEPARATE FROM local_books.py
----------------------------------------
local_books.py is the spine: identifiers, ISBNs, shelving, the one-line tagline.
This is the prose. Keeping them apart means the build can be reasoned about
without scrolling past several thousand words of copy, and a factual correction
(an ISBN, a shelf) never risks disturbing the writing.

WHY IT EXISTS AT ALL
--------------------
The first build gave each book a page of about 250 words. Structurally correct —
canonical, Book schema, internal links — but thin, against roughly 1,800 words on
a comparable gradsummit book page. Thin pages do not rank, and ranking is the
entire reason these eight books needed a home. This is the fix.

Every field is written, not copied. The Amazon descriptions were the source for
the facts — template counts, chapter counts, framework names, deliverables — and
those are reproduced faithfully. The prose is not, because duplicating a
marketplace listing that already ranks costs the page its own chance to.

Fields per slug:
  who        who the book is for (list)
  not_for    who should look elsewhere, and where — stated plainly, because a
             book page that will not say who it is wrong for is an advert
  inside     what the book actually contains, in order (list)
  differs    what this adds over the free official guidance it operationalises
  faq        [(question, answer)] — rendered as <details> and as FAQPage JSON-LD
"""

DETAIL = {

    # ---------------------------------------------------------------- clinical
    "clinical-audit-quality-improvement": {
        "who": [
            "Foundation doctors and residents with an audit requirement and an ARCP date",
            "Nurses and allied-health professionals running a ward-level improvement project",
            "Supervisors who keep sending the same project back for the same reasons",
        ],
        "not_for": (
            "This is not a research-methods book. If your project is designed to produce "
            "generalisable new knowledge rather than to improve local care, you are doing "
            "research and need ethics approval — start with a research design guide instead."
        ),
        "inside": [
            "Classifying the project — audit, quality improvement, or research — and taking the right governance route",
            "Registering it, and settling the ethics question before it costs you weeks",
            "Finding the standard: what good looks like, and where the criterion comes from",
            "A defensible baseline measurement, with a sample you can justify",
            "A SMART aim that carries a number and a date",
            "Driver diagrams and root-cause analysis: why the gap exists, not just that it does",
            "PDSA cycles as a ramp rather than a single test",
            "Run charts, and the rules that separate signal from noise",
            "The re-audit, measured like for like so the comparison means something",
            "Writing up to SQUIRE 2.0, plus abstract, poster, and a curriculum-mapped portfolio entry",
        ],
        "differs": (
            "HQIP guidance, the IHI Model for Improvement and the SQUIRE 2.0 checklist are all "
            "free, and all of them describe the destination rather than the route. They tell you "
            "a project needs a defensible baseline; they do not sit with you while you choose a "
            "sample size, or tell you that measuring the re-audit differently from the baseline "
            "is the single most common reason a project is rejected. This workbook is the "
            "coaching around those standards, one page at a time."
        ),
        "faq": [
            ("Is this audit or quality improvement?",
             "Both, deliberately. Most trainees are told to do one and end up doing the other, "
             "because in practice they are one cycle: you measure against a standard, you find a "
             "gap, you change something, you measure again. Treating them as separate worlds is "
             "what produces audits that never improve anything and QI projects with no baseline."),
            ("Do I need ethics approval?",
             "Usually not, but the answer depends on classification rather than on topic — and "
             "getting it wrong in either direction is expensive. A project intended to improve "
             "local care against an existing standard is normally service evaluation or audit, "
             "and takes a governance route rather than an ethics one. The first chapter settles "
             "this before you invest any time."),
            ("What if my re-audit shows no improvement?",
             "That is a finding, and a publishable one. What makes it worthless is not being able "
             "to say why — which is what the driver diagram and root-cause work exist to prevent. "
             "A project that shows no change and explains the mechanism is stronger than one that "
             "shows improvement it cannot account for."),
            ("Will this satisfy my portfolio requirement?",
             "The final chapter produces a supervisor-signed entry mapped to curriculum "
             "competencies, which is the form most training programmes ask for. Requirements vary "
             "by deanery and specialty, so check yours against the mapping rather than assuming."),
        ],
    },

    "evidence-based-practice-project": {
        "who": [
            "Nursing and allied-health students with an EBP assignment or capstone",
            "DNP candidates building a scholarly project",
            "Faculty and preceptors who grade these and want students to arrive with the artefacts",
        ],
        "not_for": (
            "If you intend to generate new evidence rather than apply existing evidence, this is "
            "the wrong book — that is research, with the ethics review and design work that "
            "implies. If your change has already been implemented and you need it to spread "
            "across a system, the implementation workbook picks up where this one stops."
        ),
        "inside": [
            "Framing a searchable PICO(T) question, and choosing an EBP model you can justify",
            "A documented, reproducible search — the part most often lost and most often asked for",
            "Screening to a defensible evidence set",
            "Levelling every study with the hierarchy your programme examines you on",
            "Rapid critical appraisal using Johns Hopkins and Melnyk forms",
            "Synthesis into a graded recommendation rather than a summary of each paper",
            "A change proposal your unit will actually approve",
            "A pilot, and a fidelity check that tells you whether the change was really made",
            "Outcome, process and balancing measures",
            "A rubric and competency map, a reflective entry, and faculty sign-off",
        ],
        "differs": (
            "The standard EBP textbook is a reference work of several hundred pages. It explains "
            "everything and produces nothing. Students read it and still cannot hand in the "
            "evidence table, the synthesis or the change proposal they are actually graded on. "
            "This book keeps one distinction bright throughout — evidence-based practice applies "
            "existing evidence to change care, it is not research, and it usually needs no ethics "
            "review — and that single clarity routinely saves weeks."
        ),
        "faq": [
            ("Is an EBP project research?",
             "No, and confusing the two is the most expensive mistake in this work. Research "
             "generates new generalisable knowledge and needs ethics review. An EBP project "
             "applies evidence that already exists to change local care, and normally takes a "
             "governance route instead. Students who assume they need an IRB submission often "
             "lose a term to it."),
            ("Which model should I use — Johns Hopkins, Melnyk or Iowa?",
             "Whichever your programme teaches and examines, because you will be assessed against "
             "its language. The book covers all three and includes the appraisal forms for the "
             "first two; the workflow is the same whichever you choose, and the chapter on model "
             "selection makes you write down why you picked yours."),
            ("How many studies do I need?",
             "There is no threshold, and chasing a count produces padded evidence tables. What "
             "matters is that your search was documented and reproducible, your inclusion criteria "
             "were applied consistently, and the evidence you did find is levelled and appraised. "
             "A defensible six beats an unexplained twenty."),
            ("What if the evidence does not support a change?",
             "Then the recommendation is not to change, and that is a legitimate, gradeable "
             "result. The graded-recommendation chapter covers how to state it — with the "
             "strength of evidence made explicit — rather than forcing a change the evidence "
             "will not carry."),
        ],
    },

    "clinical-case-report": {
        "who": [
            "Clinicians with a case worth reporting and no publication yet",
            "Trainees whose portfolio expects a publication",
            "Supervisors and senior authors who keep fixing the same problems in drafts",
        ],
        "not_for": (
            "A case series of more than a handful of patients, or any design with a comparison "
            "group, is a different article type with different reporting standards. If you are "
            "synthesising published cases rather than reporting your own, you want the systematic "
            "review route instead."
        ),
        "inside": [
            "Screening the case for worthiness, and naming a single teaching point",
            "Consent — obtained and documented to the standard a journal will accept",
            "De-identification, with the standard modelled rather than described",
            "Mapping to the CARE checklist before drafting, not after",
            "The timeline figure, which trainees get wrong more often than any other element",
            "Presentation and clinical findings",
            "Diagnostic assessment, including what was excluded and why",
            "Intervention and outcomes, with follow-up stated honestly",
            "A discussion that argues rather than summarises, and explicit teaching points",
            "A findable title and abstract",
            "Screening a journal — indexed, legitimate, appropriate — and assembling the submission",
        ],
        "differs": (
            "The CARE guideline is free and it is a checklist: it tells you a case report needs a "
            "timeline, not how to build one that a copy-editor will accept. And it says nothing "
            "about the two things that sink first case reports before review — consent that will "
            "not stand up, and de-identification that leaves a patient recognisable. Those "
            "chapters come first here, and the worked example throughout models the standard it "
            "teaches: relative timing, no identifiers, nothing that could expose a real person."
        ),
        "faq": [
            ("Do I need written consent from the patient?",
             "For a case report, effectively always. Most journals require documented consent from "
             "the patient or their legal representative regardless of how thoroughly the case is "
             "de-identified, and many will not consider a submission without it. Obtain it before "
             "you write, not after — the consent chapter comes before the drafting chapters for "
             "that reason."),
            ("How de-identified does it have to be?",
             "Enough that the patient could not be recognised by someone who knows them — which is "
             "a higher bar than removing the name. Relative timing rather than dates, no unit or "
             "admission identifiers, and care with any combination of details that is individually "
             "innocuous and collectively unique. The book models this throughout."),
            ("Why do case reports get desk-rejected?",
             "Most often for scope mismatch with the journal, a missing or inadequate consent "
             "statement, no clear teaching point, or non-compliance with CARE. All four are "
             "avoidable before submission, and all four are checked here."),
            ("Can I publish a case report as a trainee?",
             "Yes, and it is the most common route to a first publication. What it requires is "
             "the discipline of the process rather than seniority — which is precisely what this "
             "workbook supplies."),
        ],
    },

    "implementation-science": {
        "who": [
            "Clinical leads rolling a proven practice out beyond one ward",
            "Improvement teams whose pilot worked and then stalled",
            "Grant applicants who need a defensible implementation section",
        ],
        "not_for": (
            "If you have not yet demonstrated the practice works locally, start with the audit and "
            "QI workbook or the EBP workbook — this one begins from a proven practice that is not "
            "being used. If you are testing whether an intervention works at all, that is "
            "effectiveness research, not implementation."
        ),
        "inside": [
            "Classifying the project and quantifying the know-do gap",
            "A CFIR determinant assessment, completed rather than cited",
            "A prioritised barrier and facilitator register",
            "Matching ERIC strategies to barriers, with the logic written down",
            "Specifying each strategy so another team could replicate it",
            "Proctor implementation outcomes, defined and measured alongside the clinical one",
            "A RE-AIM evaluation plan across all five dimensions",
            "Choosing a hybrid design, and phasing with EPIS",
            "Sustainability, and de-implementation of what the change replaces",
            "A StaRI-structured report, and a fundable implementation section",
        ],
        "differs": (
            "The CFIR team published a user guide specifically because of the misuse they kept "
            "seeing: a framework named in the methods and never used, barriers matched to "
            "strategies with no stated reasoning, CFIR and RE-AIM bolted together without "
            "distinguishing determinants from outcomes, and evaluations that measure only the "
            "clinical result and so cannot explain a failure. The free framework PDFs tell you "
            "what the frameworks are. They do not make you complete one. Here you do not read "
            "about CFIR, you complete a CFIR assessment."
        ),
        "faq": [
            ("What is the difference between quality improvement and implementation science?",
             "QI asks whether you can improve a local process. Implementation science asks why a "
             "practice already known to work is not being used, and what it takes to get it "
             "adopted and sustained across a system. Different question, different frameworks, "
             "different outcomes measured — and the second usually follows the first."),
            ("Do I have to use CFIR and RE-AIM together?",
             "They answer different questions and are commonly conflated. CFIR characterises "
             "determinants — what will help or hinder. RE-AIM evaluates outcomes across reach, "
             "effectiveness, adoption, implementation and maintenance. Using both is legitimate "
             "and common, provided you can say which does what in your study."),
            ("What are implementation outcomes, and why measure them separately?",
             "Proctor's set — acceptability, adoption, appropriateness, feasibility, fidelity, "
             "cost, penetration, sustainability — describe how well the change was delivered, "
             "distinct from whether the clinical outcome moved. Without them a null result is "
             "uninterpretable: you cannot tell whether the practice failed or was never really "
             "implemented."),
            ("Is this useful for a grant application?",
             "That is one of its stated purposes. The final chapter builds a fundable "
             "implementation section, and the specification of strategies is exactly the detail "
             "reviewers look for and rarely receive."),
        ],
    },

    "clinical-trial-protocol": {
        "who": [
            "First-time investigators told to write the protocol",
            "Trial coordinators and research nurses assembling a submission",
            "Clinical academics preparing an ethics or sponsor package",
        ],
        "not_for": (
            "This builds a protocol; it does not run the analysis. It supports rather than "
            "replaces your trial statistician, your sponsor's SOPs, and your regulatory-affairs "
            "and ethics specialists. It is not regulatory or statistical advice, and guideline "
            "versions change — verify them at the time you write."
        ),
        "inside": [
            "Classifying the trial, and mapping to the SPIRIT 2025 skeleton with version control",
            "Objectives, and a defined estimand under ICH E9(R1)",
            "An endpoint hierarchy that distinguishes primary from everything else",
            "Design, randomisation, allocation concealment and blinding",
            "Eligibility criteria that recruit rather than exclude everyone",
            "A TIDieR intervention description another site could deliver",
            "The schedule-of-assessments figure",
            "Sample-size justification a committee will accept",
            "An analysis-plan skeleton, CRF design and data-management plan",
            "A plain-language consent package, and consent as a process rather than a signature",
            "GCP safety reporting, monitoring, and the trial master file",
            "Prospective registration and the submission package",
        ],
        "differs": (
            "SPIRIT 2025, the NIH-FDA protocol template and ICH-GCP are all freely available, and "
            "between them they specify what a protocol must contain. None of them tells a "
            "first-time investigator how to frame an estimand, lay out a schedule of assessments, "
            "justify a sample size to a committee that will push back, or run a consent process "
            "rather than collect a signature. This workbook adds the regulatory-operations layer "
            "that pure design books omit — delegation, safety reporting, monitoring, registration, "
            "the master file — and carries one worked trial through all of it."
        ),
        "faq": [
            ("What is an estimand and why does it matter?",
             "An estimand states precisely what treatment effect you intend to measure, including "
             "how you will handle the events that complicate it — discontinuation, rescue "
             "medication, death. ICH E9(R1) made it explicit because trials had long reported "
             "effects without saying what question they answered. Defining it before the protocol "
             "is written prevents an analysis plan that cannot be defended afterwards."),
            ("Does following SPIRIT guarantee approval?",
             "No. SPIRIT is a reporting standard for completeness, not a design review. A protocol "
             "can be SPIRIT-complete and still be sent back for an unjustified sample size, "
             "eligibility criteria that will not recruit, or a consent process that a committee "
             "considers inadequate. Those are what the coaching chapters address."),
            ("When do I register the trial?",
             "Prospectively — before the first participant is enrolled. Most journals following "
             "ICMJE will not publish a trial registered retrospectively, and this is discovered "
             "far too late with dispiriting regularity. The registration chapter comes before "
             "submission for that reason."),
            ("Do I still need a statistician?",
             "Yes. This workbook makes you arrive at that conversation with a defined estimand, a "
             "stated endpoint hierarchy and a draft sample-size justification, which makes the "
             "conversation far shorter and more productive. It does not substitute for it."),
        ],
    },

    # -------------------------------------------------------------- healthcare
    "clinical-research-design-simplified": {
        "who": [
            "Nurses, physicians and allied-health professionals designing a first study",
            "Clinicians with a research idea and no formal methods training",
            "Trainees whose protocol has been sent back and who were not told why",
        ],
        "not_for": (
            "If you already have data and need to analyse it, this is the wrong end of the "
            "process. If your project is local improvement against an existing standard, it is "
            "probably audit rather than research — the clinical audit workbook is the better fit "
            "and takes a much shorter governance route."
        ),
        "inside": [
            "Turning a clinical observation into a researchable question with PICOT",
            "Testing that question against FINER before committing to it",
            "Matching a design to the question rather than to what you have seen before",
            "Sampling, and the difference between what is ideal and what is achievable in a clinic",
            "Choosing measures, and the validity and reliability an examiner will ask about",
            "Anticipating what an ethics committee will query, before submission",
            "Planning analysis before data collection, so the data can answer the question",
        ],
        "differs": (
            "Most clinical research texts are written for people whose job is research. This one "
            "is written for people whose job is clinical care and who have a research requirement "
            "attached — no prior methods background assumed, no statistics degree needed to follow "
            "it, and the worked examples come from practice rather than from a methods seminar."
        ),
        "faq": [
            ("Can I do this alongside a full clinical job?",
             "That is the assumption it is written on. The chapters are short and each ends with "
             "a decision recorded rather than an essay written, which is what makes the work "
             "survivable in the gaps between clinical commitments. Design work is front-loaded on "
             "purpose: the decisions that cost the most to reverse are the ones you make first."),
            ("My protocol was rejected. Will this tell me why?",
             "Probably. The most common reasons a first protocol is sent back are an unclear "
             "question, a design that cannot answer it, a sampling plan with no justification, and "
             "measures whose validity is asserted rather than evidenced. Each has a chapter, and "
             "the ethics chapter covers the queries committees raise most often."),
            ("Does it cover qualitative designs?",
             "Yes, as design choices rather than as an afterthought — when a qualitative or mixed "
             "design answers the question better, and what that commits you to. It does not teach "
             "qualitative analysis itself; the coding workbook does that."),
            ("Do I need statistics training to use this?",
             "No. It covers the design decisions that determine which analysis is appropriate, and "
             "makes you plan the analysis before collecting data. It does not teach you to run the "
             "tests, and it says plainly where a statistician should be involved."),
            ("How is this different from audit or service evaluation?",
             "Research sets out to produce generalisable new knowledge and needs ethics review. "
             "Audit measures local practice against an existing standard and normally does not. "
             "The distinction determines your governance route and can cost months if you get it "
             "wrong, which is why it is settled early."),
            ("What is FINER and why use it alongside PICOT?",
             "PICOT makes a question specific — population, intervention, comparison, outcome, "
             "time. FINER asks whether it is worth doing and can be done: feasible, interesting, "
             "novel, ethical, relevant. A question can be perfectly specific and still be "
             "unanswerable in your setting, and FINER is what catches that."),
        ],
    },

    "public-health-research-simplified": {
        "who": [
            "Public health students and MPH candidates",
            "Practitioners building evidence for programmes or policy",
            "Anyone working with population-level or secondary data",
        ],
        "not_for": (
            "This is population-level work. If your question is about individual clinical care or "
            "a single service, the clinical research design guide fits better. If you need a "
            "systematic review rather than primary data, that is a different book."
        ),
        "inside": [
            "Turning community and system problems into precise research questions",
            "Choosing among cross-sectional, cohort, trial, qualitative and mixed-methods designs",
            "Ethics and data governance appropriate to population data",
            "Equity built into the design rather than added in the discussion",
            "Working with messy secondary and administrative data",
            "Sampling frames for populations rather than clinic lists, and what each one excludes",
            "Measurement at population level: routine indicators, survey instruments, and their limits",
            "Analysis with runnable code in R and Python, not pseudocode",
            "Reporting aimed at programmes and policy audiences as well as journals",
            "Turning findings into a brief a commissioner will read, alongside the paper",
        ],
        "differs": (
            "Population-level research carries constraints a general methods text does not cover: "
            "equity as a design question rather than a limitation, secondary data you did not "
            "collect and cannot re-collect, and findings that must persuade commissioners and "
            "policymakers rather than only reviewers. This follows one workflow — problem, "
            "question, design, data, analysis, reporting — with checklists, decision trees and "
            "code you can actually run."
        ),
        "faq": [
            ("What if my data are secondary and messy?",
             "That is the normal case in population work, and it has its own chapter. Data you did "
             "not collect and cannot re-collect changes what you can claim, and the honest handling "
             "of missingness, linkage and definition changes over time is treated as part of the "
             "method rather than as a limitation to be confessed at the end."),
            ("How is this different from clinical research design?",
             "The unit of analysis, and the audience. Population-level questions bring sampling "
             "frames, ecological inference and equity into the design itself, and the findings "
             "usually have to persuade commissioners and policymakers as well as reviewers. If "
             "your question is about individual patient care, the clinical design guide fits better."),
            ("Is the code maintained?",
             "The code is written to be readable and adapted rather than run blind, using stable "
             "core libraries in R and Python instead of fast-moving packages. If you work in Stata "
             "or SPSS the workflow still holds; you would translate the steps rather than the "
             "syntax."),
            ("Do I need to know R or Python already?",
             "No. The code is provided and runnable, with enough explanation to adapt it. If you "
             "prefer another tool the workflow still holds — the code is an accelerator, not the "
             "method."),
            ("Is this suitable for a thesis?",
             "Yes, and it is written with that in mind: the workflow produces the artefacts a "
             "committee expects, in the order they expect them. Check your programme's specific "
             "requirements against the reporting chapter."),
            ("What does equity-centred actually mean here?",
             "That disaggregation, the choice of comparison groups, and who is represented in the "
             "data are treated as design decisions made at the start, rather than caveats added to "
             "the discussion once the analysis is done."),
        ],
    },

    "systematic-reviews-healthcare-simplified": {
        "who": [
            "DNP and doctoral candidates whose project requires a systematic review",
            "Clinicians contributing to guideline development",
            "Anyone who has been asked for a review and shown a finished Cochrane one as the model",
        ],
        "not_for": (
            "A narrative or scoping review answers a different question and needs a different "
            "method. If you are collecting primary data, this is the wrong book — though it is a "
            "reasonable place to start, since a proper review tells you whether the primary study "
            "is needed at all."
        ),
        "inside": [
            "A focused, answerable question, and a protocol registered before you start",
            "A reproducible search strategy across the databases your field expects",
            "Screening, with the decisions documented well enough to survive scrutiny",
            "Data extraction that does not have to be redone",
            "Risk-of-bias appraisal you can defend",
            "Synthesis — and an honest judgement about whether the data support pooling",
            "Meta-analysis where they do, including heterogeneity and its interpretation",
            "GRADE, and stating certainty rather than implying it",
            "A PRISMA-compliant manuscript ready to submit",
        ],
        "differs": (
            "The usual model available to a first-time reviewer is a finished fifty-page Cochrane "
            "review, which shows the destination and nothing of the route. This walks the sequence "
            "in order, at a level that assumes clinical training rather than research training, "
            "and is explicit about the decision most reviews get wrong — whether the studies are "
            "similar enough to pool at all."
        ),
        "faq": [
            ("What is the difference between this and a scoping review?",
             "A systematic review answers a focused question with a pre-specified method and, where "
             "appropriate, a pooled estimate. A scoping review maps what exists on a broader "
             "question and does not usually appraise or pool. Choosing the wrong one is expensive, "
             "so the first chapter makes you decide before you search."),
            ("How many databases do I need to search?",
             "Enough that a reader could believe you did not miss the obvious, which in health "
             "research usually means at least the major bibliographic databases for your field "
             "plus a trials register, and often grey literature. What matters more than the count "
             "is that the strategy is documented well enough to be re-run."),
            ("What does GRADE actually do?",
             "It separates the strength of a recommendation from the certainty of the evidence "
             "behind it, and forces you to state the second explicitly. Reviews that skip it tend "
             "to imply more confidence than their evidence supports, which is what a careful "
             "reader will challenge first."),
            ("How long does a systematic review take?",
             "Longer than almost anyone plans for. Screening and extraction dominate, and both "
             "scale with the size of your search rather than with the number of studies you "
             "finally include. A tightly framed question is the single biggest time saver, which "
             "is why the question chapter comes first."),
            ("Do I have to register the protocol?",
             "You should, and for many journals and programmes you must. Prospective registration "
             "on PROSPERO or an equivalent is what distinguishes a systematic review from a "
             "literature search written up afterwards, and it protects you against the accusation "
             "of having changed the question once you saw the results."),
            ("Do I need a meta-analysis?",
             "Only if the studies are similar enough in population, intervention and outcome to "
             "make a pooled estimate meaningful. Pooling heterogeneous studies produces a precise "
             "number that means nothing. A systematic review with a narrative synthesis and a "
             "clear explanation of why pooling was inappropriate is the stronger paper."),
            ("Can I do one on my own?",
             "Screening and extraction are normally done in duplicate, and most journals expect "
             "at least two reviewers for the screening stage. Plan for a second person even if "
             "the rest of the work is yours."),
        ],
    },
}

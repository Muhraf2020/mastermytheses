# -*- coding: utf-8 -*-
"""
tool_content.py - the authored content for the clinical tools.

Every word, worked example, FAQ and calculation here is written for this site.
gradsummit.com already carries thirty research-methods tools and
phdjourneysimplified.com carries ten; none of them is clinical, and nothing in
this file is copied from either. That is deliberate: three of the author's own
domains competing for one query helps none of them.

The tools answer questions a clinician asks in the week they are asked, and each
one ends at the book that covers the whole job rather than at an email form.

Each entry supplies:
    slug         URL and filename
    title        <title>, already carrying the brand
    description  meta description and og:description
    h1           the question a reader typed, in their words
    standfirst   one sentence under the h1
    book         slug of the book this tool belongs to, from local_books.py
    widget       the tool UI; must contain every id its script references
    script       the calculation, self-contained, no dependencies
    explainer    (heading, body html) - the method behind the numbers
    faq          [(question, answer)] - rendered as FAQPage structured data
    related      [(slug, label)] other tools worth a click
"""

# --------------------------------------------------------------------------
# shared javascript: statistics helpers every calculator needs.
# Inlined per page rather than served as a file, so a tool page has no
# dependency that can 404 and no extra request before it can compute.
# --------------------------------------------------------------------------
STATS_JS = """
  var Z = {0.90: 1.6448536, 0.95: 1.9599640, 0.99: 2.5758293};
  function num(id){ var v = document.getElementById(id).value.trim();
    if (v === '') return null; var n = Number(v); return isFinite(n) ? n : null; }
  function fmt(x, d){ if (x === null || !isFinite(x)) return '\\u2014';
    return x.toFixed(d === undefined ? 2 : d); }
  function pct(x, d){ if (x === null || !isFinite(x)) return '\\u2014';
    return (100 * x).toFixed(d === undefined ? 1 : d) + '%'; }
  // Wilson score interval: behaves at 0 and 100%, where the textbook
  // normal approximation produces impossible bounds.
  function wilson(k, n, z){
    if (!n) return [null, null];
    var p = k / n, d = 1 + z * z / n;
    var c = (p + z * z / (2 * n)) / d;
    var h = (z / d) * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n));
    return [Math.max(0, c - h), Math.min(1, c + h)];
  }
  function row(label, value, ci, note){
    return '<tr><th scope="row">' + label + '</th><td class="num">' + value +
      '</td><td class="num muted">' + (ci || '') + '</td><td class="muted">' +
      (note || '') + '</td></tr>';
  }
  function warn(msg){
    return '<p class="tool-warn" role="status">' + msg + '</p>';
  }
"""

TOOLS = [

# ==========================================================================
{
 "slug": "pico-question-builder",
 "title": "PICO Question Builder — turn a clinical problem into a searchable question",
 "description": "Build a PICO question from a clinical problem, then get the Boolean "
                "search string to paste straight into PubMed. Free, no sign-up.",
 "h1": "Turn your clinical problem into a PICO question",
 "standfirst": "Fill in the four parts and this writes the question your supervisor is "
               "asking for — and the PubMed search that goes with it.",
 "book": "evidence-based-practice-project",
 "widget": """
    <div class="tool-grid">
      <label for="p">Population <span class="hint">who the patients are</span>
        <input id="p" type="text" placeholder="adults admitted with community-acquired pneumonia"></label>
      <label for="i">Intervention <span class="hint">what you would do</span>
        <input id="i" type="text" placeholder="early mobilisation within 24 hours"></label>
      <label for="c">Comparison <span class="hint">the alternative; leave blank if none</span>
        <input id="c" type="text" placeholder="usual care"></label>
      <label for="o">Outcome <span class="hint">what you will measure</span>
        <input id="o" type="text" placeholder="length of stay"></label>
      <label for="t">Timeframe <span class="hint">optional</span>
        <input id="t" type="text" placeholder="within 30 days"></label>
      <label for="qtype">Question type
        <select id="qtype">
          <option value="therapy">Therapy or intervention</option>
          <option value="diagnosis">Diagnosis</option>
          <option value="prognosis">Prognosis</option>
          <option value="aetiology">Aetiology or harm</option>
          <option value="qualitative">Experience or meaning</option>
        </select></label>
    </div>
    <div class="actions">
      <button class="btn" id="go" type="button">Build my question</button>
      <button class="btn secondary" id="reset" type="button">Clear</button>
    </div>
    <div id="out" class="tool-out" hidden></div>
""",
 "script": """
  var DESIGN = {
    therapy:    ['randomised controlled trial', 'A randomised controlled trial answers this best. A well-conducted cohort study is the usual fallback.'],
    diagnosis:  ['cross-sectional study with a reference standard', 'You need consecutive patients who all receive both the new test and the reference standard.'],
    prognosis:  ['cohort study', 'Follow a defined group forward from a common starting point.'],
    aetiology:  ['cohort or case-control study', 'Randomising people to a harm is not ethical, so observational designs carry this question.'],
    qualitative:['qualitative study', 'Ask about experience and meaning, not effect size. Interviews or focus groups, analysed thematically.']
  };
  var FILTER = {
    therapy: '(randomized controlled trial[pt] OR clinical trial[pt])',
    diagnosis: '(sensitivity and specificity[mh] OR diagnosis[sh])',
    prognosis: '(cohort studies[mh] OR prognosis[mh])',
    aetiology: '(cohort studies[mh] OR case-control studies[mh])',
    qualitative: '(qualitative research[mh] OR interviews as topic[mh])'
  };
  function phrase(s){
    s = s.trim();
    if (!s) return '';
    return s.indexOf(' ') > -1 ? '"' + s + '"' : s;
  }
  function build(){
    var p = document.getElementById('p').value.trim(),
        i = document.getElementById('i').value.trim(),
        c = document.getElementById('c').value.trim(),
        o = document.getElementById('o').value.trim(),
        t = document.getElementById('t').value.trim(),
        k = document.getElementById('qtype').value;
    var out = document.getElementById('out');
    var missing = [];
    if (!p) missing.push('Population');
    if (!i) missing.push('Intervention');
    if (!o) missing.push('Outcome');
    if (missing.length){
      out.hidden = false;
      out.innerHTML = warn('Add ' + missing.join(', ') +
        ' \\u2014 a PICO question needs at least who, what, and what you will measure.');
      return;
    }
    var q = 'In ' + p + ', does ' + i +
            (c ? ', compared with ' + c : '') +
            ', affect ' + o + (t ? ' ' + t : '') + '?';
    var terms = [phrase(p), phrase(i)];
    if (c) terms.push(phrase(c));
    terms.push(phrase(o));
    var search = terms.join(' AND ') + ' AND ' + FILTER[k];
    var d = DESIGN[k];
    out.hidden = false;
    out.innerHTML =
      '<h3>Your question</h3><p class="tool-answer">' + q + '</p>' +
      '<h3>Design that answers it</h3><p><strong>' + d[0] + '</strong>. ' + d[1] + '</p>' +
      '<h3>PubMed search</h3><p class="tool-code">' + search + '</p>' +
      '<p class="muted">Paste that into PubMed. If it returns nothing, drop the ' +
      'Outcome term first \\u2014 outcomes are the least consistently indexed part of a record. ' +
      'If it returns thousands, add the Comparison back in.</p>';
  }
  document.getElementById('go').addEventListener('click', build);
  document.getElementById('reset').addEventListener('click', function(){
    ['p','i','c','o','t'].forEach(function(id){ document.getElementById(id).value = ''; });
    document.getElementById('out').hidden = true;
  });
""",
 "explainer": ("What PICO is actually for", """
    <p>PICO is not a formatting exercise. It exists because a vague question cannot be
    searched and cannot be answered. &ldquo;Does early mobilisation help?&rdquo; has no
    population, no comparison and no outcome, so there is no set of papers that either
    supports or refutes it. Every appraisal you attempt afterwards inherits that vagueness.</p>
    <p>The four parts do specific work. <strong>Population</strong> decides which studies
    are even eligible. <strong>Intervention</strong> and <strong>Comparison</strong> decide
    what the effect is measured against &mdash; and &ldquo;usual care&rdquo; is a real
    comparison that needs defining, because usual care differs between wards.
    <strong>Outcome</strong> decides what counts as success, and it must be something you
    can actually obtain from your records.</p>
    <p>The question type matters more than most people are told. It determines which study
    design can answer you, and therefore which appraisal checklist applies later. A therapy
    question appraised with a diagnostic checklist produces a confident, wrong answer.</p>
    <p>A practical warning about the search: databases index populations and interventions
    well and outcomes poorly. If your search returns nothing, the outcome term is usually
    the culprit, not the absence of evidence.</p>
"""),
 "faq": [
   ("Do I always need a comparison?",
    "No. Prevalence and experience questions often have none, and forcing one in distorts "
    "the question. But for any therapy question, leaving the comparison blank usually means "
    "you have not yet decided what you are comparing against — and 'usual care' still "
    "needs defining, because it varies by ward."),
   ("My search returns thousands of results. What now?",
    "Add the comparison term back, then restrict the population. Narrowing the outcome is "
    "the last thing to try, because outcome terms are inconsistently indexed and you will "
    "lose relevant papers before you lose irrelevant ones."),
   ("Is PICO the same as PICOT or PECO?",
    "They are the same skeleton. PICOT adds an explicit timeframe, useful when the outcome "
    "is time-dependent, such as 30-day readmission. PECO swaps Intervention for Exposure and "
    "is used for aetiology and harm questions, where nobody assigned the exposure."),
   ("Can I use this for a service evaluation or audit?",
    "Partly. An audit compares practice against an agreed standard rather than testing an "
    "intervention, so it needs a standard and a sample, not a comparison group. Build the "
    "population and outcome here, then move to the audit sample size tool."),
 ],
 "related": [("nnt-absolute-risk-calculator", "Turn a trial result into an NNT"),
             ("clinical-audit-sample-size", "Sizing an audit instead?")],
},

# ==========================================================================
{
 "slug": "diagnostic-test-calculator",
 "title": "Diagnostic Test Calculator — sensitivity, specificity, PPV, NPV and likelihood ratios",
 "description": "Enter a 2×2 table and get sensitivity, specificity, PPV, NPV, "
                "likelihood ratios and accuracy with confidence intervals. Free, no sign-up.",
 "h1": "Sensitivity, specificity, PPV and NPV from a 2×2 table",
 "standfirst": "Enter the four counts and this returns every diagnostic accuracy measure "
               "with confidence intervals — and shows why PPV changes when prevalence does.",
 "book": "clinical-research-design-simplified",
 "widget": """
    <p class="muted" style="margin-top:0">Enter counts from your study. Rows are the test
    result, columns are the reference standard.</p>
    <div class="tool-2x2">
      <table class="matrix">
        <thead><tr><th></th><th scope="col">Disease present</th><th scope="col">Disease absent</th></tr></thead>
        <tbody>
          <tr><th scope="row">Test positive</th>
              <td><input id="tp" type="number" min="0" step="1" value="80" aria-label="True positives"></td>
              <td><input id="fp" type="number" min="0" step="1" value="40" aria-label="False positives"></td></tr>
          <tr><th scope="row">Test negative</th>
              <td><input id="fn" type="number" min="0" step="1" value="20" aria-label="False negatives"></td>
              <td><input id="tn" type="number" min="0" step="1" value="860" aria-label="True negatives"></td></tr>
        </tbody>
      </table>
    </div>
    <div class="tool-grid">
      <label for="conf">Confidence level
        <select id="conf"><option value="0.95">95%</option><option value="0.90">90%</option>
        <option value="0.99">99%</option></select></label>
      <label for="prev">Recalculate PPV/NPV at a different prevalence <span class="hint">optional, %</span>
        <input id="prev" type="number" min="0" max="100" step="0.1" placeholder="e.g. 2"></label>
    </div>
    <div class="actions">
      <button class="btn" id="go" type="button">Calculate</button>
      <button class="btn secondary" id="reset" type="button">Reset</button>
    </div>
    <div id="out" class="tool-out" hidden></div>
""",
 "script": """
  function calc(){
    var tp = num('tp'), fp = num('fp'), fn = num('fn'), tn = num('tn');
    var z = Z[Number(document.getElementById('conf').value)];
    var out = document.getElementById('out');
    out.hidden = false;
    if (tp === null || fp === null || fn === null || tn === null ||
        tp < 0 || fp < 0 || fn < 0 || tn < 0){
      out.innerHTML = warn('All four cells need a number of zero or more.'); return;
    }
    var dis = tp + fn, well = fp + tn, n = dis + well;
    if (!dis || !well){
      out.innerHTML = warn('You need at least one patient with the disease and one without, ' +
        'or sensitivity and specificity are undefined.'); return;
    }
    var sens = tp / dis, spec = tn / well;
    var prev = dis / n;
    var ppv = (tp + fp) ? tp / (tp + fp) : null;
    var npv = (tn + fn) ? tn / (tn + fn) : null;
    var acc = (tp + tn) / n;
    var ci = function(k, m){ var w = wilson(k, m, z); return pct(w[0]) + ' to ' + pct(w[1]); };

    var lrp = (spec < 1) ? sens / (1 - spec) : null;
    var lrn = (spec > 0) ? (1 - sens) / spec : null;
    var lrCI = function(lr, seLog){
      if (lr === null || !isFinite(lr) || lr <= 0) return '';
      return fmt(lr * Math.exp(-z * seLog)) + ' to ' + fmt(lr * Math.exp(z * seLog));
    };
    var sePos = Math.sqrt((1 - sens) / (sens * dis) + spec / ((1 - spec) * well));
    var seNeg = Math.sqrt(sens / ((1 - sens) * dis) + (1 - spec) / (spec * well));

    var html = '<h3>Accuracy of the test itself</h3>' +
      '<table class="results"><thead><tr><th>Measure</th><th class="num">Value</th>' +
      '<th class="num">CI</th><th>Reading</th></tr></thead><tbody>' +
      row('Sensitivity', pct(sens), ci(tp, dis), 'of ' + dis + ' with the disease, ' + tp + ' tested positive') +
      row('Specificity', pct(spec), ci(tn, well), 'of ' + well + ' without it, ' + tn + ' tested negative') +
      row('Likelihood ratio +', fmt(lrp), lrCI(lrp, sePos), lrp > 10 ? 'strong rule-in' : (lrp > 5 ? 'moderate rule-in' : 'weak')) +
      row('Likelihood ratio \\u2212', fmt(lrn, 3), lrCI(lrn, seNeg), lrn < 0.1 ? 'strong rule-out' : (lrn < 0.2 ? 'moderate rule-out' : 'weak')) +
      row('Accuracy', pct(acc), ci(tp + tn, n), 'depends on prevalence; rarely the useful number') +
      '</tbody></table>' +
      '<h3>Performance in this sample</h3>' +
      '<table class="results"><tbody>' +
      row('Prevalence', pct(prev), ci(dis, n), dis + ' of ' + n + ' patients') +
      row('PPV', pct(ppv), (tp + fp) ? ci(tp, tp + fp) : '', 'chance a positive result is correct here') +
      row('NPV', pct(npv), (tn + fn) ? ci(tn, tn + fn) : '', 'chance a negative result is correct here') +
      '</tbody></table>';

    var alt = num('prev');
    if (alt !== null && alt > 0 && alt < 100){
      var q = alt / 100;
      var ppv2 = (sens * q) / (sens * q + (1 - spec) * (1 - q));
      var npv2 = (spec * (1 - q)) / (spec * (1 - q) + (1 - sens) * q);
      html += '<h3>The same test at ' + alt + '% prevalence</h3><table class="results"><tbody>' +
        row('PPV', pct(ppv2), '', 'was ' + pct(ppv) + ' at ' + pct(prev)) +
        row('NPV', pct(npv2), '', 'was ' + pct(npv) + ' at ' + pct(prev)) +
        '</tbody></table>' +
        '<p class="muted">Sensitivity and specificity did not change \\u2014 they are properties ' +
        'of the test. PPV and NPV did, because they depend on how common the disease is in ' +
        'the people being tested. This is the single most common misreading of a validation study.</p>';
    }
    out.innerHTML = html;
  }
  document.getElementById('go').addEventListener('click', calc);
  document.getElementById('reset').addEventListener('click', function(){
    document.getElementById('tp').value = 80; document.getElementById('fp').value = 40;
    document.getElementById('fn').value = 20; document.getElementById('tn').value = 860;
    document.getElementById('prev').value = '';
    document.getElementById('out').hidden = true;
  });
  calc();
""",
 "explainer": ("Why PPV is not a property of the test", """
    <p>Sensitivity and specificity describe the test. Move the same assay to another
    hospital and they stay roughly the same. Predictive values describe the test
    <em>in a particular population</em>, and they move sharply with prevalence.</p>
    <p>Work the default numbers. In that sample, prevalence is 10%, and a positive result
    is right two thirds of the time. Put the identical test into a screening programme
    where prevalence is 2%, and the positive predictive value collapses — most positives
    become false positives, because there are so many more well people to draw them from.
    Nothing about the test changed. Only the population did.</p>
    <p>This is why likelihood ratios are worth learning. They combine sensitivity and
    specificity into one number per result, and they can be applied to whatever pre-test
    probability your patient actually has. As a rough guide, a positive likelihood ratio
    above 10 meaningfully rules a diagnosis in, and a negative likelihood ratio below 0.1
    meaningfully rules it out. Between 0.5 and 2, the test has barely changed what you
    believed before you ordered it.</p>
    <p>Accuracy — the proportion of all results that were correct — is the number
    most often quoted and least often useful. In a rare disease, a test that calls everyone
    negative achieves high accuracy and finds nobody.</p>
"""),
 "faq": [
   ("Which confidence interval does this use?",
    "The Wilson score interval for proportions, and the log method for likelihood ratios. "
    "Wilson is used deliberately: the normal approximation taught in most courses produces "
    "impossible bounds below 0 or above 100% when a proportion is near either extreme, which "
    "is exactly where diagnostic studies often sit."),
   ("My specificity is 100% and the likelihood ratio shows a dash. Why?",
    "A positive likelihood ratio is sensitivity divided by the false positive rate. If "
    "specificity is exactly 100%, that denominator is zero and the ratio is infinite rather "
    "than undefined in a useful sense. It usually means your sample of well patients was too "
    "small to observe a false positive, not that the test never produces one."),
   ("Can I use this for a screening programme?",
    "Yes, and you should use the prevalence box when you do. A test validated in a specialist "
    "clinic will look far worse in a screening population, and modelling that before you "
    "roll out is the whole point."),
   ("What sample size do I need for a diagnostic accuracy study?",
    "It is driven by the number of patients with the disease, not the total. Precision on "
    "sensitivity depends on the diseased column alone, so a large study with few cases still "
    "gives a wide interval for sensitivity."),
 ],
 "related": [("nnt-absolute-risk-calculator", "Absolute risk and NNT"),
             ("pico-question-builder", "Frame a diagnostic question")],
},

# ==========================================================================
{
 "slug": "nnt-absolute-risk-calculator",
 "title": "NNT and Absolute Risk Calculator — ARR, RRR, relative risk and odds ratio",
 "description": "Turn trial event counts into absolute risk reduction, relative risk "
                "reduction, NNT and NNH with confidence intervals. Free, no sign-up.",
 "h1": "What is the NNT for this trial?",
 "standfirst": "Enter the events in each arm and this returns absolute and relative risk "
               "reduction, the number needed to treat, and why the two look so different.",
 "book": "evidence-based-practice-project",
 "widget": """
    <div class="tool-grid">
      <label for="te">Treatment group: events <input id="te" type="number" min="0" step="1" value="15"></label>
      <label for="tn2">Treatment group: total <input id="tn2" type="number" min="1" step="1" value="500"></label>
      <label for="ce">Control group: events <input id="ce" type="number" min="0" step="1" value="30"></label>
      <label for="cn">Control group: total <input id="cn" type="number" min="1" step="1" value="500"></label>
      <label for="conf">Confidence level
        <select id="conf"><option value="0.95">95%</option><option value="0.90">90%</option>
        <option value="0.99">99%</option></select></label>
      <label for="dir">The event is <select id="dir">
        <option value="bad">something bad (death, readmission)</option>
        <option value="good">something good (recovery, discharge)</option></select></label>
    </div>
    <div class="actions">
      <button class="btn" id="go" type="button">Calculate</button>
      <button class="btn secondary" id="reset" type="button">Reset</button>
    </div>
    <div id="out" class="tool-out" hidden></div>
""",
 "script": """
  function calc(){
    var a = num('te'), n1 = num('tn2'), c = num('ce'), n2 = num('cn');
    var z = Z[Number(document.getElementById('conf').value)];
    var bad = document.getElementById('dir').value === 'bad';
    var out = document.getElementById('out'); out.hidden = false;
    if (a === null || c === null || !n1 || !n2){
      out.innerHTML = warn('Fill in events and totals for both groups.'); return; }
    if (a > n1 || c > n2){
      out.innerHTML = warn('A group cannot have more events than participants.'); return; }

    var eer = a / n1, cer = c / n2;
    var arr = cer - eer;                       // positive = treatment had fewer events
    var rr  = cer ? eer / cer : null;
    var rrr = cer ? arr / cer : null;
    var seARR = Math.sqrt(eer * (1 - eer) / n1 + cer * (1 - cer) / n2);
    var lo = arr - z * seARR, hi = arr + z * seARR;

    var b = n1 - a, d = n2 - c;
    var or = (b && c) ? (a * d) / (b * c) : null;
    var seLogOR = (a && b && c && d) ? Math.sqrt(1/a + 1/b + 1/c + 1/d) : null;
    var seLogRR = (a && c) ? Math.sqrt(1/a - 1/n1 + 1/c - 1/n2) : null;

    var helps = bad ? arr > 0 : arr < 0;
    var mag = Math.abs(arr);
    var nnt = mag > 0 ? 1 / mag : null;
    var label = helps ? 'NNT (number needed to treat)' : 'NNH (number needed to harm)';

    var nntCI = '';
    if (lo < 0 && hi > 0){
      nntCI = 'interval crosses no effect';
    } else if (mag > 0){
      var x = 1 / Math.abs(hi), y = 1 / Math.abs(lo);
      nntCI = fmt(Math.min(x, y), 0) + ' to ' + fmt(Math.max(x, y), 0);
    }
    var ciTxt = function(v, se){ return (v && se) ?
      fmt(v * Math.exp(-z * se)) + ' to ' + fmt(v * Math.exp(z * se)) : ''; };

    out.innerHTML =
      '<h3>Risk in each arm</h3><table class="results"><tbody>' +
      row('Control event rate', pct(cer), '', c + ' of ' + n2) +
      row('Treatment event rate', pct(eer), '', a + ' of ' + n1) +
      '</tbody></table>' +
      '<h3>The effect</h3><table class="results"><thead><tr><th>Measure</th>' +
      '<th class="num">Value</th><th class="num">CI</th><th>Reading</th></tr></thead><tbody>' +
      row('Absolute risk difference', pct(Math.abs(arr)),
          pct(Math.min(Math.abs(lo), Math.abs(hi))) + ' to ' + pct(Math.max(Math.abs(lo), Math.abs(hi))),
          helps ? 'fewer events on treatment' : 'more events on treatment') +
      row('Relative risk reduction', rrr === null ? '\\u2014' : pct(Math.abs(rrr)), '',
          'the impressive-looking number') +
      row('Relative risk', fmt(rr), ciTxt(rr, seLogRR), rr < 1 ? 'treatment lowers risk' : 'treatment raises risk') +
      row('Odds ratio', fmt(or), ciTxt(or, seLogOR), 'overstates the effect when events are common') +
      row(label, nnt === null ? '\\u2014' : fmt(Math.ceil(nnt), 0), nntCI,
          'patients treated for one extra ' + (helps ? 'benefit' : 'harm')) +
      '</tbody></table>' +
      (lo < 0 && hi > 0 ? warn('The confidence interval for the absolute difference includes ' +
        'zero, so this trial is compatible with no effect. An NNT quoted from it is not ' +
        'meaningfully bounded.') : '') +
      '<p class="muted">Same data, two stories: a relative reduction of ' +
      (rrr === null ? '\\u2014' : pct(Math.abs(rrr))) + ' sounds far larger than an absolute ' +
      'reduction of ' + pct(Math.abs(arr)) + '. Both are correct. Only the absolute figure ' +
      'tells your patient what they can expect.</p>';
  }
  document.getElementById('go').addEventListener('click', calc);
  document.getElementById('reset').addEventListener('click', function(){
    document.getElementById('te').value = 15; document.getElementById('tn2').value = 500;
    document.getElementById('ce').value = 30; document.getElementById('cn').value = 500;
    document.getElementById('out').hidden = true;
  });
  calc();
""",
 "explainer": ("Why relative risk reduction flatters every treatment", """
    <p>Run the default numbers. Events fall from 6% to 3%. The relative risk reduction is
    50% &mdash; the figure that reaches the press release. The absolute risk reduction is
    3 percentage points, which means about 33 patients must be treated for one to avoid the
    event. Both numbers describe the same trial honestly. Only one of them tells a patient
    what to expect.</p>
    <p>The gap widens as the event becomes rarer. A drop from 0.2% to 0.1% is also a 50%
    relative reduction, but the NNT is 1,000. This is why relative figures are the ones that
    get quoted, and why any appraisal checklist worth using asks for the absolute difference.</p>
    <p>The number needed to treat is just the reciprocal of the absolute risk difference,
    rounded up, because you cannot treat a fraction of a person. It carries the same
    uncertainty as that difference, so it needs a confidence interval &mdash; and when the
    interval for the absolute difference crosses zero, the NNT interval becomes unbounded
    rather than merely wide. That is a real result, not a computational failure: the trial
    is compatible with the treatment helping, doing nothing, or harming.</p>
    <p>Odds ratios appear because logistic regression produces them, not because they are
    easier to understand. When events are rare the odds ratio is close to the relative risk.
    When events are common it exaggerates, sometimes badly. If a paper reports only an odds
    ratio for a common outcome, be careful before you translate it into an NNT.</p>
"""),
 "faq": [
   ("Should I use the odds ratio or the relative risk?",
    "Report the relative risk if you have the raw counts, which you do here. The odds ratio "
    "is worth having when you are comparing with a paper that reported one, or when the study "
    "was case-control, where relative risk cannot be calculated directly."),
   ("Why does my NNT have no upper limit?",
    "Because the confidence interval for the absolute risk difference includes zero. As the "
    "difference approaches zero, the number you would need to treat approaches infinity. The "
    "honest reading is that this trial has not established an effect."),
   ("What is a good NNT?",
    "There is no threshold. It depends entirely on the outcome and the cost of treating. An "
    "NNT of 100 is excellent for preventing a stroke with a cheap, safe tablet, and poor for "
    "preventing a mild rash with an expensive infusion."),
   ("Can I use this on a meta-analysis?",
    "Only if you have the pooled event counts. If you have a pooled relative risk and a "
    "baseline risk instead, the absolute difference has to be derived from those, and the "
    "baseline risk you choose should reflect your own population, not the trials' average."),
 ],
 "related": [("pico-question-builder", "Build the question first"),
             ("diagnostic-test-calculator", "Sensitivity, specificity and PPV")],
},

# ==========================================================================
{
 "slug": "clinical-audit-sample-size",
 "title": "Clinical Audit Sample Size Calculator — how many notes do you need?",
 "description": "Work out how many records to review for a clinical audit, with the "
                "finite population correction most calculators leave out. Free, no sign-up.",
 "h1": "How many notes do I need to review?",
 "standfirst": "Audit sample size is not a power calculation. This works out how many "
               "records give you a compliance figure precise enough to act on.",
 "book": "clinical-audit-quality-improvement",
 "widget": """
    <div class="tool-grid">
      <label for="N">Eligible cases in the period <span class="hint">your whole population</span>
        <input id="N" type="number" min="1" step="1" value="400"></label>
      <label for="p">Expected compliance <span class="hint">%, best guess; use 50 if unsure</span>
        <input id="p" type="number" min="1" max="99" step="1" value="70"></label>
      <label for="e">Acceptable margin of error <span class="hint">± percentage points</span>
        <input id="e" type="number" min="1" max="25" step="1" value="10"></label>
      <label for="conf">Confidence level
        <select id="conf"><option value="0.95">95%</option><option value="0.90">90%</option>
        <option value="0.99">99%</option></select></label>
    </div>
    <div class="actions">
      <button class="btn" id="go" type="button">Calculate</button>
      <button class="btn secondary" id="reset" type="button">Reset</button>
    </div>
    <div id="out" class="tool-out" hidden></div>
""",
 "script": """
  function calc(){
    var N = num('N'), p = num('p'), e = num('e');
    var z = Z[Number(document.getElementById('conf').value)];
    var out = document.getElementById('out'); out.hidden = false;
    if (!N || p === null || e === null || p <= 0 || p >= 100 || e <= 0){
      out.innerHTML = warn('Enter the number of eligible cases, an expected compliance ' +
        'between 1 and 99%, and a margin of error above zero.'); return; }
    var q = p / 100, m = e / 100;
    var n0 = z * z * q * (1 - q) / (m * m);
    var n  = n0 / (1 + (n0 - 1) / N);
    var need = Math.min(N, Math.ceil(n));
    var frac = need / N;

    var note = '';
    if (need >= N){
      note = warn('The precision you asked for needs your entire population. Review all ' +
        N + ' cases, or accept a wider margin of error.');
    } else if (frac > 0.5){
      note = warn('This is over half your eligible cases. Reviewing all ' + N +
        ' may cost little more and removes sampling error entirely.');
    }
    // what a smaller, commonly used sample would actually buy you
    var rows = '';
    [20, 30, 50, 100].forEach(function(s){
      if (s >= N) return;
      var se = Math.sqrt(q * (1 - q) / s) * Math.sqrt((N - s) / (N - 1));
      rows += row(s + ' records', '\\u00b1' + (100 * z * se).toFixed(1) + ' points', '',
        s < need ? 'less precise than you asked for' : 'meets your target');
    });

    out.innerHTML =
      '<h3>Review ' + need + ' records</h3>' +
      '<p class="tool-answer">' + need + ' of ' + N + ' eligible cases (' +
      (100 * frac).toFixed(0) + '%)</p>' +
      '<p>That gives you a compliance estimate of roughly ' + p + '% \\u00b1 ' + e +
      ' percentage points at ' + (100 * Number(document.getElementById('conf').value)) +
      '% confidence.</p>' + note +
      '<h3>What other sample sizes would buy you</h3>' +
      '<table class="results"><thead><tr><th>Sample</th><th class="num">Margin of error</th>' +
      '<th class="num"></th><th></th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<p class="muted">Margins assume simple random sampling from your ' + N +
      ' cases, with the finite population correction applied. Taking the first ' + need +
      ' notes on the pile is not random and will not deliver this precision.</p>';
  }
  document.getElementById('go').addEventListener('click', calc);
  document.getElementById('reset').addEventListener('click', function(){
    document.getElementById('N').value = 400; document.getElementById('p').value = 70;
    document.getElementById('e').value = 10; document.getElementById('out').hidden = true;
  });
  calc();
""",
 "explainer": ("Audit sample size is a precision problem, not a power problem", """
    <p>Most sample size calculators answer a different question from the one an audit asks.
    They size a study to detect a difference between two groups. An audit has no second
    group: it compares one population against an agreed standard, and what you need is a
    compliance figure precise enough that people will act on it.</p>
    <p>So the inputs are different. You need the number of eligible cases in the period,
    a guess at compliance, and the margin of error you can live with. If you have no idea
    what compliance will be, enter 50% &mdash; that is the value that requires the largest
    sample, so it is the safe assumption.</p>
    <p>The finite population correction matters here and is missing from most online
    calculators. Those assume you are sampling from an effectively infinite population. An
    audit samples from a known, often small, list &mdash; every caesarean section last
    quarter, every discharge summary in March. When your sample is a large fraction of that
    list, the correction reduces the number you need substantially, sometimes by half.</p>
    <p>One caution that no formula can fix: this arithmetic assumes a random sample. Pulling
    the most recent fifty notes, or the ones that happen to be on the ward, produces a number
    with no defensible margin of error at all. Number your eligible cases and select with a
    random sequence.</p>
"""),
 "faq": [
   ("Why does 50% expected compliance need the biggest sample?",
    "Because the variance of a proportion is largest at 50% and shrinks as you move towards "
    "0 or 100%. If you genuinely do not know what to expect, 50% is the conservative entry: "
    "it will never leave you under-sampled."),
   ("Is there a minimum sample for an audit?",
    "No universal one, though many departments default to 20 or 50 out of habit. The table "
    "above shows what those conventional numbers actually buy you in precision, which is "
    "usually less than people assume."),
   ("My whole population is only 30 cases. What then?",
    "Review all of them. Below roughly 50 eligible cases, sampling saves little effort and "
    "costs you the ability to state a margin of error at all."),
   ("Does this apply to the re-audit as well?",
    "Yes, and use the same margin of error both times. If the first cycle had ±10 points "
    "and the second ±20, an apparent improvement may be nothing more than the wider "
    "interval on the second sample."),
 ],
 "related": [("run-chart-builder", "Plot the data once you have it"),
             ("pico-question-builder", "If it is a question, not a standard")],
},

# ==========================================================================
{
 "slug": "run-chart-builder",
 "title": "Run Chart Builder — plot QI data and test it against the runs rules",
 "description": "Paste your measurements and get a run chart with the median, plus the "
                "shift, trend and runs tests that separate real change from noise. Free, no sign-up.",
 "h1": "Is my quality improvement project actually working?",
 "standfirst": "Paste your numbers in order. This draws the run chart and applies the four "
               "rules that distinguish a real change from ordinary variation.",
 "book": "clinical-audit-quality-improvement",
 "widget": """
    <div class="tool-grid wide">
      <label for="data">Your measurements, in time order
        <span class="hint">one per line, or separated by commas</span>
        <textarea id="data" rows="6">62, 58, 65, 61, 59, 64, 60, 72, 75, 78, 74, 80, 79, 83</textarea></label>
      <label for="lbl">What you measured <span class="hint">optional, used as the axis label</span>
        <input id="lbl" type="text" placeholder="% compliance with the checklist"></label>
    </div>
    <div class="actions">
      <button class="btn" id="go" type="button">Draw the chart</button>
      <button class="btn secondary" id="reset" type="button">Reset</button>
    </div>
    <div id="out" class="tool-out" hidden></div>
""",
 "script": """
  function parseData(s){
    return s.split(/[\\s,;]+/).map(function(v){ return v.trim(); })
            .filter(function(v){ return v !== ''; })
            .map(Number).filter(function(v){ return isFinite(v); });
  }
  function median(a){
    var b = a.slice().sort(function(x, y){ return x - y; }), m = b.length >> 1;
    return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2;
  }
  function chart(v, med, label){
    var W = 720, H = 300, PL = 48, PR = 16, PT = 16, PB = 34;
    var lo = Math.min.apply(null, v), hi = Math.max.apply(null, v);
    if (lo === hi){ lo -= 1; hi += 1; }
    var pad = (hi - lo) * 0.12; lo -= pad; hi += pad;
    var x = function(i){ return PL + i * (W - PL - PR) / Math.max(1, v.length - 1); };
    var y = function(d){ return PT + (hi - d) * (H - PT - PB) / (hi - lo); };
    var pts = v.map(function(d, i){ return x(i) + ',' + y(d); }).join(' ');
    var dots = v.map(function(d, i){
      var above = d > med, below = d < med;
      var fill = above ? '#0ea5e9' : (below ? '#94a3b8' : '#f59e0b');
      return '<circle cx="' + x(i) + '" cy="' + y(d) + '" r="4" fill="' + fill + '"><title>Point ' +
             (i + 1) + ': ' + d + '</title></circle>';
    }).join('');
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" class="runchart" role="img" aria-label="Run chart of ' +
      v.length + ' measurements with a median of ' + med + '">' +
      '<line x1="' + PL + '" y1="' + y(med) + '" x2="' + (W - PR) + '" y2="' + y(med) +
        '" stroke="#ef4444" stroke-dasharray="6 4" stroke-width="2"/>' +
      '<text x="' + (W - PR) + '" y="' + (y(med) - 6) + '" text-anchor="end" font-size="12" fill="#ef4444">median ' + med + '</text>' +
      '<polyline points="' + pts + '" fill="none" stroke="#0f172a" stroke-width="2"/>' + dots +
      '<line x1="' + PL + '" y1="' + (H - PB) + '" x2="' + (W - PR) + '" y2="' + (H - PB) + '" stroke="#cbd5e1"/>' +
      '<line x1="' + PL + '" y1="' + PT + '" x2="' + PL + '" y2="' + (H - PB) + '" stroke="#cbd5e1"/>' +
      '<text x="' + PL + '" y="' + (H - 10) + '" font-size="12" fill="#64748b">point 1</text>' +
      '<text x="' + (W - PR) + '" y="' + (H - 10) + '" text-anchor="end" font-size="12" fill="#64748b">point ' + v.length + '</text>' +
      '<text x="6" y="' + (PT + 10) + '" font-size="12" fill="#64748b">' + (label || 'value') + '</text>' +
      '</svg>';
  }
  function analyse(v, med){
    var useful = v.filter(function(d){ return d !== med; });
    var n = useful.length;
    var signs = useful.map(function(d){ return d > med ? 1 : -1; });
    var runs = 1, longest = 1, cur = 1;
    for (var i = 1; i < signs.length; i++){
      if (signs[i] !== signs[i - 1]){ runs++; cur = 1; }
      else { cur++; if (cur > longest) longest = cur; }
    }
    var nAbove = signs.filter(function(s){ return s > 0; }).length;
    var nBelow = n - nAbove;
    // trend: consecutive strictly increasing or decreasing points, ties broken
    var up = 1, down = 1, bestUp = 1, bestDown = 1;
    for (var j = 1; j < v.length; j++){
      if (v[j] > v[j - 1]){ up++; down = 1; } else if (v[j] < v[j - 1]){ down++; up = 1; }
      else { up = 1; down = 1; }
      if (up > bestUp) bestUp = up;
      if (down > bestDown) bestDown = down;
    }
    var trend = Math.max(bestUp, bestDown);
    var mu = null, sd = null, loLim = null, hiLim = null;
    if (nAbove > 0 && nBelow > 0 && n > 1){
      mu = 2 * nAbove * nBelow / n + 1;
      sd = Math.sqrt(2 * nAbove * nBelow * (2 * nAbove * nBelow - n) / (n * n * (n - 1)));
      loLim = mu - 1.96 * sd; hiLim = mu + 1.96 * sd;
    }
    return {n: n, runs: runs, longest: longest, trend: trend,
            lo: loLim, hi: hiLim, nAbove: nAbove, nBelow: nBelow};
  }
  function go(){
    var v = parseData(document.getElementById('data').value);
    var label = document.getElementById('lbl').value.trim();
    var out = document.getElementById('out'); out.hidden = false;
    var notice = '';
    if (v.length < 10){
      notice = warn('You have ' + v.length + ' point' + (v.length === 1 ? '' : 's') +
        '. The runs rules need at least 10 to mean anything, and 15 to 20 is the usual advice.' +
        (v.length ? ' The chart below is drawn, but treat the tests as indicative only.' : ''));
      if (!v.length){ out.innerHTML = notice; return; }
    }
    var med = median(v), a = analyse(v, med);
    var signals = [];
    if (a.longest >= 6) signals.push(['Shift', 'Yes \\u2014 ' + a.longest +
      ' consecutive points on one side of the median', true]);
    else signals.push(['Shift', 'No \\u2014 longest run is ' + a.longest + ' (needs 6)', false]);
    if (a.trend >= 5) signals.push(['Trend', 'Yes \\u2014 ' + a.trend +
      ' consecutive points all moving one way', true]);
    else signals.push(['Trend', 'No \\u2014 longest is ' + a.trend + ' (needs 5)', false]);
    if (a.lo !== null){
      var few = a.runs < a.lo, many = a.runs > a.hi;
      signals.push(['Number of runs', a.runs + ' observed, ' + a.lo.toFixed(1) + '\\u2013' +
        a.hi.toFixed(1) + ' expected by chance' + (few ? ' \\u2014 too few' : (many ? ' \\u2014 too many' : ' \\u2014 within range')),
        few || many]);
    }
    var any = signals.some(function(s){ return s[2]; });
    var rows = signals.map(function(s){
      return '<tr><th scope="row">' + s[0] + '</th><td>' + s[1] + '</td><td>' +
        (s[2] ? '<span class="flag">signal</span>' : '<span class="muted">no signal</span>') + '</td></tr>';
    }).join('');

    out.innerHTML = notice + chart(v, med, label) +
      '<h3>The runs rules</h3><table class="results"><tbody>' + rows + '</tbody></table>' +
      '<p class="' + (any ? 'tool-answer' : 'muted') + '">' + (any
        ? 'At least one rule is broken, which is evidence of non-random change \\u2014 the '
          + 'thing you were hoping to see if you made a deliberate improvement.'
        : 'No rule is broken. Everything here is consistent with ordinary variation, so '
          + 'there is no evidence yet that anything changed.') + '</p>' +
      '<p class="muted">' + a.n + ' of ' + v.length + ' points were used for the runs tests; ' +
      'points sitting exactly on the median are excluded by convention.</p>';
  }
  document.getElementById('go').addEventListener('click', go);
  document.getElementById('reset').addEventListener('click', function(){
    document.getElementById('data').value = '62, 58, 65, 61, 59, 64, 60, 72, 75, 78, 74, 80, 79, 83';
    document.getElementById('lbl').value = '';
    document.getElementById('out').hidden = true;
  });
  go();
""",
 "explainer": ("Before and after is not evidence", """
    <p>The most common quality improvement error is comparing a mean before an intervention
    with a mean after it. Both numbers vary week to week on their own. Comparing two points
    from a wobbling line tells you almost nothing, and it will show an improvement roughly
    half the time even when nothing was done.</p>
    <p>A run chart fixes this by plotting every measurement in time order against the median
    of the whole series, then asking whether the pattern is one that random variation could
    plausibly produce. Four rules do that work. A <strong>shift</strong> is six or more
    consecutive points on the same side of the median. A <strong>trend</strong> is five or
    more consecutive points all rising or all falling. <strong>Too few or too many
    runs</strong> means the line crosses the median less or more often than chance would
    predict. And an <strong>astronomical point</strong> is one obviously outside the pattern
    &mdash; a judgement call, which is why it is not automated here.</p>
    <p>Points that land exactly on the median are excluded from the counting. They cannot be
    on either side, and leaving them in inflates the run lengths.</p>
    <p>You need enough data. Below ten points the rules have very little power, and with
    fewer than that you will neither detect a real improvement nor be reassured by a null
    result. Fifteen to twenty points, collected at whatever interval is natural for your
    process, is the usual advice.</p>
"""),
 "faq": [
   ("Is a run chart the same as a control chart?",
    "No. A run chart uses the median and the runs rules and needs no assumption about the "
    "distribution. A control chart adds calculated limits based on the variation in the data "
    "and detects more kinds of signal, but it needs more points and more care to construct. "
    "Start with a run chart."),
   ("Should the median be recalculated after the change?",
    "For detecting whether a change happened, use the median of the baseline data and extend "
    "it forward. Recalculating across the whole series, as this tool does by default, is the "
    "right choice when you are simply looking at a process over time and have not yet "
    "intervened at a known point."),
   ("How often should I measure?",
    "Often enough to get ten to twenty points in the life of the project, and at an interval "
    "that matches how the process actually varies. Weekly is common for ward-level work. "
    "Monthly sampling often means the project ends before the chart can say anything."),
   ("A rule is broken. Does that prove my intervention worked?",
    "It shows the variation is unlikely to be random. It does not establish that your "
    "intervention caused it, since something else may have changed at the same time. That is "
    "why the annotation on a QI chart, recording what was done and when, matters as much as "
    "the points."),
 ],
 "related": [("clinical-audit-sample-size", "How many records to review"),
             ("pico-question-builder", "Frame the question first")],
},
]

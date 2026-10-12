# Theme question rules (how we count what customers say, for any brand)

Why this exists: Stage 2 and 3b turn thousands of reviews and comments into counts ("n of N critical reviews say X"). A model counts exactly what the question asks. A fuzzy question gives a fuzzy count, and a fuzzy count can send a whole campaign to the wrong angle. These rules make every question mean one thing, the same way for every brand, every model and every run.

Evidence: C:\cca\jev\ and vault note `Resources/Luna vs Jev - Head to Head Tests.md` (200 labelled Habbits reviews, two models, written 2026-10-07).

## The rules (apply to every theme question for every brand)
1. **Explicit statements only.** Count what the reviewer says, not what we infer. "Would recommend" needs "I recommend it / buy it / try it", not "love it". "Would not recommend" needs "don't buy / never recommend". "Misleading" needs a reference to the ads, claims or promises, not just "it did not work". Models over-flag implied versions badly (would_recommend: 23 flags for 11 true; misleading: a third of flags wrong).
2. **A negated mention is not a mention.** "No sensitivity at all", "no freshness" do not count as sensitivity or freshness. Write the question as "says the product caused / gave them X. Answer no if the reviewer says it did not." Questions worded "does the reviewer mention X" fire on denials.
3. **Name the thing.** "Compares with a named brand or a specific product" (not "regular toothpaste", not their usual paste). "Price, value or quantity named" (a bare "waste of money" in a not-working review is an effectiveness complaint, not a price objection, and counting it pushes us toward discounts when the real problem is trust).
4. **One question, one thing.** Fake product (counterfeit, not original) and misleading claims (ads not true) are different problems with different fixes: two questions. "Did not work" is a third.
5. **Loose to count, strict to quote.** Keep two questions for a theme when the use differs: the loose one finds nearly everyone (counting shares), the strict one returns only clear cases (pulling ad quotes, so every line is safe to use). Example: good_whitening_result (loose) and good_whitening_quote_grade (strict, precision 1.00 but only about half the true cases).
6. **Put the definition in the question text itself**, including an "Answer no if ..." sentence. Humans labelling the audit and the models then read the identical words.
7. **Say what you could not tell.** A refusal (Luna) or a middle-band probability (0.25 to 0.75) means "unsure": send to a second reader, never count silently. Report every share with its interval (Wilson 95%), and never report a share for a theme with fewer than 8 audit positives.

## The audit (every brand run, about 10 minutes of effort, about 15 cents)
Draw 100 random reviews from the run that no one has looked at. Three blind labellers (fresh Claude agent, gpt-5-mini, Claude main) answer the same question text. Key = majority of 3. A theme is CLEARED for counting when, on the audit, it has at least 5 key positives, precision at least 0.75 and share error within 5 points of reviews. Uncleared themes are counted by hand or by the second reader. Themes with fewer than 5 cases are reported as untested. Do not let a labeller see model output. Scripts: `scripts/theme_counter.py` (counter and audit sample), the scorers in C:\cca\jev\ (test2_score.py pattern).

## Routing (measured on Habbits, 2026-10-07; re-check per category)
- Jev (TypeSafe, text only, about $0.04 per 1,000 reviews): the counter. Graded probabilities, so its middle band flags its own errors (71% of its errors sit in 0.25 to 0.75).
- Luna (OpenAI Decisions, gpt-6-luna, text and images, about $0.35 per 1,000 reviews): second reader, and anything with an image. Very confident, so it cannot flag its own errors. Refuses very short reviews (use that as "cannot tell"). Its `compares_other_brand` wording broke (precision 0.22): count that theme with Jev only.
- Data rule: public text only, names/handles/emails/URLs stripped (`strip_pii`), never client drafts or NDA material (TypeSafe keeps derived data).
- Hinglish and other languages: unproven (both models missed 4 of 9 true cases on 9 real non-English reviews). Audit those separately when a category has many.

## Habbits question set (the worked example; `references/theme-questions-example-habbits.json`, 22 questions)
Keep the themes brand-specific (written from a first read of that brand's reviews); keep the rules above identical.

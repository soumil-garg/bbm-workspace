# LEGACY: approaches Soumil rejected, kept for history only
Do not copy anything from this folder into a new round. Why each item is here:
- `daigo_round2/` : compositing. The model drew scenes only, code placed the pack on a white die-cut tile and the words on top, sachets were "completely plain". Rejected 10 Oct 2026: "it looks like you've just pasted the product and text on pic ... the sachets look like condom packs".
- `daigo_build_round1.py`, `daigo_make_cutouts.py`, `daigo_qa_round1.py` : round 1, the pack cut out and placed by code, plain foil sachets in the scene prompts, literal claims-safe lines. Rejected 9 Oct 2026.
- `daigo_round3/` : the first whole-ad run (graphics approved in spirit) with Hinglish-only lines. Its text still carries the banned trio phaado, daalo, hilao (ruled out as very controversial). The reference images it made now live in `references/examples/daigo_refs/`.
- `critic_template.md`, `sensitivity_template.md`, `make_inputs_r4.py`, `pool_r4.py` : the Daigo-specific copy-gate files, superseded by `references/templates/` and `scripts/make_copy_inputs.py`.
The method that replaced all of this is `references/whole-ad-recipe.md`.

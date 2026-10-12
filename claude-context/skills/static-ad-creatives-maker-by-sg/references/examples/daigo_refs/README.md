# Daigo reference images (the inputs of the loved round 4)
- `pouch_clean_ai.png`: the real Daigo pouch with the "10's" badge, the buttermilk seal and the icon row removed by the model from the site photo (prompt `p_clean_pouch.txt`, claims audit C38). Check it at zoom against the photo; the faint tone-on-tone "buttermilk" print behind the lettering is the real pack's own.
- `sachet_ref.png`: the branded slim stick-pack sachet (prompt `p_sachet_ref.txt`), generated from the clean pouch because no photo of the real sachet front exists yet. It is a reconstruction; replace it when the client sends a real photo.
Used by `references/templates/ads_config.example.json` through the {SKILL} path placeholder.

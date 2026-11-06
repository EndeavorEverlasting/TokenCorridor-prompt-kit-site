# TokenCorridor-prompt-kit-site — Agent Governance

Operating rules: evidence before action; bounded scope and one writer; reuse existing owners; never expose secrets, overwrite unique work or claim success without observed validation, commit and integration proof.

## Retired product and canonical routing (P00 / P01 / P04)
AgentSwitchboard is a retired product; historical donor evidence and verified existing caller compatibility only. TokenCorridor owns the product control plane: prompts, routing, dispatch authority, Work Graph, proofs and website. Automation supplies reusable primitives; native agents/FirstMate are runtimes, not products. Technical cleanup does not reopen retirement. Do not assign new product work to AgentSwitchboard or infer authority from old plans.


## Moonwake public first-release root — PS-0208
The public Pages homepage `/index.html` is **Moonwake** and must remain byte-identical to `/moonwake/index.html`.
The full generated public Prompt Library lives at `/prompt-library/index.html`; its original immutable release blob SHA is `650c5ba2830e45fde8cbf2348088017e4d496d2b`. Never overwrite the Moonwake entrypoint with a generated catalog.
Pages branch source publishes public `main`; the custom workflow validates source and observes public HTTP but must not race a second deployment owner.
The canonical engineering repo (immutable ID 1382415392) remains private; this repo contains only public static art, typefaces with OFL notices, product HTML and the already-published Prompt Kit.
Updates to the source's generated catalog must target `prompt-library/index.html`, not `index.html`. Public live claims require GitHub Pages readback and successful HTTP parity, independently of Git merges.

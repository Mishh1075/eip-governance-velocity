# EIP Governance Velocity

A first analysis of how fast Ethereum proposals move through their statuses, prepared for
[EIPsInsight](https://github.com/AvarchLLC/eipsinsight-v4) (`docs/INTERN-TASKS.md`, item 2.3: Governance Velocity dashboard).

**Open the notebook:** [`eip_governance_velocity.ipynb`](eip_governance_velocity.ipynb)

Data: the public Git history of `ethereum/EIPs` and `ethereum/ERCs`, up to 10 November 2026
(1,232 proposals, 2,907 cleaned status changes).

## Key findings

1. **Draft is the slow step.** For proposals created since 2020, a completed Draft spell lasts a median of about 6.8 months for EIPs and 6.0 months for ERCs.
2. **ERCs move faster through review.** Median time in Review is about 2.4 months for ERCs against 6.2 for EIPs, and Last Call about 0.9 against 2.0 months.
3. **Few proposals reach Final.** Of proposals created since 2020, about 10% of EIPs and 17% of ERCs reached Final within 12 months, and about 23% and 25% within 36 months. The overall EIP–ERC difference is not significant (log-rank p ≈ 0.13); ERCs are faster early on.
4. **Stagnancy probability.** An EIP that is six months old and not yet Stagnant has about a 37% chance of turning Stagnant in the next six months. 61% of EIPs created since 2021 were Stagnant within 24 months.
5. **A data gap.** No ERC has moved to Stagnant in the Git history since 15 October 2023, just before ERCs moved to their own repository, even though 216 ERC Drafts are now older than six months. ERC stagnancy after that date cannot be measured from statuses alone.
6. **Coming back.** About 30% of Stagnant spells since 2020 have ended, a median of 3.2 months later, mostly back to Draft.

## Method in brief

* Status changes are read from `git log -G '^status:'` on both repositories; commits shared by both histories are counted once.
* `Moved` is dropped; old statuses are mapped to today's names (Abandoned → Withdrawn, Active → Living, Deferred → Stagnant).
* Time to Final and time to Stagnant use Kaplan-Meier estimates, with proposals still open treated as censored.
* The stagnancy probability is the conditional six-month risk `(S(a) − S(a+6)) / S(a)` for a proposal of age `a`.

Limitations (status history only, Withdrawn treated as censoring, commit dates) are listed at the end of the notebook.

## Reproduce

```bash
git clone https://github.com/ethereum/EIPs.git eips
git clone https://github.com/ethereum/ERCs.git ercs
pip install -r requirements.txt
python extract.py          # rebuilds data/*.csv
jupyter notebook eip_governance_velocity.ipynb
```

Misha Parekh · misha.parekh@somaiya.edu · [linkedin.com/in/misha-parekh](https://linkedin.com/in/misha-parekh)

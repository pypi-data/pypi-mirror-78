eQuilibrator-API
================
[![pipeline status](https://gitlab.com/elad.noor/equilibrator-api/badges/master/pipeline.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![coverage report](https://gitlab.com/elad.noor/equilibrator-api/badges/master/coverage.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![Join the chat at https://gitter.im/equilibrator-devs/equilibrator-api](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/equilibrator-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


A command-line API with minimal dependencies for calculation of standard 
thermodynamic potentials of biochemical reactions using the data found on 
[eQuilibrator](http://equilibrator.weizmann.ac.il/).
Does not require any network connections.

## Current Features

* Example scripts for singleton and bulk calculations.
* Calculation of standard Gibbs potentials of reactions (together with confidence intervals).
* Calculation of standard reduction potentials of half-cells.

To access more advanced features, such as adding new compounds that are not
among the 500,000 currently in the MetaNetX database, try using our 
[Component Contribution](https://gitlab.com/equilibrator/component-contribution)
package.

## Cite us

If you plan to use results from `equilibrator-api` in a scientific publication,
please cite our paper:

Noor E, Haraldsdóttir HS, Milo R, Fleming RMT. Consistent estimation of Gibbs 
energy using component contributions. PLoS Comput Biol. 2013;9: e1003098.

## Installation

The easiest way to get eQuilibrator-API up and running is using virtualenv, PyPI, and Jupyter notebooks:
```
virtualenv -p python3 equilibrator
source equilibrator/bin/activate
pip install equilibrator-api jupyter
curl https://gitlab.com/elad.noor/equilibrator-api/raw/develop/scripts/equilibrator_cmd.ipynb > equilibrator_cmd.ipynb
jupyter notebook
```
Then select the notebook called `equilibrator_cmd.ipynb` and follow the examples in it.

If you are using a Windows environment, that are a few dependencies that
work better under  `conda`. Make sure to first run:
```
conda install -c conda-forge python-levenshtein
```
and only then install the `pip` packages.

## Example Usage

Import the API and create an instance. Creating the EquilibratorAPI class
instance reads all the data that is used to calculate thermodynamic potentials of reactions.

```python
from equilibrator_api import ComponentContribution, Q_
cc = ComponentContribution()
```

- **IMPORTANT NOTE** - version 0.3.2 on PyPI introduces support for Magnesium ion concentration (pMg). Almost all Gibbs energy estimates are affected, and therefore current estimates are not backward-compatible. To revert to the previous estimates, initialize using: `cc = ComponentContribution.legacy()` instead of the default constructor.

You can parse a reaction formula that uses compound accessions from different
databases ([KEGG](https://www.kegg.jp/), [ChEBI](https://www.ebi.ac.uk/chebi/),
[MetaNetX](https://www.metanetx.org/), [BiGG](http://bigg.ucsd.edu/), and a
few others). The following example is ATP hydrolysis 
to ADP and inorganic phosphate, using KEGG compound IDs:

```python
rxn = cc.parse_reaction_formula("kegg:C00002 + kegg:C00001 = kegg:C00008 + kegg:C00009")
```

We highly recommend that you check that the reaction is atomically balanced
(conserves atoms) and charge balanced (redox neutral). We've found that it's
easy to accidentally write unbalanced reactions in this format (e.g. forgetting
to balance water is a common mistake) and so we always check ourselves.

```python
if not rxn.is_balanced():
    print('%s is not balanced' % rxn)
```

Now we know that the reaction is "kosher" and we can safely proceed to
calculate the standard change in Gibbs potential due to this reaction.

```python
cc.p_h = Q_(6.5)  # set pH
cc.ionic_strength = Q_("200 mM")  # set I

print(f"ΔG0 = {cc.standard_dg(rxn)}")
print(f"ΔG'0 = {cc.standard_dg_prime(rxn)}")
print(f"ΔG'm = {cc.physiological_dg_prime(rxn)}")
```

You can also calculate the reversibility index ([Noor et al. 2012](https://doi.org/10.1093/bioinformatics/bts317))
for this reaction.

```python
print(f"ln(Reversibility Index) = {cc.ln_reversibility_index(rxn)}")
```

The reversibility index is a measure of the degree of the reversibility of the
reaction that is normalized for stoichiometry. If you are interested in
assigning reversibility to reactions we recommend this measure because 1:2
reactions are much "easier" to reverse than reactions with 1:1 or 2:2 reactions.
You can see the [paper](https://doi.org/10.1093/bioinformatics/bts317) linked above for more information.

### Pathway analysis tools have been ported to a new project
Running Max-min Driving Force (MDF) or Enzyme Cost Minimization (ECM) anslyses
is no longer part of `equilibrator-api` and has been ported to a separate project
names [`equilibrator-pathway`](https://gitlab.com/equilibrator/equilibrator-pathway).
Note, that the pathway configuration file format used in previous versions of
`equilibrator-api` (prior to 0.2.7) is not longer supported. You can find code
and configuration file examples in the [new repository](https://gitlab.com/equilibrator/equilibrator-pathway/-/tree/develop/examples).

### Further examples for reaction parsing
We support several compound databases, not just KEGG. One can mix between several sources in the same reaction, e.g.:
```python
rxn = cc.parse_reaction_formula("kegg:C00002 + CHEBI:15377 = metanetx.chemical:MNXM7 + bigg.metabolite:pi")
```

Or, you can use compound names instead of identifiers. However, it is discouraged to use in batch, since we only pick
the closest hit in our database, and that can often be the wrong compound. Always verify that the reaction is balanced,
and preferably also that the InChIKeys are correct:
```python
rxn = cc.search_reaction("beta-D-glucose = glucose")
print(rxn)
```
In this case, the matcher arbitrarily chooses `alpha-D-glucose` as the first hit for the name `glucose`.
Therefore, it is always better to use the most specific synonym to avoid mis-annotations.

## Dependencies:
- python >= 3.7
- equilibrator-cache (latest)
- component-contribution (latest)
- numpy
- scipy
- pandas
- matplotlib
- quilt
- path
- pint
- uncertainties
- pyparsing
- python-Levenshtein-wheels
- sqlalchemy
- periodictable
- cobra (optional)

## Troubleshooting:

### "Download failed" error when initializing `ComponentContribution()`
eQuilibrator uses [Quilt](https://quiltdata.com/) to store the data required for its estimates. During the first time you initialize `equilibrator_api.ComponentContribution()` on a new machine, about 1.4 GigaBytes of data is downloaded from the Quilt servers, a process that can sometimes take up to 1 hour. If the downloaded is interupted, a corrupt local version of the DB might be stored, and one needs to remove it in order to start over. That requires you to [install quilt](https://docs.quiltdata.com/installation) and run the following commands in your shell:
```bash
quilt rm equilibrator/cache
quilt rm equilibrator/component_contribution
```

If you have a slow connection, it is recommended to use quilt directly to install the DB, before using equilibrator-api:
```bash
quilt install equilibrator/cache
quilt install equilibrator/component_contribution
```


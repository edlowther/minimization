### Minimization

This is a Python implementation of some software written in Perl by a team at Nuffield in Oxford called OxMaR (Oxford Minimization and Randomization) and released under the Creative Commons Attribution licence in 2014. Full details of original tool were published in Plos One. 

The aim of the tool is to enable researchers to use the concept of minimization to allocate research trial participants to either the control or intervention groups; essentially this means flipping a "biased coin" so that there is a random element to the allocation decision but the differences between the two groups on key variables of interest (e.g. demographic, contextual) are minimized. 

This repository is configured so that any changes pushed to the `new-participant-data.yaml` file will trigger a GitLab runner to both do the allocation and report the results back to trial administrators via the main `README.md` file. We assume that each new trial participant gets a new, unique id, and this is stored in the yaml file. If this assumption is not met, e.g. due to data entry error, this will be reported back to the trial administrators via the `README.md` document. 

There is also a secondary feature in the `./demo` directory which enables scrutiny of how the `minimisation_weight` variable functions; in essence, it strikes the balance between fully deterministic minimisation and a fully random allocation process, as can be seen in the `sensitivity-analysis.md` document. 

There are no automated tests, but the code has been extensively user tested by the research team. 

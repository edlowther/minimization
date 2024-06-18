# Minimization with GitLab

### Prerequisites

Follow the installation instructions available on [the project homepage](https://github.com/edlowther/minimization).

It is also helpful to have a good feel for how `yaml` files work as this will be at the heart of your interface with the software. If you haven't used `yaml` much before, it may be worth reading [this tutorial](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started); although you shouldn't need to do too much with the files (mostly it's just swapping `1`s and `0`s around), unintentional changes can cause problems that are hard to debug if you're new to the syntax of `yaml`.

### Running a project

To get started, define categories that you would like to minimise differences over and all their possible values in `initialize-project.yaml`. Please note that the values need to be mutually exclusive; a trial participant cannot have both `value_a` and `value_b` in `category_1`. Also please note that the values must all be unique; there cannot be a `value_a` in both `category_1` and `category_2`. Beyond these restrictions, the categories and values can take on any names that you assign to them in this file.

You can directly edit the `initialize-project.yaml` file in your web browser - open the file, click on the blue button labelled "Edit", then click on "Edit single file".

Once you have finished entering the relevant information for your study, scroll down and click "Commit changes" (ensuring that the Target Branch is listed as `gitlab`).

This will prompt GitLab to generate three things:

1. Analysis of how different values of the `minimisation_weight` variable would affect the distribution of the characteristics you have entered, which you will be able to see (after a short delay) [here](./demo/sensitivity-analysis.md)
2. A new input yaml file, `new-participant-data.yaml`, which you can use to enter an individual participant's data as they are recruited to your trial. Nb you must ensure that exactly one value is set to `1` for each category; all others must be set to `0`. Once you hit "Commit changes" (as above), GitLab will assign this trial participant to the Control or Intervention group and report back to which one via this page (replacing this information in your copy of the project, although you can refer back to them on the [project homepage](https://github.com/edlowther/minimization/tree/gitlab) if needed)
3. A new output file, `allocations.csv` - this is where the information you have entered for each trial participant and the study group they were assigned to is stored and kept under `git` version control

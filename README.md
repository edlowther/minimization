# Minimization via GitLab

### Prerequisites

Follow the installation instructions available at [...]

### Running a project

To get started, define categories that you would like to minimise differences over and all their possible values in `initialize-project.yaml`. 

One way of achieving this is directly editing the file in your web browser - open the file, click on the blue button labelled "Edit", then click on "Edit single file". 

Once you have finished entering this information, scroll down and click "Commit changes" (ensuring that the Target Branch is listed as `gitlab`). 

This will prompt GitLab to generate two things: 

1. Analysis of how different values of the `minimisation_weight` variable would affect the distribution of the characteristics you have entered, which you will be able to see (after a short delay) [here](./demo/sensitivity-analysis.md)
2. A new yaml file, `new-participant-data.yaml`, which you can use to enter an individual participant's data as they are recruited to your trial. Nb you must ensure that exactly one value is set to `1` for each category; all others must be set to `0`. Once you hit "Commit changes" (as above), GitLab will assign this trial participant to the Control or Intervention group and report back to which one via this page
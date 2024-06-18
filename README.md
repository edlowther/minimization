# Minimization

Open-source software to randomly allocate participants in clinical trials to the control or experimental arms of a study, while minimizing differences in the distribution of key patient characteristics between the two study groups. 

### Motivation

While the generation of a "biased coin" that manifests the minimization algorithm is relatively straightforward, to the best of our knowledge there are no open-source implementations that can keep a record of how different trial participants have been assigned to groups over the course of a study that do not require advanced web-development skills and at least some investment in back-end infrastructure.

Our approach is to make use of `git`, which - along with the server-side tools available on its dominant web-based platforms free of charge - is extremely well suited to this task.

This repository will guide you through the configuration required to get you started on your own project. 

### Usage

This software was deployed inside UCL's Trusted Research Environment (the [Data Safe Haven](https://www.ucl.ac.uk/isd/services/file-storage-sharing/data-safe-haven-dsh)) on a secure instance of GitLab. 

To review the code as it was used there, please see the `production` [branch of this repository](https://github.com/edlowther/minimization/tree/production).

To run a customised version of this software for your own clinical trial, please follow these steps:

- First create an account on [GitLab](https://about.gitlab.com/) - if you are new to the platform you may wish to start with the free trial option
- Enter your details, then click on "Import" for your first project
- Your project will need to be assigned to a "group name", enter something apt then click on "Repository by URL"
- Enter the url: https://github.com/edlowther/minimization.git
- Leave "Mirror repository" unchecked, and give the project a name and a "slug" e.g. `minimization` for both
- Set the visibility level - "Private" may be a good choice if real patient data is involved (even if it is anonymized), then click "Create project"
- Once your project has been created, click on "Settings" in the left-hand navigation bar, then "Access Tokens"
- Click on "Add new" then give it a name (e.g. `minimization`) and an expiry date that can be up to one year into the future
- For "Select a role", choose "Developer", then check the `write_repository` box
- Click "Create project access token", and click on the clipboard icon that appears to copy this into your clipboard
- Click on "Settings" again in the left-hand navigation bar, then "CI/CD"
- "Expand" the Variables section, and click "Add variable"
- Set Visibility to "Masked"
- Uncheck "Protect variable"
- In the "Key" text entry field type "ACCESS_TOKEN" (without the quotation marks)
- Paste the token that should still be in your clipboard into the "Value" text entry field, then click "Add variable"
- Click on "Settings" then "Repository" in left-hand navigation bar, then "Expand" the "Branch defaults" section
- Select `gitlab` to be the new default branch, then click "Save changes"
- From the project homepage, click on `.gitlab-ci.yml` - then click on the blue "Edit" button, then "Edit single file"
- Enter your GitLab username and email address in the relevant git config lines, you can use the `noreply` GitLab email address if you like, which follows this pattern: `<YOUR_GITLAB_USER_ID>-<YOUR_GITLAB_USERNAME>@users.noreply.gitlab.com` (you can find the user id in your [user settings](https://gitlab.com/-/user_settings/profile))
- Change the git remote url so that it follows the pattern: `https://<YOUR_GITLAB_USERNAME>:$ACCESS_TOKEN@gitlab.com/<YOUR_GITLAB_ORG_NAME>/<YOUR_PROJECT_NAME>`
- Double check your configuration changes then click "Commit changes"
- Click on pipelines, then "Verify my account", then enter the data requested to enable this project to function on GitLab

The project configuration should now be complete, and you can start adding trial-specific data. Follow the instructions in the README displayed at the [root of the `gitlab` branch](./-/tree/gitlab).

A separate branch containing an alternative version of the software that can be deployed on GitHub will be published here in due course. 

### References

For an excellent explanation of the concept of minimisation in this context, please see: 

- O’Callaghan CA (2014) OxMaR: Open Source Free Software for Online Minimization and Randomization for Clinical Trials. PLoS ONE 9(10): e110761. https://doi.org/10.1371/journal.pone.0110761
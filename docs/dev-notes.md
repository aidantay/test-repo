# Developer Notes

### How to make the follow-up run 100% automatic in the future

To allow the PR merge to automatically trigger the follow-up tag creation without manually clicking "Run workflow":

1. Create a GitHub Personal Access Token (PAT) with repo scope (or GitHub App Token).
2. Save it in your repository: Settings → Secrets and variables → Actions → New repository secret → Name:
RELEASE_PAT.

Because RELEASE_PAT is a user token (not default GITHUB_TOKEN), GitHub will automatically trigger the follow-up
ci.yml run as soon as the Release PR is merged!

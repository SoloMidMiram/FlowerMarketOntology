# Pull request review

The sole maintainer authorizes merges. This policy applies to every pull request, including the maintainer’s own changes. A second human GitHub approval is optional.

Before merging, record the following in the pull request:

- The reviewed head commit SHA and any prerequisite pull requests.
- The technical review findings, how blocking findings were resolved, and any follow-up issues. A coding agent can provide an independent technical assessment. Record its findings as review evidence and reserve GitHub approval for eligible human reviewers.
- Links to passing GitHub Actions runs for the reviewed revision. Require the applicable tests, security checks, and repository validation configured for the change. If a check is unavailable, record the gap and the verification performed. Resolve required check failures before merging.
- The maintainer’s merge decision. For critical changes, including permissions, secrets, CI enforcement, publication controls, or breaking schema changes, the maintainer must explicitly authorize the reviewed SHA in the pull request before merging.

If the head changes, review the new changes and refresh the check evidence and any explicit authorization before merging.

Merging research or ontology code authorizes the repository change only. Before publishing botanical care claims or associated imagery, record each applicable release decision separately.

- **Evidence verification.** Verify the botanical identity and the sources supporting each proposed care claim, including the conditions under which it applies.
- **Editorial approval.** Approve the actual publication wording in each applicable locale, with attribution and uncertainty preserved.
- **Image licensing.** Verify permission for the intended use and record the license and any required attribution for each image before publication.

Keep the affected material unpublished until its release gates are satisfied. The repository owner can make and record these decisions as solo maintainer.

Policy reference: [SahebKhabar PR #3](https://github.com/SoloMidMiram/SahebKhabar/pull/3).

# Laboratory Work 3 — CI/CD with GitHub Actions

**Course:** DevOps Essentials — Containerization, Orchestration and CI/CD  
**Student:** [Your name]  
**Date:** [Submission date]

## Objective
Create a GitHub Actions CI/CD pipeline for a Flask ToDo application: automatically execute tests on pushes and pull requests and publish a Docker image to Docker Hub after successful tests on `main`.

## Links (complete after pushing)
- GitHub repository: [ADD PUBLIC REPOSITORY URL]
- Successful Actions run (both jobs): [ADD RUN URL]
- Docker Hub repository: [ADD IMAGE URL]

## Part 1 — Repository and tests
The supplied application includes four pytest tests: healthy endpoint, empty ToDo list, add a ToDo, and reject a missing title. Expected baseline `4 passed`.

**Actual local result and environment:** [FILL IN AFTER RUNNING]  
**Screenshot:** [ADD LOCAL TEST SCREENSHOT IF REQUIRED]

## Part 2 — Test-only workflow
`ci.yml` triggers on `push` to `main`, pull requests targeting `main`, and manually with `workflow_dispatch`. The `test` job checks out source, sets up Python 3.12, installs dependencies, and runs `pytest -v`.

**Result:** [ADD GREEN ACTIONS RUN STATUS]  
**Screenshot 1:** [ADD SCREENSHOT OF ACTIONS LOG: 4 passed]

## Part 3 — Deliberately fail and repair
In `app/main.py`, the `/health` endpoint is intentionally changed from `jsonify(status="ok")` to `jsonify(status="OK")`. The expected failing test is **`test_health`**, because the returned JSON no longer matches `{"status": "ok"}`. After restoring lowercase `ok`, the tests should pass again.

**Actual failure log:** [ADD EXACT LOG SNIPPET AFTER GITHUB RUN]  
**Screenshot 2:** [ADD RED FAILED RUN]  
**Screenshot 3:** [ADD GREEN FIXED RUN]

## Part 4 — GitHub Secrets
The following repository secrets must be created: `DOCKERHUB_USERNAME` (Docker Hub user) and `DOCKERHUB_TOKEN` (write-enabled access token). Their values must not be committed or displayed in the report.

**Screenshot 4:** [ADD SCREENSHOT SHOWING SECRET NAMES ONLY]

## Part 5 — Image build and publication
The `build-and-push` job has `needs: test`, so it waits for successful tests. Its `if` expression limits publication to the `main` branch for non-PR events. Docker actions log in, configure Buildx, and publish tags `latest` and the SHA of the commit.

**Result:** [ADD ACTUAL BUILD RESULT]  
**Screenshot 5:** [ADD BOTH JOBS SUCCESSFUL]  
**Screenshot 6:** [ADD DOCKER HUB TAGS]

## Part 6 — Running the published image
Commands: `docker run -d --rm -p 5000:5000 --name todo USER/todo-app:latest` and `curl http://localhost:5000/health`.

**Expected output:** `{"status":"ok"}`  
**Actual output:** [ADD ACTUAL OUTPUT]  
**Screenshot 7:** [ADD HEALTH ENDPOINT TEST]

## Part 7 — Pull request behavior
A feature branch adds the test `test_second_todo_gets_id_two`, then opens a pull request to `main`. Test job should run; publishing should be skipped. After merge, both jobs should run on `main`.

**Actual PR link:** [ADD PR URL]  
**Screenshot 8:** [ADD PR TEST PASS + BUILD SKIPPED]  
**Screenshot 9:** [ADD POST-MERGE BUILD RUN]

## Written answers required by the assignment

**1. Which test failed in Part 3, and why?**  
`test_health` fails because the test expects lowercase `{"status":"ok"}`, but the intentionally modified endpoint returns uppercase `{"status":"OK"}`. Paste the exact GitHub failure message above after running it.

**2. Why does Part 7 skip `build-and-push`?**  
The job has `if: github.ref_name == 'main' && github.event_name != 'pull_request'`. On a pull request, `github.event_name` is `pull_request`, so the condition is false. Images are published only for appropriate events on `main` after successful tests.

**3. Why publish a tag with the commit SHA in addition to `latest`?**  
`latest` is movable and can point to a newer image. A commit SHA tag identifies the image built for one specific revision, making it easier to reproduce a deployment, investigate regressions, or roll back. (Docker tags themselves are mutable unless registry controls enforce immutability.)

## Oral defense — sample short answers

- **What if `needs: test` is removed?** The two jobs can run in parallel, and publishing no longer waits for the test job.
- **Why repeat `actions/checkout` in the build job?** Separate jobs run on separate fresh runners; the build job must fetch its own source files.
- **Where is the Docker Hub token?** GitHub Actions repository secrets; GitHub redacts recognized secret values from logs.
- **What if the token secret is missing?** Docker login/push will fail due to missing credentials.
- **Why `permissions: contents: read`?** Grants the default workflow token only source read access rather than broader repository permissions.
- **`run` vs `uses`?** `run: pytest -v` executes a shell command; `uses: actions/checkout@v6` invokes an action.
- **How to run manually?** GitHub Actions → select CI/CD → Run workflow, enabled by `workflow_dispatch`.

## Status and honesty note
This file is a **report draft**, not evidence of a completed GitHub run. Fill placeholders with real links, logs, and screenshots after completing the external GitHub/Docker Hub steps.

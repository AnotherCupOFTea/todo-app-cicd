# Lab 3 — CI/CD with GitHub Actions (ToDo Flask App)

This repo is based on the supplied **todo-app-starter.zip**. The final workflow is at `.github/workflows/ci.yml`.

## Expected project tree

```text
.github/workflows/ci.yml
app/__init__.py
app/main.py
tests/test_main.py
requirements.txt
pytest.ini
Dockerfile
.dockerignore
.gitignore
README.md
LAB_REPORT.md
PR_TEST_TO_ADD.txt
```

## 1. Local setup (Part 1)

Use Python 3.12 (Windows PowerShell):

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

On macOS/Linux, use `python3 -m venv .venv`, then `source .venv/bin/activate`.

Expected initial result: `4 passed`.

Create a **public** GitHub repo called `todo-app` (no README when creating it, because this project already includes README). Run inside this folder:

```bash
git init
git add .
git commit -m "Initial ToDo app with CI/CD workflow"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/todo-app.git
git push -u origin main
```

> This package includes the **final** workflow already. For exact chronological evidence for Part 2, temporarily use the test-only workflow described below before configuring Docker Hub. Then restore the full final workflow.

## 2. Demonstrate test-only CI (Part 2)

For Part 2, temporarily remove the entire `build-and-push:` job from `ci.yml` (and optionally the unused env section), commit and push. The workflow still runs `test` on `push`, `pull_request` and manual `workflow_dispatch`. Go to GitHub → **Actions** → CI/CD → test → Run tests. Capture screenshot showing **4 passed**. Restore the full workflow for Part 5.

## 3. Demonstrate CI failure and repair (Part 3)

Change `return jsonify(status="ok")` in `app/main.py` to `return jsonify(status="OK")`, then:

```bash
git add app/main.py
git commit -m "Break health check"
git push
```

In Actions, capture the failed test. **Expected reason:** `test_health` expects `{"status": "ok"}`, but gets `{"status": "OK"}`.

Revert `OK` to `ok`:

```bash
git add app/main.py
git commit -m "Fix health check"
git push
```

Capture the successful run. **Do the break/fix before enabling image publishing**, so the failed run can't be mistaken for a publishing run.

## 4. Docker Hub secrets (Part 4)

Create Docker Hub account and a `todo-app` repository. Generate a Docker Hub personal access token with **write** access.

GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**:

- `DOCKERHUB_USERNAME`: your Docker Hub username
- `DOCKERHUB_TOKEN`: your Docker Hub access token

Do **not** put secrets in code, screenshots, commits, or lab reports. Screenshot only secret **names**.

## 5. Build and publish (Part 5)

Restore the supplied complete `.github/workflows/ci.yml`. Commit it:

```bash
git add .github/workflows/ci.yml
git commit -m "Add Docker build and publish job"
git push
```

Actions → latest CI/CD run → expect `test` then `build-and-push`. Docker Hub should show `latest` and a full Git commit SHA tag.

Publishing requires the GitHub and Docker Hub accounts and repository secrets; it cannot be completed from this prepared ZIP alone.

## 6. Pull and test the published image (Part 6)

```bash
docker pull YOUR_DOCKERHUB_USERNAME/todo-app:latest
docker run -d --rm -p 5000:5000 --name todo YOUR_DOCKERHUB_USERNAME/todo-app:latest
curl http://localhost:5000/health
curl -X POST -H "Content-Type: application/json" -d '{"title":"Submit Lab 3"}' http://localhost:5000/todos
curl http://localhost:5000/todos
docker stop todo
```

Expected health response: `{"status":"ok"}`. For Windows PowerShell use `curl.exe` rather than `curl` to preserve curl syntax; quoting JSON may vary by shell. Port conflict? Use `-p 5050:5000` and `localhost:5050`.

## 7. PR — test only (Part 7)

```bash
git checkout -b feature/new-test
```

Copy the test from `PR_TEST_TO_ADD.txt` into the **end** of `tests/test_main.py`. Then:

```bash
git add tests/test_main.py
git commit -m "Add second todo ID test"
git push -u origin feature/new-test
```

Open a PR targeting `main`. The `test` job runs (expect **5 passed**), but `build-and-push` is **skipped** because the event is `pull_request` and the workflow's `if` excludes PRs. Capture screenshots; merge the PR. A new push to `main` triggers both jobs and new `latest` + SHA image tags.

## Deliverables

Complete `LAB_REPORT.md` by adding real screenshots and links to: (1) public GitHub repo, (2) successful run showing **both** jobs, and (3) Docker Hub image. Never invent a completed run or screenshot.

## Notes about the cloud-services PDF

The separate `Cloud_Services_IaaS_PaaS_SaaS.pdf` explains that Railway is PaaS and DigitalOcean droplets are IaaS. This lab publishes a Docker image to **Docker Hub**; it does **not** require deploying the app to Railway or DigitalOcean. Publishing a Docker image is not itself deployment to a running web server.

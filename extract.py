"""Rebuild data/status_events.csv and data/proposals.csv from the public EIPs and ERCs repositories.

Usage:
    git clone https://github.com/ethereum/EIPs.git eips
    git clone https://github.com/ethereum/ERCs.git ercs
    python extract.py
"""
import csv, os, re, subprocess

REPOS = {"eips": ("EIPS", "eip"), "ercs": ("ERCS", "erc")}
LOG = ["git", "log", "--no-merges", "--format=@@COMMIT %H %aI", "-p", "--unified=0", "-G", "^status:", "--", "EIPS/*.md", "ERCS/*.md"]

events = {}
for repo in REPOS:
    out = subprocess.run(LOG, cwd=repo, capture_output=True, text=True, errors="replace").stdout
    commit = date = num = old = None
    for line in out.splitlines():
        if line.startswith("@@COMMIT"):
            _, commit, date = line.split(" ", 2); num = None
        elif line.startswith("diff --git"):
            m = re.search(r" b/(EIPS|ERCS)/(?:eip|erc)-(\d+)\.md$", line); num = int(m.group(2)) if m else None; old = None
        elif num is not None and line.startswith("-status:"):
            old = line.split(":", 1)[1].strip()
        elif num is not None and line.startswith("+status:"):
            # the same commit can appear in both repositories (shared history); key on (commit, number) to count it once
            events[(commit, num)] = dict(number=num, commit=commit, date=date, old=old, new=line.split(":", 1)[1].strip(), repo=repo)

props = {}
for repo, (folder, prefix) in REPOS.items():
    for f in os.listdir(os.path.join(repo, folder)):
        m = re.match(prefix + r"-(\d+)\.md$", f)
        if not m:
            continue
        txt = open(os.path.join(repo, folder, f), encoding="utf-8", errors="replace").read(4000)
        get = lambda k: (re.search(rf"^{k}:\s*(.+)$", txt, re.M) or [None, ""])[1].strip()
        if repo == "eips" and get("status") == "Moved":
            continue
        n = int(m.group(1))
        props[n] = dict(number=n, kind="ERC" if repo == "ercs" else "EIP", status=get("status"), type=get("type"),
                        category=get("category"), created=get("created"), title=get("title"))

os.makedirs("data", exist_ok=True)
with open("data/status_events.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["number", "commit", "date", "old", "new", "repo"]); w.writeheader()
    w.writerows(sorted(events.values(), key=lambda r: (r["number"], r["date"])))
with open("data/proposals.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["number", "kind", "status", "type", "category", "created", "title"]); w.writeheader()
    w.writerows(sorted(props.values(), key=lambda r: r["number"]))
print(len(events), "status events;", len(props), "proposals")

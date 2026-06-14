#!/usr/bin/env python3
"""
generate_content.py — build content.json for the Learn-on-the-go PWA
from Scott's Second Brain academic sets.

Reads:
  <second_brain>/Academic/<Subject>/quiz.md      -> quiz cards
  <second_brain>/Courses/<Subject>/course.md     -> course lessons

Writes:
  <out>/content.json

Auto-includes any NEW set you build later (it just scans the folders).
Portable: pass the Second Brain path + output path as args.

Usage:
  python3 generate_content.py "/path/to/Second Brain" "/path/to/output_dir"
"""
import sys, os, re, json, datetime, glob

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def parse_quiz(md):
    """Cards: a line '**Qn.** question' followed by a line 'A. answer'."""
    cards = []
    lines = md.splitlines()
    i = 0
    qre = re.compile(r'^\*\*Q\d+[.\)]?\*\*\s*(.+)$')
    are = re.compile(r'^A[.\)]\s*(.+)$')
    while i < len(lines):
        m = qre.match(lines[i].strip())
        if m:
            q = m.group(1).strip()
            a = ""
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if not s:
                    j += 1; continue
                am = are.match(s)
                if am:
                    a = am.group(1).strip()
                break
            if a:
                cards.append({"q": q, "a": a})
        i += 1
    return cards

def parse_course(md):
    """Lessons from the syllabus list + any full '## Lesson N' sections."""
    lessons = {}
    # syllabus: - **L1 — Title.** teaser
    syl = re.compile(r'^-\s*\*\*L(\d+)\s*[—-]\s*(.+?)\.\*\*\s*(.*)$')
    for line in md.splitlines():
        m = syl.match(line.strip())
        if m:
            n = int(m.group(1))
            lessons[n] = {"n": n, "title": m.group(2).strip(),
                          "body": m.group(3).strip(), "check": "", "full": False}
    # full lessons: ## Lesson N ... (until next ##)
    blocks = re.split(r'\n(?=## )', md)
    lre = re.compile(r'^##\s*Lesson\s*(\d+)', re.I)
    for b in blocks:
        m = lre.match(b.strip())
        if m:
            n = int(m.group(1))
            body = re.sub(r'^##\s*Lesson\s*\d+[^\n]*\n', '', b.strip()).strip()
            check = ""
            cm = re.search(r'\*\*Check:\*\*\s*(.+)', body)
            if cm:
                check = cm.group(1).strip()
            lessons.setdefault(n, {"n": n, "title": f"Lesson {n}"})
            lessons[n]["body"] = body
            lessons[n]["check"] = check
            lessons[n]["full"] = True
    return [lessons[k] for k in sorted(lessons)]

def main():
    sb = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/Documents/Claude/Projects/Second Brain")
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    subjects = {}
    # Academic sets -> quizzes
    for d in sorted(glob.glob(os.path.join(sb, "Academic", "*"))):
        if not os.path.isdir(d):
            continue
        name = os.path.basename(d)
        if name.startswith("_") or name.startswith("."):
            continue
        cards = parse_quiz(read(os.path.join(d, "quiz.md")))
        subjects.setdefault(name, {"id": re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'),
                                   "title": name, "lessons": [], "quiz": []})
        subjects[name]["quiz"] = cards
    # Courses -> lessons
    for d in sorted(glob.glob(os.path.join(sb, "Courses", "*"))):
        if not os.path.isdir(d):
            continue
        name = os.path.basename(d)
        if name.startswith("_") or name.startswith("."):
            continue
        lessons = parse_course(read(os.path.join(d, "course.md")))
        subjects.setdefault(name, {"id": re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'),
                                   "title": name, "lessons": [], "quiz": []})
        subjects[name]["lessons"] = lessons
    data = {
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "subjects": [subjects[k] for k in sorted(subjects)
                     if subjects[k]["lessons"] or subjects[k]["quiz"]],
    }
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "content.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    nq = sum(len(s["quiz"]) for s in data["subjects"])
    nl = sum(len(s["lessons"]) for s in data["subjects"])
    print(f"Wrote content.json: {len(data['subjects'])} subjects, "
          f"{nl} lessons, {nq} quiz cards.")

if __name__ == "__main__":
    main()

"""Turn the Phase Tagger's records (saved as JSON files by Claude) into _build/phase_tags.py, and the page orders
(the sibling pageorders/ folder, when it was read too) into _build/page_order.py.
Usage: python3 _build/sync_tags.py <folder of videos/*.json>"""
import json, glob, sys, os, pprint
rows = sorted((json.load(open(f)) for f in glob.glob(os.path.join(sys.argv[1], "*.json"))), key=lambda d: d.get("order", 0))
tags = {}
for d in rows:
    t = dict(order=d.get("order", 0), title=d["title"], phases=d.get("phases", []), roles=d.get("roles", []), formats=d.get("formats", []))
    if "Other" in t["roles"] and d.get("otherRole", "").strip(): t["other"] = d["otherRole"].strip()
    tags[d["spec"]] = t
out = '''# Tags for every video on the site: When (phases), Who (roles, with "other" naming any other role) and
# What (formats). Set by Mark in the Phase Tagger page on Claude; Claude syncs it here with _build/sync_tags.py.
# A video listed here appears on exactly the role and format pages its tags name, under those phases.
TAGS = ''' + pprint.pformat(tags, width=140, sort_dicts=False) + "\n"
open(os.path.join(os.path.dirname(__file__), "phase_tags.py"), "w").write(out)
print(len(tags), "videos synced")

# Page order: Mark's play order for each role and format page (Phase Tagger, Page order view).
od = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "pageorders")
if os.path.isdir(od):
    orders = {}
    for f in sorted(glob.glob(os.path.join(od, "*.json"))):
        d = json.load(open(f)); d = d.get("data", d)
        if d.get("page") and d.get("order"): orders[d["page"]] = list(d["order"])
    out = '''# Mark's play order for each role and format page, set in the Phase Tagger's Page order view; Claude syncs it
# here with _build/sync_tags.py. Videos tagged for a page but missing from its list play after the listed ones.
ORDER = ''' + pprint.pformat(orders, width=140, sort_dicts=False) + "\n"
    open(os.path.join(os.path.dirname(__file__), "page_order.py"), "w").write(out)
    print(len(orders), "page orders synced")

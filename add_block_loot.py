import json, os, glob

loot_dir = r"i:\.m\.minecraft\versions\1.20.1-Forge_47.3.22\thingpacks\Extended-Storage\data\extended_storage\loot_tables\blocks"

for filepath in glob.glob(os.path.join(loot_dir, "*.json")):
    filename = os.path.basename(filepath)
    block_id = "extended_storage:" + filename.replace(".json", "")

    with open(filepath, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    changed = False
    for pool in data.get("pools", []):
        for cond in pool.get("conditions", []):
            if isinstance(cond, dict) and cond.get("condition") == "minecraft:inverted":
                term = cond.get("term", {})
                if term.get("condition") == "minecraft:block_state_property" and "block" not in term:
                    term["block"] = block_id
                    changed = True
                    print(f"  Fixed: {filename}")

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

print("Done!")

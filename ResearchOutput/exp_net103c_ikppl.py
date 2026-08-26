#!/usr/bin/env python3
import json, os, re, subprocess

IK = os.path.expanduser("~/f3cache/llama.cpp-ik/build/bin")
Q8 = os.path.expanduser("~/f3cache/gguf/qwen2.5-7b-instruct-q8_0-00001-of-00003.gguf")
SLICE = "/tmp/net103_slice.txt"
print("slice exists:", os.path.exists(SLICE), os.path.getsize(SLICE), flush=True)
p = subprocess.run([os.path.join(IK, "llama-perplexity"), "-m", Q8,
                    "-f", SLICE, "-c", "2048", "-t", "8"],
                   capture_output=True, text=True, timeout=14400)
o = p.stdout + p.stderr
open("/tmp/net103_ikppl_raw.txt", "w").write(o[-3000:])
finals = [l for l in o.splitlines() if "Final estimate" in l]
val = None
for l in finals:
    nums = re.findall(r"=\s*([0-9]+\.[0-9]+)", l)
    if nums:
        val = float(nums[-1])
d = json.load(open("/home/raver1975/f3cache/net103b_results.json"))
d["ppl_ik_7bq8_fixed"] = val
d["ik_final_lines"] = finals
json.dump(d, open("/home/raver1975/f3cache/net103b_results.json", "w"), indent=1)
print(f"ik ppl fixed parse: {val}", flush=True)
print("ALL_DONE_NET103C", flush=True)

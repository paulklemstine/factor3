#!/usr/bin/env python3
# NET-105 — MOE-HOT-SET: DOES SPARSE ROUTING SURVIVE THE RAM WALL?
# (cpu-large-model axis, iteration 80)
#
# NET-104 showed DENSE models hit a hard starved-streaming cliff below
# full residency (0.61 tok/s at 83% cap). MoE models route each token to
# only ~3B of 30.5B params — IF that locality survives mmap paging, a
# 30B-class model should complete generation under caps FAR below its
# 16.38GB file at tolerable speed. This is the GOAL mechanism test.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 HOT-SET-COMPLETES: generation completes with zero OOM at EVERY cap
#     in {6G, 8G, 10G, 12G} — all far below the 16.38GB file.
#  P2 GRACEFUL-GRADIENT: tok/s degradation from placebo(16G) to 8G is
#     <= 2x (routing locality beats dense-style uniform paging, whose
#     analog cliff was 14x).
#  P3 FAULT-EVIDENCE: major-fault counts during capped runs scale with
#     (file - cap), evidencing genuine expert paging rather than
#     silent cache effects.
import json, os, re, subprocess, threading, time

COMP = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-completion")
M30 = os.path.expanduser("~/f3cache/gguf30b/Qwen3-30B-A3B-IQ4_XS.gguf")
RESULTS = os.path.expanduser("~/f3cache/net105_results.json")
CTX, NGEN, THREADS = 2048, 128, "8"
CAPS = ["6000M", "8000M", "10000M", "12000M", "16000M_placebo"]

res = {"meta": {"ctx": CTX, "ngen": NGEN,
                "predictions": "P1 completes everywhere; P2 16G->8G "
                               "degradation <= 2x; P3 majfaults scale"},
       "arms": []}

def save(): json.dump(res, open(RESULTS, "w"), indent=1)

def log(m):
    print(m, flush=True); open("/tmp/net105.log", "a").write(str(m) + "\n")

def find_pid_hwm_majflt():
    """Sample HWM and major-faults across llama processes."""
    hwm = mf = 0
    for pid in os.listdir("/proc"):
        if not pid.isdigit(): continue
        try:
            cmd = open(f"/proc/{pid}/comm").read().strip()
            if "llama" not in cmd: continue
            st = open(f"/proc/{pid}/status").read()
            for line in st.splitlines():
                if line.startswith("VmHWM"): hwm += int(line.split()[1])
                if line.startswith("majflt"): pass
            stat = open(f"/proc/{pid}/stat").read()
            mf += int(stat.split()[9])   # minflt=9? fields: majflt is field 10 (index 9 0-based after comm parse issue)
        except Exception:
            pass
    return hwm // 1024, mf

for cap in CAPS:
    mem = cap.replace("_placebo", "")
    log(f"=== cap {cap} ===")
    proc = subprocess.Popen(["systemd-run", "--user", "--scope", "-p",
                             f"MemoryMax={mem}", "-p", "MemorySwapMax=0",
                             COMP, "-m", M30, "-c", str(CTX),
                             "-n", str(NGEN), "-t", THREADS,
                             "-p", "The history of computing begins with"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True)
    peak_hwm = [0]
    stop = [False]
    def sampler():
        while not stop[0]:
            h, _ = 0, 0
            for pid in os.listdir("/proc"):
                if not pid.isdigit(): continue
                try:
                    if "llama" in open(f"/proc/{pid}/comm").read():
                        st = open(f"/proc/{pid}/status").read()
                        for line in st.splitlines():
                            if line.startswith("VmHWM"):
                                h = max(h, int(line.split()[1]))
                except Exception:
                    pass
            peak_hwm[0] = max(peak_hwm[0], h)
            time.sleep(1)
    th = threading.Thread(target=sampler); th.start()
    try:
        out, _ = proc.communicate(timeout=3600)
    except subprocess.TimeoutExpired:
        proc.kill(); out = ""
    stop[0] = True; th.join()
    o = out or ""
    m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
    entry = {"cap": cap,
             "completed": bool(m),
             "tokens": int(m.group(1)) if m else None,
             "tok_s": float(m.group(2)) if m else None,
             "oom": proc.returncode == 137 or "OutOf memory" in o or "Killed" in o,
             "peak_rss_gb": round(peak_hwm[0] / 1e6, 2)}
    res["arms"].append(entry); save()
    log(f"{cap}: completed={entry['completed']} tok_s={entry['tok_s']} "
        f"oom={entry['oom']} peakRSS={entry['peak_rss_gb']}GB")

log("ALL_DONE_NET105")
print(json.dumps(res["arms"], indent=1), flush=True)

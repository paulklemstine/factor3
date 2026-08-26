#!/bin/bash
# NET-105R v4 — MOE HOT-SET under ENFORCED user-scope caps.
# Inner bash polls until its cgroup's memory.max appears AND matches the
# requested cap (systemd migrates the process asynchronously), then execs.
set -u
BIN=/home/raver1975/f3cache/llama.cpp/build/bin/llama-completion
M30=/home/raver1975/f3cache/gguf30b/Qwen3-30B-A3B-IQ4_XS.gguf
LOG=/tmp/net105rv2.log
CTX=2048; NGEN=128; THREADS=8

log(){ echo "$(date +%H:%M:%S) $*" >> "$LOG"; }

for CAP in 6G 8G 16G_placebo; do
  MEM="${CAP%_placebo}"
  OUT="/tmp/net105rv2_${CAP}.out"
  log "=== cap $CAP ==="

  systemd-run --user --scope \
    -p "MemoryMax=$MEM" -p "MemorySwapMax=0" \
    --setenv=LLAMABIN="$BIN" --setenv=M30FILE="$M30" \
    --setenv=CTXX="$CTX" --setenv=NGENN="$NGEN" --setenv=THREADSS="$THREADS" \
    --setenv=MEMREQ="$MEM" \
    bash -c '
      ok=""
      for i in $(seq 1 40); do
        CGPATH=$(sed "s|0::||" /proc/self/cgroup)
        MAXREAD=$(cat "${CGPATH}/memory.max" 2>/dev/null || echo UNREADABLE)
        if [ "$MAXREAD" = "$MEMREQ" ]; then ok=yes; break; fi
        sleep 0.25
      done
      if [ -z "$ok" ]; then
        echo "FATAL never enforced (last cgpath=$CGPATH max=$MAXREAD req=$MEMREQ)"
        exit 43
      fi
      echo "ASSERT enforced cgpath=$CGPATH max=$MAXREAD"
      exec "$LLAMABIN" -m "$M30FILE" -c "$CTXX" -n "$NGENN" -t "$THREADSS" \
           -p "The history of computing begins with"
    ' > "$OUT" 2>&1
  RC=$?

  TOKS=$(grep -oE "[0-9.]+ tokens per second" "$OUT" | tail -1)
  RUNS=$(grep -oE "/\s+[0-9]+ runs" "$OUT" | tail -1 | grep -oE "[0-9]+" | tail -1)
  OOMC=$(grep -ciE "out of memory|killed|segfault" "$OUT")
  ASSERT=$(grep "^ASSERT" "$OUT" | tail -1)
  log "cap=$CAP rc=$RC runs=${RUNS:-0} tok_s=[$TOKS] oom_or_segfault=$OOMC out_bytes=$(wc -c < "$OUT")"
  [ -n "$ASSERT" ] && log "  $ASSERT"
done
log "ALL_DONE_NET105RV2"

/* exp509_ma1_sieve.c (v2, wheel-30) — round-47 exp 509 MA1-EFFECTIVE
 *
 * Exact pi(x; m, a) for every reduced class a mod m, one segmented-sieve pass.
 *
 * v2 kernel: wheel-30. Only numbers coprime to 30 are represented (density
 * 8/30); primes 2,3,5 are never marked (seeded into counts globally); each
 * remaining prime p >= 7 marks via its 8 residue chains mod 30p — every chain
 * is an arithmetic progression with CONSTANT step 8p in slot space.
 *
 * Checkpoints x = 2^k may fall inside a segment: detected during the survivor
 * scan. Every flush produces a DELTA (counters zeroed at flush) tagged with a
 * cutoff position (2^k mid-scan, or the thread's chunk end for its tail).
 * The merge sorts all flush events by cutoff and sweeps ascending, emitting a
 * cumulative row at every 2^k — provably includes every interval exactly once.
 *
 * Correctness notes:
 *  - chain starts are >= max(p*p, lo), so primes survive; p=2,3,5 excluded
 *    from marking by construction;
 *  - number 1 is masked at segment 0;
 *  - primes < R=286440 satisfy p % R == p, so clsmap handles small primes
 *    naturally (e.g. 11 | R maps to class -1 for m=11); seeds add p<=7;
 *  - uint32 counters safe: per-thread per-residue max ~1e5 << 2^32.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

#define SEGEXP 24
#define SEGLEN (1ULL << SEGEXP)
#define WHEEL 30
#define NRES 8
#define MAXCP 24
#define NMOD 19
#define R 286440ULL
#define MAXPHI 60   /* phi(105)=48 largest here; headroom */

static const uint64_t MODS[NMOD] = {
    3, 4, 5, 7, 8, 11, 31,                       /* design-set core      */
    6, 10, 14, 15, 21, 22, 33, 35, 55, 77, 93,   /* pair moduli | R      */
    105                                          /* one triple product   */
};

static const uint32_t RES[NRES] = {1, 7, 11, 13, 17, 19, 23, 29};
static int RIDX[30];                 /* residue -> chain index or -1 */
static uint32_t QPFX[31];            /* QPFX[r] = #allowed residues <= r */

static int8_t *clsmap[NMOD];         /* clsmap[j][r]: class index or -1 */
static uint32_t *base_primes;
static uint8_t *inv30_tab;           /* p^{-1} mod 30, per base prime */
static uint32_t n_base;
static uint64_t g_maxslots;

static uint64_t gcd_u64(uint64_t a, uint64_t b) {
    while (b) { uint64_t w = a % b; a = b; b = w; }
    return a;
}

/* count of wheel-allowed numbers <= n. QPFX[r] = #{allowed < r}, so add 1
   when r itself is allowed. (The missing "+1" here truncated every segment
   whose hi-1 landed on an allowed residue, dropping its top primes.) */
static inline uint64_t incl_allowed(uint64_t n) {
    uint64_t r = n % WHEEL;
    return 8ULL * (n / WHEEL) + QPFX[r] + (uint64_t)(RIDX[r] >= 0 ? 1 : 0);
}

static void build_tables(void) {
    int acc = 0;
    for (int r = 0; r < 30; r++) {
        RIDX[r] = -1;
        QPFX[r] = (uint32_t)acc;
        int c = -1;
        for (int cc = 0; cc < NRES; cc++) if (RES[cc] == (uint32_t)r) c = cc;
        if (c >= 0) RIDX[r] = c;
        if (RIDX[r] >= 0) acc++;
    }
    QPFX[30] = (uint32_t)acc;
}

static void build_clsmaps(void) {
    for (int j = 0; j < NMOD; j++) {
        clsmap[j] = malloc(R);
        uint64_t m = MODS[j];
        int idx_of[512];
        for (int i = 0; i < 512; i++) idx_of[i] = -1;
        for (uint64_t a = 1; a < m; a++)
            if (gcd_u64(a, m) == 1) idx_of[a] = 0;
        int nc = 0;
        for (uint64_t a = 1; a < m; a++)
            if (gcd_u64(a, m) == 1) idx_of[a] = nc++;
        for (uint64_t r = 0; r < R; r++) {
            uint64_t a = r % m;
            clsmap[j][r] = (a < 512 && idx_of[a] >= 0)
                           ? (int8_t)idx_of[a] : (int8_t)-1;
        }
    }
}

static void build_base_primes(uint64_t lim) {
    uint8_t *comp = calloc(lim + 1, 1);
    base_primes = malloc(sizeof(uint32_t) * (lim / 4 + 64));
    inv30_tab = malloc(lim / 4 + 64);
    n_base = 0;
    for (uint64_t i = 2; i * i <= lim; i++)
        if (!comp[i])
            for (uint64_t j = i * i; j <= lim; j += i) comp[j] = 1;
    for (uint64_t i = 7; i <= lim; i++) {          /* skip 2,3,5: wheel */
        if (!comp[i]) {
            uint64_t t = i % WHEEL, inv = 1;
            for (uint64_t u = 1; u < WHEEL; u++)
                if ((t * u) % WHEEL == 1) { inv = u; break; }
            inv30_tab[n_base] = (uint8_t)inv;
            base_primes[n_base++] = (uint32_t)i;
        }
    }
    free(comp);
}

static inline void aggregate(const uint32_t *cnt, uint64_t dst[NMOD][MAXPHI]) {
    for (int j = 0; j < NMOD; j++)
        memset(dst[j], 0, sizeof(dst[j]));
    for (uint64_t r = 0; r < R; r++) {
        uint32_t c = cnt[r];
        if (!c) continue;
        for (int j = 0; j < NMOD; j++) {
            int8_t a = clsmap[j][r];
            if (a >= 0) dst[j][(int)a] += c;
        }
    }
}

typedef struct {
    uint64_t lo, hi;      /* number range of segment */
    uint64_t g0;          /* group of first allowed >= lo */
    int j0;               /* chain index of first allowed >= lo */
    uint64_t nslots;
} SegGeo;

static inline void seg_geo(uint64_t s, SegGeo *g) {
    g->lo = s << SEGEXP;
    g->hi = g->lo + SEGLEN;
    uint64_t r = g->lo % WHEEL;
    if (RIDX[r] >= 0) { g->j0 = RIDX[r]; g->g0 = g->lo / WHEEL; }
    else {
        int c = 0;
        while (c < NRES && RES[c] < r) c++;
        if (c < NRES) { g->j0 = c; g->g0 = g->lo / WHEEL; }
        else          { g->j0 = 0; g->g0 = g->lo / WHEEL + 1; }
    }
    g->nslots = incl_allowed(g->hi - 1) - incl_allowed(g->lo) +
                (RIDX[g->lo % WHEEL] >= 0 ? 1 : 0);
}

/* local slot of allowed n >= g->lo. Plain subtraction: for n in the same
   30-group as the segment's first allowed number, RIDX[n%30] >= g->j0 by
   minimality of j0; later groups carry >= NRES slack. The previous
   "(x + NRES) % NRES" wrap here was WRONG (slot collisions/mislabels). */
static inline uint64_t slot_of(uint64_t n, const SegGeo *g) {
    return (n / WHEEL - g->g0) * NRES + (uint64_t)(RIDX[n % WHEEL] - g->j0);
}

/* flush events for the global sweep */
typedef struct { uint64_t cutoff; int t, q; } Flush;

static int flush_cmp(const void *A, const void *B) {
    const Flush *a = A, *b = B;
    if (a->cutoff != b->cutoff) return a->cutoff < b->cutoff ? -1 : 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <topexp> <outfile>\n", argv[0]);
        return 2;
    }
    int topexp = atoi(argv[1]);
    const char *outpath = argv[2];
    if (topexp > 40 || topexp < SEGEXP) {
        fprintf(stderr, "need SEGEXP<=topexp<=40\n"); return 2;
    }

    build_tables();
    build_clsmaps();
    build_base_primes(1ULL << ((topexp + 1) / 2));

    const int max_cp = topexp - SEGEXP + 1;
    const int nseg = (int)(1ULL << topexp >> SEGEXP);
    /* max allowed-count per segment: ceil(SEGLEN*8/30) + phase slack */
    g_maxslots = SEGLEN * NRES / WHEEL + NRES + 8;

    int T = 1;
#ifdef _OPENMP
#pragma omp parallel
#pragma omp master
    T = omp_get_num_threads();
#endif
    if (T > 16) T = 16;
    if (T > nseg) T = nseg;

    typedef uint64_t (*ContribT)[NMOD][MAXPHI];
    ContribT *contrib = calloc(T, sizeof(ContribT));
    uint64_t *cutoff_own[MAXCP + 2];
    for (int t = 0; t < T; t++) cutoff_own[t] = calloc(max_cp + 2, sizeof(uint64_t));
    int *ncp_own = calloc(T, sizeof(int));
    uint64_t base = nseg / T;
    int rem = nseg % T;

    double wt0 = (double)time(NULL);

#ifdef _OPENMP
#pragma omp parallel num_threads(T)
#endif
    {
#ifdef _OPENMP
        int tid = omp_get_thread_num();
#else
        int tid = 0;
#endif
        long long s0 = (long long)tid * base + (tid < rem ? tid : rem);
        long long s1 = s0 + (long long)base + (tid < rem ? 1 : 0);
        uint8_t *arr = malloc(g_maxslots);
        uint32_t *cnt = calloc(R, sizeof(uint32_t));
        contrib[tid] = calloc(max_cp + 2, sizeof(**contrib));
        int owned = 0;
        long long my_lo = s0 << SEGEXP, my_hi = s1 << SEGEXP;
        uint64_t cps[MAXCP]; int ncps = 0;
        for (int k = SEGEXP; k <= topexp; k++) {
            uint64_t v = 1ULL << k;
            if (my_lo < v && v <= my_hi) cps[ncps++] = v;
        }
        int cp_next = 0;

        for (long long s = s0; s < s1; s++) {
            SegGeo geo;
            seg_geo((uint64_t)s, &geo);
            memset(arr, 0, geo.nslots);
            if (geo.lo == 0) arr[slot_of(1, &geo)] = 1;      /* mask 1 */
            for (uint32_t bi = 0; bi < n_base; bi++) {
                uint64_t p = base_primes[bi];
                uint64_t pp = p * p;
                if (pp >= geo.hi) break;                     /* primes ascend */
                uint64_t B = pp > geo.lo ? pp : geo.lo;
                uint64_t P = WHEEL * p;
                uint64_t inv30 = inv30_tab[bi];
                for (int c = 0; c < NRES; c++) {
                    uint64_t n_c = p * ((RES[c] * inv30) % WHEEL);
                    uint64_t nst;
                    if (B <= n_c) nst = n_c;
                    else nst = n_c + ((B - n_c + P - 1) / P) * P;
                    if (nst >= geo.hi) continue;
                    size_t idx = (size_t)slot_of(nst, &geo);
                    size_t stp = (size_t)(NRES * p);
                    size_t lim = geo.nslots;
                    if (stp >= 32) {
                        size_t ahead = 4 * stp;
                        size_t i = idx;
                        for (; i + ahead < lim; i += stp) {
                            __builtin_prefetch(arr + i + ahead, 1, 3);
                            arr[i] = 1;
                        }
                        for (; i < lim; i += stp) arr[i] = 1;
                    } else {
                        for (; idx < lim; idx += stp) arr[idx] = 1;
                    }
                }
            }
            /* scan survivors, flushing deltas at internal checkpoints */
            uint64_t next_cp = (cp_next < ncps) ? cps[cp_next] : ~0ULL;
            for (uint64_t sl = 0; sl < geo.nslots; sl++) {
                if (arr[sl]) continue;
                uint64_t qq = sl + (uint64_t)geo.j0;
                uint64_t pnum = WHEEL * (geo.g0 + qq / NRES) + RES[qq % NRES];
                if (pnum >= next_cp) {
                    aggregate(cnt, contrib[tid][owned]);
                    memset(cnt, 0, R * sizeof(uint32_t));
                    cutoff_own[tid][owned++] = next_cp;
                    cp_next++;
                    next_cp = (cp_next < ncps) ? cps[cp_next] : ~0ULL;
                }
                cnt[pnum % R]++;
            }
        }
        /* tail flush closes the chunk (may be empty) */
        aggregate(cnt, contrib[tid][owned]);
        cutoff_own[tid][owned++] = (uint64_t)s1 << SEGEXP;
        ncp_own[tid] = owned;
        free(arr); free(cnt);
    }

    /* ---- merge: sweep all flush events by cutoff, emit rows at 2^k ---- */
    Flush *fl = malloc(sizeof(Flush) * (size_t)T * (max_cp + 2));
    int nfl = 0;
    for (int t = 0; t < T; t++)
        for (int q = 0; q < ncp_own[t]; q++) {
            fl[nfl].cutoff = cutoff_own[t][q];
            fl[nfl].t = t; fl[nfl].q = q; nfl++;
        }
    qsort(fl, (size_t)nfl, sizeof(Flush), flush_cmp);

    FILE *f = fopen(outpath, "w");
    fprintf(f, "META topexp=%d nthreads=%d nmod=%d R=%llu\n",
            topexp, T, NMOD, (unsigned long long)R);
    static uint64_t running[NMOD][MAXPHI];
    memset(running, 0, sizeof(running));
    /* seed p in {2,3,5}: the only primes absent from the wheel-30 grid.
       Class index = index of value (sp mod m) among coprime classes. */
    for (int j = 0; j < NMOD; j++) {
        uint64_t m = MODS[j];
        static const int SEEDP[3] = {2, 3, 5};   /* wheel-missing primes */
    for (int spi = 0; spi < 3; spi++) {
        const int sp = SEEDP[spi];
            if (gcd_u64((uint64_t)sp, m) != 1) continue;
            int idx = 0;
            for (uint64_t a = 1; a < m; a++) {
                if (gcd_u64(a, m) != 1) continue;
                if (a == (uint64_t)sp % m) break;
                idx++;
            }
            running[j][idx] += 1;
        }
    }
    int ptr = 0;
    for (int k = SEGEXP; k <= topexp; k++) {
        uint64_t xk = 1ULL << k;
        while (ptr < nfl && fl[ptr].cutoff <= xk) {
            for (int j = 0; j < NMOD; j++)
                for (int a = 0; a < MAXPHI; a++)
                    running[j][a] += contrib[fl[ptr].t][fl[ptr].q][j][a];
            ptr++;
        }
        uint64_t sum31 = 0;
        for (int a = 0; a < MAXPHI; a++) sum31 += running[6][a];
        fprintf(f, "CP %d sum_m31=%llu\n", k, (unsigned long long)sum31);
        for (int j = 0; j < NMOD; j++) {
            uint64_t m = MODS[j];
            int nc = 0;
            for (uint64_t a = 1; a < m; a++)
                if (gcd_u64(a, m) == 1) nc++;
            fprintf(f, "C %d %llu", k, (unsigned long long)m);
            for (int a = 0; a < nc; a++)
                fprintf(f, " %llu", (unsigned long long)running[j][a]);
            fprintf(f, "\n");
        }
    }
    /* integrity: every flush consumed */
    fprintf(f, "FLUSHES total=%d consumed=%d\n", nfl, ptr);
    fprintf(f, "TIME wall_seconds=%.1f\n", (double)time(NULL) - wt0);
    fclose(f);
    fprintf(stderr, "done: topexp=%d wall=%.1fs flushes=%d/%d\n",
            topexp, (double)time(NULL) - wt0, ptr, nfl);
    return 0;
}

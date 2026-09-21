
"""usage: compare.py old.npz new.npz out.json"""
import sys, json, numpy as np
SIGN_INVARIANT = {"data_nu"}  # PCA scores (graphtools data_nu): component signs are not defined
a, b = np.load(sys.argv[1]), np.load(sys.argv[2])
res = {}
for k in sorted(set(a.files) | set(b.files)):
    if k not in a.files or k not in b.files:
        res[k] = {"present_in_both": False}; continue
    x, y = a[k], b[k]
    same_shape = x.shape == y.shape
    row = {"present_in_both": True, "shape_old": list(x.shape), "shape_new": list(y.shape), "shape_equal": same_shape}
    if same_shape:
        d = np.abs(x - y)
        row.update({"max_abs_diff": float(d.max()), "mean_abs_diff": float(d.mean()),
                    "allclose_rtol1e-5_atol1e-8": bool(np.allclose(x, y, rtol=1e-5, atol=1e-8)),
                    "array_equal": bool(np.array_equal(x, y))})
        if k in SIGN_INVARIANT:
            # PCA scores: per-component sign is arbitrary; align signs before judging
            s = np.sign((x * y).sum(0)); s[s == 0] = 1
            ys = y * s
            row.update({"sign_flipped_components": int((s < 0).sum()),
                        "max_abs_diff_sign_aligned": float(np.abs(x - ys).max()),
                        "allclose_sign_aligned": bool(np.allclose(x, ys, rtol=1e-5, atol=1e-8)),
                        "array_equal_sign_aligned": bool(np.array_equal(x, ys))})
            row["allclose_rtol1e-5_atol1e-8"] = row["allclose_sign_aligned"]
            row["array_equal"] = row["array_equal_sign_aligned"]
    res[k] = row
rows = [r for r in res.values() if r.get("present_in_both")]
if all(r.get("shape_equal") and r.get("array_equal") for r in rows) and len(rows) == len(res):
    verdict = "identical"
elif all(r.get("shape_equal") and r.get("allclose_rtol1e-5_atol1e-8") for r in rows) and len(rows) == len(res):
    verdict = "allclose"
else:
    verdict = "changed"
out = {"old": sys.argv[1], "new": sys.argv[2], "verdict": verdict, "quantities": res}
json.dump(out, open(sys.argv[3], "w"), indent=1)
print(json.dumps(out, indent=1))

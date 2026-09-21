
"""usage: run_snapshot.py <label> <paul15.h5> <snapdir> [t]   (t default "auto"; t="auto" is NOT deterministic in magic 3.0.0, use a fixed int for differential tests)"""
import sys, json, time, platform, importlib
import numpy as np, h5py
label, h5path, snapdir = sys.argv[1:4]
t_arg = sys.argv[4] if len(sys.argv) > 4 else "auto"
t_arg = int(t_arg) if t_arg != "auto" else t_arg
with h5py.File(h5path, "r") as f:
    X = f["data.debatched"][()]           # (genes, cells) as in scanpy.datasets.paul15
    genes = f["data.debatched_rownames"][()].astype(str)
X = np.ascontiguousarray(X.T, dtype=np.float64)     # (cells, genes)
X = X[:1000]                                          # deterministic subsample: first 1000 cells
import magic
t0 = time.time()
op = magic.MAGIC(knn=5, n_pca=50, t=t_arg, random_state=0, n_jobs=8, verbose=0)
X_magic = op.fit_transform(X, genes="all_genes")
elapsed = time.time() - t0
X_magic = np.asarray(X_magic, dtype=np.float64)
kernel = op.graph.kernel
kernel = kernel.toarray() if hasattr(kernel, "toarray") else np.asarray(kernel)
diff_op = op.diff_op
diff_op = diff_op.toarray() if hasattr(diff_op, "toarray") else np.asarray(diff_op)
data_nu = np.asarray(op.graph.data_nu)
np.savez_compressed(f"{snapdir}/{label}_paul15.npz", X_input=X, X_magic=X_magic,
                    kernel=kernel, diff_op=diff_op, data_nu=data_nu)
def ver(m):
    try:
        return importlib.import_module(m).__version__
    except Exception as e:
        return f"ERR:{e}"
meta = {"label": label, "python": platform.python_version(),
        "versions": {m: ver(m) for m in ["magic","numpy","scipy","sklearn","pandas","matplotlib","graphtools","scprep","tasklogger","pygsp","h5py"]},
        "dataset": "paul15.h5 data.debatched, first 1000 cells, all genes",
        "params": {"knn":5,"n_pca":50,"t":t_arg,"random_state":0,"n_jobs":8},
        "t_selected": int(op._check_params() or 0) if False else None,
        "shapes": {"X_input": list(X.shape), "X_magic": list(X_magic.shape), "kernel": list(kernel.shape),
                   "diff_op": list(diff_op.shape), "data_nu": list(data_nu.shape)},
        "elapsed_s": round(elapsed, 2)}
try:
    meta["t_selected"] = int(op.t) if isinstance(op.t, (int, np.integer)) else str(op.t)
    meta["t_opt"] = None if getattr(op, "_t_opt", None) is None else int(op._t_opt)  # not all versions expose this
except Exception as e:
    meta["t_note"] = str(e)
json.dump(meta, open(f"{snapdir}/{label}_meta.json", "w"), indent=1)
print(json.dumps(meta, indent=1))

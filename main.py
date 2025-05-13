from model.scge_model import build_model
import pandas as pd

def save_results(m):
	Y_df = m["Y"].records
	Y = dict(zip(Y_df["region"], Y_df["level"]))
	K_df = m["K"].records
	K = dict(zip(K_df["region"], K_df["level"]))
	U = m["U"].records["level"].iloc[0]
	Z = m["Z"].records["level"].iloc[0]
	
	df = pd.DataFrame({"region": list(Y.keys()),"Y": list(Y.values()),"K": list(K.values())})
	
	df.to_csv("results/outputs.csv", index=False)
	pd.DataFrame([{"U": U, "Z": Z}]).to_csv("results/summary.csv", index=False)


def main():
    m, model = build_model()
    model.toGams("results/scge.gms")
    model.solve()
    solve_status = model.solve_status
    print("Solve status:", solve_status)
    save_results(m)
    
if __name__ == "__main__":
    main()

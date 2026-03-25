import pandas as pd

# Import your logic function
# Make sure analyze_logic is defined somewhere accessible
from your_logic_file import analyze_logic   # <-- CHANGE THIS


def run_batch():
    try:
        print("Reading samples.csv...")
        df = pd.read_csv("samples.csv")

        print("Columns found:", df.columns.tolist())

        # Auto-handle column order safely
        if len(df.columns) < 3:
            raise ValueError("samples.csv must have at least 3 columns")

        id_col = df.columns[0]
        context_col = df.columns[1]
        code_col = df.columns[2]

        results = []

        for _, row in df.iterrows():
            bug_id = row[id_col]
            context = row[context_col]
            code = row[code_col]

            print(f"Processing ID: {bug_id}")

            try:
                bug_line, explanation = analyze_logic(context, code)
            except Exception as e:
                bug_line = None
                explanation = f"Error during analysis: {str(e)}"

            results.append({
                "ID": bug_id,
                "Bug Line": bug_line,
                "Explanation": explanation
            })

        output_df = pd.DataFrame(results)
        output_df.to_csv("output.csv", index=False)

        print("✅ output.csv generated successfully!")

    except Exception as e:
        print("❌ Batch execution failed:", str(e))


if __name__ == "__main__":
    run_batch()
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("Dataseti është bosh – kontrollo burimin e të dhënave.")

    return df


def compute_univariate_summary(df: pd.DataFrame, output_dir: str) -> None:
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    summary = df[numeric_cols].describe().T
    summary.to_csv(os.path.join(output_dir, "summary_statistics_numeric.csv"))


def compute_country_summary(df: pd.DataFrame, output_dir: str) -> None:
    required_cols = [
        "country",
        "teaching",
        "research",
        "citations",
        "cwur_score",
        "num_students",
        "international_students",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        present = [c for c in required_cols if c in df.columns]
    else:
        present = required_cols

    if "country" not in present:
        return

    value_cols = [c for c in present if c != "country"]
    country_summary = (
        df.groupby("country")[value_cols].agg(["mean", "median", "min", "max", "count"])
    )
    country_summary.to_csv(
        os.path.join(output_dir, "country_summary_after_outlier_removal.csv")
    )


def plot_distributions(df: pd.DataFrame, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    key_cols = [
        "teaching",
        "research",
        "citations",
        "cwur_score",
        "num_students",
        "student_staff_ratio",
    ]
    cols = [c for c in key_cols if c in df.columns]

    for col in cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribucioni i {col}")
        plt.xlabel(col)
        plt.ylabel("Frekuenca")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"hist_{col}.png"), dpi=300)
        plt.close()

        plt.figure(figsize=(6, 5))
        sns.boxplot(x=df[col].dropna())
        plt.title(f"Boxplot për {col}")
        plt.xlabel(col)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"boxplot_{col}.png"), dpi=300)
        plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: str) -> None:
    candidate_cols = [
        "teaching",
        "research",
        "citations",
        "cwur_score",
        "rank_gap",
        "research_efficiency_per_1k",
        "faculty_efficiency",
        "global_influence_index",
        "relative_teaching",
        "relative_citations",
        "relative_cwur_score",
        "num_students",
        "student_staff_ratio",
    ]

    cols = [c for c in candidate_cols if c in df.columns]
    if len(cols) < 2:
        return

    corr = df[cols].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Matrica e Korrelacioneve (Metrika Kryesore)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_heatmap_core_features.png"), dpi=300)
    plt.close()


def plot_pairwise_relationships(df: pd.DataFrame, output_dir: str) -> None:
    pair_cols = [
        "teaching",
        "research",
        "citations",
        "cwur_score",
        "relative_teaching",
        "relative_citations",
    ]
    cols = [c for c in pair_cols if c in df.columns]
    if len(cols) < 3:
        return

    sns.pairplot(df[cols].dropna(), corner=True, diag_kind="kde")
    plt.suptitle(
        "Marrëdhëniet mes metrikave kryesore (pairplot)",
        y=1.02,
        fontsize=14,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pairplot_core_metrics.png"), dpi=300)
    plt.close()


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "10th_step-removal-incorr-findings", "final_dataset_no_outliers.csv")
    output_dir = base_dir

    print("Ngarkimi i datasetit final pa outliers...")
    df = load_data(data_path)
    print(f"Rreshta: {len(df)}, Kolona: {len(df.columns)}")

    print("Llogaritja e statistikave përmbledhëse (univariate)...")
    compute_univariate_summary(df, output_dir)

    print("Llogaritja e statistikave sipas shtetit...")
    compute_country_summary(df, output_dir)

    print("Krijimi i histogramëve dhe boxplot-eve për metrikat kryesore...")
    plot_distributions(df, output_dir)

    print("Krijimi i heatmap të korrelacioneve...")
    plot_correlation_heatmap(df, output_dir)

    print("Krijimi i pairplot për metrikat kryesore...")
    plot_pairwise_relationships(df, output_dir)

    print("Analiza eksploruese (statistika përmbledhëse + multivariante) u përfundua me sukses.")


if __name__ == "__main__":
    main()





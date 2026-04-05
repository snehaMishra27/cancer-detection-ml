import argparse
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DEFAULT_FEATURES = ["Age", "Number of sexual partners", "Smokes", "STDs", "Dx"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a reproducible model.pkl for the Flask API.")
    parser.add_argument("--data", required=True, help="Path to a CSV dataset file.")
    parser.add_argument("--target", required=True, help="Target column name (0/1).")
    parser.add_argument(
        "--features",
        nargs="+",
        default=DEFAULT_FEATURES,
        help=f"Feature column names. Default: {DEFAULT_FEATURES}",
    )
    parser.add_argument("--out", default="model.pkl", help="Output path for joblib model (default: model.pkl).")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split size (default: 0.2).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42).")
    parser.add_argument(
        "--class-weight",
        default="none",
        choices=["none", "balanced"],
        help="Class weighting strategy. Use 'balanced' for severe imbalance, otherwise 'none'.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.data)

    missing_cols = [c for c in (args.features + [args.target]) if c not in df.columns]
    if missing_cols:
        raise SystemExit(f"Missing columns in CSV: {missing_cols}\nAvailable columns: {list(df.columns)}")

    X = df[args.features]
    y = df[args.target]

    # Numeric preprocessing: impute + standardize.
    numeric_features = list(X.columns)
    pre = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            )
        ],
        remainder="drop",
    )

    class_weight = None if args.class_weight == "none" else "balanced"
    clf = LogisticRegression(max_iter=2000, class_weight=class_weight, random_state=args.seed)

    model = Pipeline(
        steps=[
            ("preprocess", pre),
            ("clf", clf),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print("Confusion matrix:")
    print(confusion_matrix(y_test, pred))
    print("\nClassification report:")
    print(classification_report(y_test, pred, digits=4))

    if hasattr(model, "predict_proba"):
        p1 = model.predict_proba(X_test)[:, 1]
        try:
            print("ROC AUC:", roc_auc_score(y_test, p1))
        except Exception as e:
            print("ROC AUC unavailable:", e)

    joblib.dump(model, args.out)
    print(f"\nSaved model to: {args.out}")


if __name__ == "__main__":
    main()



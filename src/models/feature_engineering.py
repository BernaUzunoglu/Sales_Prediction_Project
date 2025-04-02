import pandas as pd

def create_features(X_raw: pd.DataFrame, ts_data: pd.DataFrame) -> pd.DataFrame:
    X = X_raw.copy()
    features = []

    for _, row in X.iterrows():
        pid = row["product_id"]
        target_date = pd.Timestamp(year=int(row["year"]), month=int(row["month"]), day=int(row["day"]))

        history = ts_data[(ts_data["product_id"] == pid) & (ts_data["order_date"] < target_date)].copy()
        history = history.sort_values("order_date")

        expected_cols = [
            "product_id", "year", "month", "day", "dayofweek", "dayofyear"
        ] + [f"lag_{i}" for i in range(1, 15)] + [
            "moving_avg_7", "moving_avg_14", "exp_moving_avg_7",
            "cumulative_sales", "avg_sales_per_day"
        ]

        if history.empty:
            # Eğer geçmiş veri yoksa: tüm feature'lar sıfır
            f = {col: 0 for col in expected_cols}
            f["product_id"] = pid
            f["year"] = row["year"]
            f["month"] = row["month"]
            f["day"] = row["day"]
            f["dayofweek"] = target_date.dayofweek
            f["dayofyear"] = target_date.dayofyear
        else:
            history["quantity"] = history["quantity"].fillna(0)
            for lag in range(1, 15):
                history[f"lag_{lag}"] = history["quantity"].shift(lag).fillna(0)

            history["moving_avg_7"] = history["quantity"].rolling(window=7).mean().fillna(0)
            history["moving_avg_14"] = history["quantity"].rolling(window=14).mean().fillna(0)
            history["exp_moving_avg_7"] = history["quantity"].ewm(span=7, adjust=False).mean()
            history["cumulative_sales"] = history["quantity"].cumsum()
            history["avg_sales_per_day"] = history["cumulative_sales"] / (history.index + 1)

            last = history.iloc[-1]
            f = {
                "product_id": pid,
                "year": row["year"],
                "month": row["month"],
                "day": row["day"],
                "dayofweek": target_date.dayofweek,
                "dayofyear": target_date.dayofyear,
                **{f"lag_{l}": last.get(f"lag_{l}", 0) for l in range(1, 15)},
                "moving_avg_7": last.get("moving_avg_7", 0),
                "moving_avg_14": last.get("moving_avg_14", 0),
                "exp_moving_avg_7": last.get("exp_moving_avg_7", 0),
                "cumulative_sales": last.get("cumulative_sales", 0),
                "avg_sales_per_day": last.get("avg_sales_per_day", 0)
            }

        features.append(f)

    df_features = pd.DataFrame(features)
    return df_features

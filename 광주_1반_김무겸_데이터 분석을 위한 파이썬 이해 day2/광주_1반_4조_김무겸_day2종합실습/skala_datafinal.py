# # NYC Yellow Taxi (2026-05) — total_amount 금액 정합성 검증 프로젝트
# 1. 데이터 준비 (Pandas vs Polars, 결측치/중복 처리, 기본 EDA)
# 2. 시각화 (diff 정의, 계산총액 vs total_amount, 벤더별 불일치, 불일치 샘플의 벤더별 diff)
# 3. 통계 분석 (불일치 데이터 상관계수 → 검정 우선순위 → t-test)
# 4. ML Pipeline (전처리 + 모델, 평가지표, joblib 저장)
# 5. report.md 자동 생성


# 1. 데이터 준비

import gc                    
import os                      
import time                    
import pandas as pd
import polars as pl
import numpy as np
from scipy import stats        # t-test 등 통계검정
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 깨짐 방지 설정 (그래프 제목/축 레이블에 한글 사용)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False
pd.set_option("display.max_columns", 30)

# 어느 디렉토리에서 실행하든 이 스크립트 파일 위치를 기준으로 데이터 파일을 찾도록 절대경로로 구성
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "yellow_tripdata_2026-05.parquet")


# ## 1.1 Pandas vs Polars 로딩 비교

# 동일한 parquet 파일을 pandas와 polars 양쪽으로 로딩하여
# 로딩 속도 / 메모리 사용량 / shape을 비교함
t0 = time.perf_counter()
df_pd = pd.read_parquet(DATA_PATH)
t_pd = time.perf_counter() - t0
mem_pd = df_pd.memory_usage(deep=True).sum() / 1024**2  # MB 단위

t0 = time.perf_counter()
df_pl = pl.read_parquet(DATA_PATH)
t_pl = time.perf_counter() - t0
mem_pl = df_pl.estimated_size() / 1024**2  # MB 단위

print(f"[pandas] 로딩시간={t_pd:.3f}초, 메모리={mem_pd:.1f}MB, shape={df_pd.shape}")
print(f"[polars] 로딩시간={t_pl:.3f}초, 메모리={mem_pl:.1f}MB, shape={df_pl.shape}")
print(f"-> polars가 pandas 대비 {t_pd / t_pl:.2f}배 빠르고, 메모리는 {mem_pd / mem_pl:.2f}배 적게 사용")


# 컬럼별 dtype 비교 (pandas vs polars가 같은 컬럼을 어떤 타입으로 해석하는지 확인)
dtype_compare = pd.DataFrame({
    "pandas_dtype": df_pd.dtypes.astype(str),
    "polars_dtype": [str(df_pl.schema[c]) for c in df_pd.columns],
})
print(dtype_compare)


# 비교가 끝났으므로 polars 데이터프레임은 메모리에서 해제 (이후 분석은 pandas로 통일)
del df_pl
gc.collect()

# ## 1.2 결측치 / 중복 처리

# 컬럼별 결측치 개수 및 비율 확인
n_rows = len(df_pd)
missing = df_pd.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)
missing_pct = (missing / n_rows * 100).round(2)
print(pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct}))

# 완전 중복 행 확인 및 제거
dup_count = df_pd.duplicated().sum()
print(f"완전 중복 행: {dup_count:,}건 ({dup_count / n_rows * 100:.3f}%)")

df_clean = df_pd.drop_duplicates()
del df_pd
gc.collect()
print("중복 제거 후 shape:", df_clean.shape)

# 결측치 처리
# - RatecodeID: 결측을 임의로 특정 요금코드로 단정할 수 없으므로 'Unknown' 문자열로 표시
# - store_and_fwd_flag: 결측은 'Unknown' 카테고리로 대체
# - congestion_surcharge / Airport_fee / cbd_congestion_fee: 금액 컬럼이므로 결측은
#   '부과되지 않음(0)'으로 간주하고 0으로 대체
#   (주의: 이 fillna(0) 처리 덕분에 2장부터의 diff 계산에서 별도로 fillna를 또 하지 않아도 됨)
# - passenger_count: 임의로 채우지 않고 결측 그대로 유지 (분석 시 필요하면 그때 제외)
df_clean["RatecodeID"] = df_clean["RatecodeID"].apply(
    lambda x: str(int(x)) if pd.notna(x) else "Unknown"
)
df_clean["store_and_fwd_flag"] = df_clean["store_and_fwd_flag"].fillna("Unknown")
for col in ["congestion_surcharge", "Airport_fee", "cbd_congestion_fee"]:
    df_clean[col] = df_clean[col].fillna(0)

remaining_missing = df_clean.isna().sum()
remaining_missing = remaining_missing[remaining_missing > 0]
print("처리 후 남은 결측 컬럼:", remaining_missing.index.tolist() if len(remaining_missing) else "없음")

# ## 1.3 기본 EDA

# 데이터 기간 및 규모 확인
print(f"분석 대상 행 수(중복제거 후): {len(df_clean):,}")
print(f"기간: {df_clean['tpep_pickup_datetime'].min()} ~ {df_clean['tpep_pickup_datetime'].max()}")


# 논리적 이상치 스캔 (음수 요금, 0거리, 시각 역전 등)
checks = {
    "fare_amount < 0": (df_clean["fare_amount"] < 0).sum(),
    "total_amount < 0": (df_clean["total_amount"] < 0).sum(),
    "trip_distance == 0": (df_clean["trip_distance"] == 0).sum(),
    "trip_distance > 100마일": (df_clean["trip_distance"] > 100).sum(),
    "하차시각 <= 승차시각": (df_clean["tpep_dropoff_datetime"] <= df_clean["tpep_pickup_datetime"]).sum(),
    "passenger_count == 0": (df_clean["passenger_count"] == 0).sum(),
}
for k, v in checks.items():
    print(f"{k}: {v:,}건 ({v/len(df_clean)*100:.3f}%)")

# 주요 수치형 컬럼 기술통계 (평균, 표준편차, 분위수 등)
num_cols = ["trip_distance", "fare_amount", "tip_amount", "total_amount", "passenger_count"]
print(df_clean[num_cols].describe().round(2))

# 범주형 분포 확인: 결제수단(payment_type), 벤더(VendorID)
# payment_type 공식 코드: 1=신용카드,2=현금,3=No charge,4=Dispute,5=Unknown,6=Voided trip
# (0은 공식 문서에 없는 비표준 코드 -> 3장 통계분석에서 원인 규명)
print(df_clean["payment_type"].value_counts(normalize=True).mul(100).round(2).rename("pct"))
print(df_clean["VendorID"].value_counts(normalize=True).mul(100).round(2).rename("pct"))

# ---
# # 2. 시각화
# 먼저 diff(불일치 금액) 계산식을 정의하고, 이를 기준으로 3가지 시각화를 진행함: (1) 계산된 총액과 total_amount 비교, (2) 벤더별 불일치 건수, (3) 불일치 샘플에 한정한 벤더별 diff 분포.

# ## 2.0 diff 계산식 정의
# `total_amount`가 세부 요금 항목(fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, congestion_surcharge, Airport_fee, cbd_congestion_fee)의 합과 일치하는지 확인하기 위한 diff 컬럼을 정의함.

# total_amount와 비교할 세부 요금 항목 정의
FEE_COMPONENTS = [
    "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "congestion_surcharge", "Airport_fee", "cbd_congestion_fee",
]

# 세부 항목의 합(계산된 총액)을 별도 컬럼으로 계산
df_clean["calc_total"] = df_clean[FEE_COMPONENTS].sum(axis=1)

# diff = 실제 청구총액 - 계산된 총액 (0이면 완전 일치, 0이 아니면 불일치)
df_clean["diff"] = (df_clean["total_amount"] - df_clean["calc_total"]).round(2)

# 불일치 여부를 이진 플래그로도 만들어둠 (이후 시각화/ML에서 재사용)
df_clean["is_mismatch"] = df_clean["diff"].abs() > 0.01

mismatch_count = int(df_clean["is_mismatch"].sum())
print(f"전체 {len(df_clean):,}건 중 불일치 {mismatch_count:,}건 "
      f"({mismatch_count / len(df_clean) * 100:.2f}%)")


# ## 2.1 계산된 총액(calc_total) vs 실제 청구총액(total_amount) 비교
# 전체 4백만 건을 그대로 산점도로 그리면 점이 겹쳐 보이지 않으므로, 2만 건을 무작위 샘플링해서 시각화함. 대각선(y=x)에 가까울수록 두 값이 일치하는 트립임.

# 산점도가 겹쳐 보이지 않도록 2만 건 무작위 샘플링 (재현성을 위해 random_state 고정)
sample_for_scatter = df_clean[["calc_total", "total_amount", "is_mismatch"]].sample(
    n=20_000, random_state=42
)

plt.figure(figsize=(7, 7))
sns.scatterplot(
    data=sample_for_scatter, x="calc_total", y="total_amount",
    hue="is_mismatch", alpha=0.4, s=15,
    palette={False: "steelblue", True: "crimson"},
)
# y=x 기준선: 이 선 위에 있으면 계산총액과 청구총액이 정확히 일치
lim = [0, sample_for_scatter[["calc_total", "total_amount"]].quantile(0.99).max()]
plt.plot(lim, lim, color="black", linestyle="--", linewidth=1, label="y = x (완전 일치선)")

plt.xlim(lim)
plt.ylim(lim)
plt.title("계산된 총액(calc_total) vs 실제 청구총액(total_amount) 비교 (2만 건 샘플)")
plt.xlabel("calc_total (세부 항목 합계, $)")
plt.ylabel("total_amount (실제 청구총액, $)")
plt.legend(title="불일치 여부")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "calc_total_vs_total_amount.png"), dpi=150)
print("차트 저장 완료: calc_total_vs_total_amount.png")
plt.close()

del sample_for_scatter
gc.collect()


# ## 2.2 벤더별 금액 불일치 건수 (Plotly 인터랙티브)
# 마우스를 올리면 벤더별 전체건수·불일치건수·불일치율을 확인할 수 있는 인터랙티브 바차트.

import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"  # 노트북 환경에서 인라인으로 렌더링되도록 설정

# 벤더별 전체건수 / 불일치건수 / 불일치율 집계
vendor_stats = df_clean.groupby("VendorID").agg(
    전체건수=("diff", "size"),
    불일치건수=("is_mismatch", "sum"),
).reset_index()
vendor_stats["불일치율(%)"] = (vendor_stats["불일치건수"] / vendor_stats["전체건수"] * 100).round(2)

fig = px.bar(
    vendor_stats, x="VendorID", y="불일치건수",
    hover_data=["전체건수", "불일치율(%)"],
    title="벤더별 금액 불일치 건수 (Plotly 인터랙티브)",
    color="불일치율(%)", color_continuous_scale="Reds",
    text="불일치건수",
    labels={"VendorID": "벤더 ID", "불일치건수": "불일치 건수"},
)
fig.update_layout(xaxis_type="category")

# 인터랙티브 HTML 파일로 저장 (브라우저에서 열어 마우스오버로 확인)
fig.write_html(os.path.join(SCRIPT_DIR, "vendor_mismatch_interactive.html"), include_plotlyjs="cdn")
print("Plotly 인터랙티브 차트 저장 완료: vendor_mismatch_interactive.html")

print(vendor_stats)

# ## 2.3 불일치 샘플에 한정한 벤더별 diff 분포 (Seaborn)
# diff가 0이 아닌(=불일치) 트립만 모아서, 벤더별로 diff 값이 어떻게 분포하는지 확인함. 극단치 영향을 줄이기 위해 -6~6달러로 클리핑함.

# 불일치 샘플만 필터링
df_mismatch = df_clean[df_clean["is_mismatch"]].copy()

plot_df = df_mismatch[["VendorID", "diff"]].copy()
plot_df["diff_clipped"] = plot_df["diff"].clip(-6, 6)

plt.figure(figsize=(9, 5))
sns.violinplot(data=plot_df, x="VendorID", y="diff_clipped", order=sorted(df_clean["VendorID"].unique()))
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.title("불일치 샘플의 벤더별 diff 분포 (Seaborn violinplot, -6~6달러 클리핑)")
plt.xlabel("VendorID")
plt.ylabel("diff ($)")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "vendor_diff_distribution.png"), dpi=150)
print("차트 저장 완료: vendor_diff_distribution.png")
plt.close()

del plot_df
gc.collect()


# ---
# # 3. 통계 분석
# diff가 0이 아닌(금액 불일치) 데이터만 모아 상관계수를 먼저 계산하고, 그 결과로 검정 우선순위를 정한 뒤 순서대로 t-test를 진행함.

# ## 3.1 불일치 데이터 상관계수 분석
# 요금 구성요소(혼잡료 2종, extra)와 벤더/결제타입 더미변수를 만들어, 각각이 diff와 얼마나 상관관계를 갖는지 확인함. (더미변수는 0/1 값이라 연속형인 diff와의 상관계수는 point-biserial 상관계수와 동일한 의미를 가짐)

# 검정 후보 변수들을 이진(0/1) 플래그로 생성 (df_mismatch 기준)
df_mismatch["has_congestion"] = (df_mismatch["congestion_surcharge"] > 0).astype(int)
df_mismatch["has_cbd_fee"] = (df_mismatch["cbd_congestion_fee"] > 0).astype(int)
df_mismatch["has_extra"] = (df_mismatch["extra"] > 0).astype(int)
df_mismatch["is_vendor1"] = (df_mismatch["VendorID"] == 1).astype(int)
df_mismatch["is_vendor2"] = (df_mismatch["VendorID"] == 2).astype(int)
df_mismatch["is_vendor6"] = (df_mismatch["VendorID"] == 6).astype(int)
df_mismatch["is_vendor7"] = (df_mismatch["VendorID"] == 7).astype(int)
df_mismatch["is_payment0"] = (df_mismatch["payment_type"] == 0).astype(int)

candidate_cols = ["has_congestion", "has_cbd_fee", "has_extra",
                  "is_vendor1", "is_vendor2", "is_vendor6", "is_vendor7", "is_payment0"]

# diff와 각 후보 변수 간 상관계수 계산
corr_with_diff = df_mismatch[["diff"] + candidate_cols].corr()["diff"].drop("diff")
corr_with_diff = corr_with_diff.sort_values(key=lambda s: s.abs(), ascending=False)
corr_with_diff_df = corr_with_diff.round(4).reset_index()
corr_with_diff_df.columns = ["변수", "diff와의 상관계수"]
print(corr_with_diff_df)


# 상관계수 히트맵으로 시각화 (자기상관 포함 전체 후보 변수 간 관계도 함께 확인)
plt.figure(figsize=(8, 6))
sns.heatmap(
    df_mismatch[["diff"] + candidate_cols].corr().round(2),
    annot=True, fmt=".2f", cmap="coolwarm", center=0,
)
plt.title("불일치 데이터 내 diff와 후보 변수들 간 상관계수 히트맵")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "diff_correlation_heatmap.png"), dpi=150)
print("차트 저장 완료: diff_correlation_heatmap.png")
plt.close()


# ## 3.2 검정 우선순위 설정
# 위 상관계수의 절댓값이 큰 순서대로 검정 우선순위를 정함. 상관계수가 클수록 그 변수가 diff(불일치 금액)를 더 잘 설명한다고 볼 수 있으므로, 먼저 검정할 가치가 크다고 판단함.

# 상관계수 절댓값 기준 우선순위 목록 출력
priority_order = corr_with_diff.index.tolist()
print("검정 우선순위 (상관계수 절댓값 큰 순):")
for rank, col in enumerate(priority_order, start=1):
    print(f"{rank}. {col} (상관계수={corr_with_diff[col]:.4f})")


# ## 3.3 우선순위대로 t-test 진행
# 각 후보 변수(플래그=1 집단 vs 플래그=0 집단)에 대해 diff 평균 차이를 Welch's t-test로 검정함. 등분산을 가정하지 않고, p-value와 함께 효과크기(Cohen's d)도 같이 해석함 (표본이 매우 커서 p-value는 항상 유의하게 나오므로 효과크기로 실질적 크기를 판단).

# Cohen's d 계산 함수 (효과크기)
def cohens_d(a, b):
    na, nb = len(a), len(b)
    pooled_std = np.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    return (a.mean() - b.mean()) / pooled_std

# 우선순위 순서대로 t-test 반복 수행, 결과를 표로 정리
ttest_results = []
for col in priority_order:
    group1 = df_mismatch.loc[df_mismatch[col] == 1, "diff"]
    group0 = df_mismatch.loc[df_mismatch[col] == 0, "diff"]

    t_stat, p_val = stats.ttest_ind(group1, group0, equal_var=False)
    d_val = cohens_d(group1, group0)

    ttest_results.append({
        "변수": col,
        "상관계수": round(corr_with_diff[col], 4),
        "flag=1 평균diff": round(group1.mean(), 3),
        "flag=0 평균diff": round(group0.mean(), 3),
        "t통계량": round(t_stat, 3),
        "p-value": f"{p_val:.3g}",
        "Cohen's d": round(d_val, 4),
    })

ttest_results_df = pd.DataFrame(ttest_results)
print(ttest_results_df)


# 3.4 t-test 결과 해석 (p-value + 효과크기)
# 표본이 매우 커서 p-value는 항상 유의하게(≈0) 나오므로, 실질적 해석은 Cohen's d(효과크기)를 기준으로 함.

VAR_DESC = {
    "has_extra": "extra(추가요금) 부과 여부",
    "is_payment0": "payment_type=0(미기록) 여부",
    "has_congestion": "congestion_surcharge(혼잡통행료) 부과 여부",
    "is_vendor1": "VendorID=1(벤더1)",
    "is_vendor2": "VendorID=2(벤더2)",
    "is_vendor6": "VendorID=6(벤더6)",
    "has_cbd_fee": "cbd_congestion_fee(CBD혼잡료) 부과 여부",
    "is_vendor7": "VendorID=7(벤더7)",
}

def effect_size_label(d):
    ad = abs(d)
    if ad < 0.2:
        return "무시할 수준"
    elif ad < 0.5:
        return "작은"
    elif ad < 0.8:
        return "중간"
    return "큰"

# 각 변수별로 p-value 유의성 판정 + 효과크기 판정을 실제 텍스트로 생성
interp_lines = ["### t-test 결과 해석 (p-value + 효과크기)"]
for _, row in ttest_results_df.iterrows():
    var = row["변수"]
    p_val = float(row["p-value"])
    d_val = row["Cohen's d"]
    sig = "유의함 (p < 0.05)" if p_val < 0.05 else "유의하지 않음 (p >= 0.05)"
    size_label = effect_size_label(d_val)
    direction = "낮추는" if d_val < 0 else "높이는"
    interp_lines.append(
        f"- **{VAR_DESC.get(var, var)}**: p-value={p_val:.3g} -> 통계적으로 {sig}, "
        f"효과크기는 {size_label} 수준(Cohen's d={d_val:.3f}). "
        f"flag=1 집단(평균 diff={row['flag=1 평균diff']})이 flag=0 집단(평균 diff={row['flag=0 평균diff']}) "
        f"대비 diff를 {direction} 방향으로 작용함."
    )

top_var = ttest_results_df.loc[ttest_results_df["Cohen's d"].abs().idxmax(), "변수"]
interp_lines.append(
    f"\n표본 크기가 수십만 건에 달해 모든 변수의 p-value가 사실상 0에 가까우므로, "
    f"통계적 유의성보다 Cohen's d로 실질적 크기를 판단해야 함. "
    f"효과크기가 가장 큰 변수는 **{VAR_DESC.get(top_var, top_var)}**로, 금액 불일치(diff)의 핵심 원인으로 해석됨."
)

interp_text = "\n".join(interp_lines)
print(interp_text)

# ---
# # 4. ML Pipeline
# `sklearn.pipeline.Pipeline`으로 전처리(원핫인코딩+스케일링)와 분류 모델을 하나로 묶어, 이후에도 같은 형식의 새로운 데이터가 들어왔을 때 간편하게 재사용할 수 있는 파이프라인을 만듦. 타겟은 `is_mismatch`(금액 불일치 여부, 이진)로 설정함.

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib

# 모델 입력용 시간 파생 컬럼 생성 (승차 시각의 시간대)
df_clean["pickup_hour"] = df_clean["tpep_pickup_datetime"].dt.hour

# 범주형 / 수치형 피처와 타겟 정의
feature_cols_cat = ["VendorID", "payment_type"]
feature_cols_num = ["trip_distance", "fare_amount", "pickup_hour"]
target_col = "is_mismatch"

# 전체 409만 건은 학습에 오래 걸리므로, 속도/메모리 확보를 위해 30만 건을 무작위 샘플링
# (불일치 비율이 원본과 거의 동일하게 유지되도록 단순 무작위 추출)
sample_df = df_clean[feature_cols_cat + feature_cols_num + [target_col]].dropna().sample(
    n=300_000, random_state=42
)
X = sample_df[feature_cols_cat + feature_cols_num]
y = sample_df[target_col].astype(int)

# 학습/평가 데이터 분리 (클래스 비율 유지를 위해 stratify 사용)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("train shape:", X_train.shape, "| test shape:", X_test.shape)
print(f"불일치 비율 - train: {y_train.mean():.3f}, test: {y_test.mean():.3f}")

del sample_df
gc.collect()


# 4.1 Pipeline 구성 (전처리 + 모델)
# `ColumnTransformer`로 범주형(OneHotEncoder)과 수치형(StandardScaler) 전처리를 정의하고, `Pipeline`으로 분류 모델(LogisticRegression)과 하나로 묶음.

# 범주형은 원핫인코딩, 수치형은 표준화(스케일링)
preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), feature_cols_cat),
    ("num", StandardScaler(), feature_cols_num),
])

# 전처리 + 모델을 하나의 Pipeline 객체로 구성
# -> 이후 같은 형식의 새 데이터가 들어와도 pipeline.predict(new_df)만 호출하면
#    전처리부터 예측까지 동일한 방식으로 자동 처리됨
pipeline = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("clf", LogisticRegression(max_iter=1000)),
])

pipeline.fit(X_train, y_train)
print("Pipeline 학습 완료")


# 4.2 평가 지표 출력

# 테스트셋에 대한 예측 및 평가지표 계산
y_pred = pipeline.predict(X_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy  = {acc:.4f}")
print(f"Precision = {prec:.4f}")
print(f"Recall    = {rec:.4f}")
print(f"F1-score  = {f1:.4f}")
print()
print("Confusion Matrix (행=실제, 열=예측):")
print(confusion_matrix(y_test, y_pred))
print()
print(classification_report(y_test, y_pred, target_names=["일치", "불일치"]))


# ## 4.3 모델 저장 (joblib) 및 재사용 예시
# 학습된 Pipeline 전체(전처리+모델)를 joblib으로 저장함. 이후 같은 형식의 새 parquet 데이터가 들어와도, 저장된 파일을 불러와 `pipeline.predict()`만 호출하면 바로 예측 가능함.

# 학습된 Pipeline(전처리+모델) 전체를 하나의 파일로 저장
MODEL_PATH = os.path.join(SCRIPT_DIR, "mismatch_prediction_pipeline.joblib")
joblib.dump(pipeline, MODEL_PATH)
print(f"모델 저장 완료: {MODEL_PATH}")

''' --- 재사용 예시: 저장된 파이프라인을 다시 불러와 새로운 데이터에 바로 적용 ---
loaded_pipeline = joblib.load(MODEL_PATH)
sample_new_data = X_test.head(5)  # 실제로는 여기에 새로 들어온 데이터를 넣으면 됨
sample_pred = loaded_pipeline.predict(sample_new_data)
print("새 데이터 5건에 대한 예측(불일치 여부):", sample_pred)
'''

# ---
# # 5. 자동화: report.md 생성
# 지금까지의 분석 결과(벤더별 불일치 현황, 상관계수 우선순위, t-test 결과, ML 성능)를 모아 `report.md` 파일을 자동 생성함. 맨 앞부분에는 '왜 이 검증이 필요한가'를 먼저 설명해 프로젝트의 중요성을 강조함.

# report.md 내용을 순서대로 쌓기 위한 리스트
report_lines = []

def rlog(s=""):
    report_lines.append(s)

# --- 0. 프로젝트 배경 (왜 이 검증이 필요한가) ---
rlog("# NYC Yellow Taxi (2026-05) 금액 정합성(total_amount) 검증 자동 리포트\n")
rlog("## 0. 이 검증이 왜 필요한가\n")
rlog("- `total_amount`가 이미 존재하더라도, 세부 요금 항목의 합과 일치하는지 검증하지 않으면 "
     "그 값을 신뢰할 근거가 없음 (회계 감사의 기본 원칙과 동일)")
rlog("- **정부 제출/법적 준수**: congestion_surcharge, cbd_congestion_fee는 뉴욕시에 납부해야 "
     "하는 통행료로, 총액에 누락되면 규제 위반 리스크로 이어질 수 있음")
rlog("- **기사 정산의 공정성**: total_amount 기준으로 정산이 이뤄진다면, 항목 누락은 기사 또는 "
     "회사 어느 쪽이든 금전적 손해로 이어질 수 있음")
rlog("- **벤더 신뢰도 관리**: 여러 결제단말 업체(TPEP)의 데이터를 통합 사용할 때, 벤더별 계산 "
     "방식 차이를 모르면 매출·수요 분석이 왜곡됨")
rlog("- **후속 분석의 신뢰성**: 본 데이터셋은 전체의 상당 부분이 불일치 상태이므로, 원인을 "
     "규명하지 않은 채 total_amount를 그대로 쓰면 모든 후속 분석의 신뢰성이 흔들림")
rlog("")

# --- 1. 벤더별 불일치 현황 ---
rlog("## 1. 벤더별 금액 불일치 현황\n")
rlog(vendor_stats.to_markdown(index=False))
rlog("")

# --- 2. 상관계수 기반 검정 우선순위 ---
rlog("## 2. 불일치 데이터 상관계수 기반 검정 우선순위\n")
rlog(corr_with_diff_df.to_markdown(index=False))
rlog("")

# --- 3. t-test 결과 ---
rlog("## 3. 우선순위별 t-test 결과\n")
rlog(ttest_results_df.to_markdown(index=False))
rlog("")
rlog(interp_text)
rlog("")

# --- 4. ML 모델 성능 ---
rlog("## 4. ML 모델(is_mismatch 예측) 성능\n")
rlog(f"- Accuracy = {acc:.4f}")
rlog(f"- Precision = {prec:.4f}")
rlog(f"- Recall = {rec:.4f}")
rlog(f"- F1-score = {f1:.4f}")
rlog("")

# --- 5. 결론 ---
rlog("## 5. 결론\n")
rlog("금액 불일치는 벤더별로 서로 다른 원인(계산 공식 차이, 특정 컬럼의 구조적 미기록, "
     "기존 결측 이슈의 파생 효과)을 가지며, 상관계수 기반으로 설정한 검정 우선순위와 "
     "t-test 결과, 그리고 ML 모델의 예측 성능이 서로 일치하는 결론을 보여줌.")

# report.md 파일로 저장
with open(os.path.join(SCRIPT_DIR, "report.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("report.md 생성 완료")


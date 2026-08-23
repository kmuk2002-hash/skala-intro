#파일 로드
import pandas as pd

df=pd.read_csv("/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv")

#파일 탐색
df.info()
df.describe()
df.shape
df.head

#IQR계산 및 이상치 제거
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3-Q1
lo, hi = Q1-1.5*IQR, Q3+1.5*IQR

df_clean = df[df["amount"].between(lo,hi)]
print(f"제거 전: {len(df)}, 제거 후: {len(df_clean)}\n제거 행 : {len(df)-len(df_clean)}")

#pandas 지역별 통계
pd_result_region = df_clean.groupby("region").agg(
    revenue=('amount','sum'),
    mean = ('amount', 'mean'),
    cnt=('amount','count')
    ).sort_values("revenue", ascending = False)
print(f'groupby 후 데이터 행:{pd_result_region["cnt"].sum()+df_clean["region"].isna().sum()}\nclean 후 데이터 행:{len(df_clean)}')
print(pd_result_region)

#pandas 카테고리별 통계
pd_result_category = df_clean.groupby("category").agg(
    revenue=('amount','sum'),
    mean = ('amount', 'mean'),
    cnt=('amount','count')
    ).sort_values("revenue", ascending = False)
print(f'groupby 후 데이터 행:{pd_result_category["cnt"].sum()+df_clean["category"].isna().sum()}\nclean 후 데이터 행:{len(df_clean)}')
print(pd_result_category)

#3)Polars Lazy API로 동일 집계 작성
import polars as pl

pl_result_region = (
    pl.scan_csv('/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv',schema_overrides={'amount':pl.Float64})
    .filter((pl.col('amount')>lo) & (pl.col('amount')<hi)).group_by('region').agg([pl.col('amount').sum().alias("revenue"),pl.col('amount').mean().alias("mean"),pl.col('amount').count().alias("cnt")])
    .sort('revenue',descending=True).collect()
)

pl_result_category = (
    pl.scan_csv('/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv',schema_overrides={'amount':pl.Float64})
    .filter((pl.col('amount')>lo) & (pl.col('amount')<hi)).group_by('category').agg([pl.col('amount').sum().alias("revenue"),pl.col('amount').mean().alias("mean"),pl.col('amount').count().alias("cnt")])
    .sort('revenue',descending=True).collect()
)

print(pl_result_region)
print(pl_result_category)

#4)DuckDB SQL로 동일 집계 작성

import duckdb

du_result_region = duckdb.sql(f"""
                    SELECT region,
                    SUM(amount) AS revenue,
                    AVG(amount) AS mean,
                    COUNT(*) AS cnt
                    FROM '/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv'
                    WHERE amount BETWEEN {lo} AND {hi}
                    GROUP BY region
                    ORDER BY revenue DESC"""
).df()

du_result_category = duckdb.sql(f"""
                    SELECT category,
                    SUM(amount) AS revenue,
                    AVG(amount) AS mean,
                    COUNT(*) AS cnt
                    FROM '/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv'
                    WHERE amount BETWEEN {lo} AND {hi}
                    GROUP BY category
                    ORDER BY revenue DESC"""
).df()

print(du_result_region)
print(du_result_category)

#세 도구 성능 비교1 pandas는 전처리가 끝난 데이터를 바로써 빠르지만 polars와 duckdb는 파싱과정이 포함되 길게 나옴
t_pandas = %timeit -o df_clean.groupby("region").agg(revenue=('amount','sum'), mean=('amount','mean'), cnt=('amount','count'))

t_polars = %timeit -o (pl.scan_csv("/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv", schema_overrides={'amount': pl.Float64}).filter(pl.col('amount').is_between(lo, hi)).group_by('region').agg([pl.col('amount').sum().alias("revenue"), pl.col('amount').mean().alias("mean"), pl.col('amount').count().alias("cnt")]).sort('revenue', descending=True).collect())

t_duckdb = %timeit -o duckdb.sql(f"""SELECT region, SUM(amount) AS revenue, AVG(amount) AS mean, COUNT(*) AS cnt FROM '{"/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv"}' WHERE amount BETWEEN {lo} AND {hi} AND region IS NOT NULL GROUP BY region ORDER BY revenue DESC""").df()

compare = pd.DataFrame({
    "engine": ["pandas", "polars", "duckdb"],
    "avg_sec": [t_pandas.average, t_polars.average, t_duckdb.average]
})
print(compare)

#세 도구 성능 비교2 공정한 비교를 위해 pandas에도 파싱과정을 포함
t_pandas_full = %timeit -o (pd.read_csv("/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv").pipe(lambda df: df[df['amount'].between(lo, hi)]).groupby("region").agg(revenue=('amount','sum'), mean=('amount','mean'), cnt=('amount','count')))

t_polars = %timeit -o (pl.scan_csv("/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv", schema_overrides={'amount': pl.Float64}).filter(pl.col('amount').is_between(lo, hi)).group_by('region').agg([pl.col('amount').sum().alias("revenue"), pl.col('amount').mean().alias("mean"), pl.col('amount').count().alias("cnt")]).sort('revenue', descending=True).collect())

t_duckdb = %timeit -o duckdb.sql(f"""SELECT region, SUM(amount) AS revenue, AVG(amount) AS mean, COUNT(*) AS cnt FROM '{"/Users/mugyeom/workspace/skala-intro/광주_1반_김무겸_데이터 분석을 위한 파이썬 이해 day2/sales_100k.csv"}' WHERE amount BETWEEN {lo} AND {hi} AND region IS NOT NULL GROUP BY region ORDER BY revenue DESC""").df()

compare = pd.DataFrame({
    "engine": ["pandas", "polars", "duckdb"],
    "avg_sec": [t_pandas_full.average, t_polars.average, t_duckdb.average]
})
print(compare)




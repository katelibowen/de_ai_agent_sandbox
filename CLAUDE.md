# CLAUDE.md

Project context and conventions for Claude Code. Read this before suggesting code or running commands.

## Stack

- **Warehouse:** BigQuery (GCP project: `<your-project-id>`, primary dataset region: `US`)
- **Transformation:** dbt-core 1.8+, profile `prod_warehouse`
- **Orchestration:** Airflow 2.x (Cloud Composer), DAGs in `orchestration/dags/`
- **Streaming ingest:** Pub/Sub → Dataflow → BigQuery (Storage Write API, default stream)
- **Source DBs:** Postgres via Datastream CDC into `raw_cdc.*` datasets
- **BI:** Looker, semantic layer in `models/marts/` exposed via `lkml/`

## Repo layout

```
models/
  staging/        # 1:1 with source tables, light cleanup, prefix stg_
  intermediate/   # reusable joins/transforms, prefix int_, never exposed to BI
  marts/
    core/         # conformed dims and facts, prefix dim_ / fact_
    finance/      # domain marts
    ops/
tests/            # custom generic + singular tests
macros/           # shared SQL macros
seeds/            # reference data, small CSVs only
analyses/         # ad-hoc, never run in prod
```

## Conventions — always follow

- **Grain in the docstring.** Every fact/dim has a `description:` in its YAML stating the grain in one sentence. No grain comment → fail review.
- **Staging models:** `select` with explicit column list, rename to snake_case, cast types, no joins. One source per staging model.
- **Surrogate keys:** `dbt_utils.generate_surrogate_key` only — never `farm_fingerprint` or hand-rolled concatenation.
- **Incremental models:** prefer `incremental_strategy='merge'` with explicit `unique_key` and `merge_update_columns`. Use `insert_overwrite` only for partition-replacement on date-partitioned tables. Never `append` for anything that can have late-arriving data.
- **Partitioning & clustering:** every fact > 10M rows must be partitioned (usually on event_date) and clustered on top 1–2 filter columns.
- **SCD Type 2:** use the `dbt_snapshot` macro pattern in `macros/scd2.sql`, never custom logic.
- **Tests:** every mart model has at minimum `unique` + `not_null` on the grain key, plus `relationships` to its dims.

## Never do

- Don't `select *` in marts or intermediate models.
- Don't write queries without a `where` filter on partitioned tables — flag the cost first.
- Don't add new sources without updating `models/staging/<source>/_sources.yml`.
- Don't create models in `marts/` that join more than 5 tables — break into intermediate first.
- Don't suggest Snowflake-specific syntax (QUALIFY is fine, but no `STREAM`, `TASK`, `MERGE INTO ... WHEN MATCHED ... DELETE`).

## Commands

- `dbt build --select state:modified+ --defer --state ./prod-manifest` — local dev run, only changed models + downstream
- `dbt test --select <model>` — tests for a single model
- `make lint` — runs sqlfluff with our config
- `make cost-check MODEL=<name>` — wraps `dbt compile` + `bq query --dry_run` to estimate bytes scanned

## Cost guardrails

Before suggesting any new full-refresh on a fact > 100GB, surface the dry-run estimate. We've had 4-figure single-query bills from forgotten partition filters; treat this as a real constraint, not a nag.

## Tone for code review

When reviewing a PR or diff: lead with grain/correctness issues, then performance, then style. Skip nitpicks unless asked.

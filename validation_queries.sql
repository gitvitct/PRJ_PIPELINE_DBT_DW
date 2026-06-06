--#######################################################################################################################################################
--#######################################################################################################################################################
--# DATA WAREHOUSE VALIDATION - PRJ_PIPELINE_DBT_DW

--##################################################################################################
--#  ENVIRONMENT CHECK
	
		SELECT NOW();

	-- drop table public.raw_sales ;
	-- drop table public.raw_customers ;
	-- drop view public.stg_sales;
	-- drop view public.stg_customers ;
	-- drop table public.customer_snapshot ;
	-- drop table public.dim_customer ;
	-- drop table public.dim_date ;
	-- drop table public.fact_sales ;
	-- drop table public.sales_summary ;


--##################################################################################################
--#  1. BRONZE LAYER VALIDATION

	--# ----------------------------------------
	--# raw_sales

		--# Data Inspection

				SELECT *
				FROM public.raw_sales
				ORDER BY sale_id;	

		--# Row Count

				SELECT COUNT(*) AS total_rows FROM public.raw_sales;

		--# Null Validation

				SELECT *
				FROM public.raw_sales
				WHERE sale_id IS NULL
				   OR customer_id IS NULL;


				-- Expected: 0 rows


	--# ----------------------------------------
	--# raw_customers

		--# Data Inspection

				SELECT *
				FROM public.raw_customers
				ORDER BY customer_id;

		--# Row Count

				SELECT COUNT(*) AS total_rows
				FROM public.raw_customers;

		--# Duplicate Customers

				SELECT
					customer_id,
					COUNT(*)
				FROM public.raw_customers
				GROUP BY customer_id
				HAVING COUNT(*) > 1;



---

--##################################################################################################
--#  2. SILVER LAYER VALIDATION
	--# ----------------------------------------
	--# stg_sales
		--# Data Inspection

				SELECT *
				FROM public.stg_sales;

		--# Row Count Reconciliation

				SELECT
					(SELECT COUNT(*) FROM raw_sales) raw_count,
					(SELECT COUNT(*) FROM stg_sales) stg_count;

				-- Expected: "raw_count = stg_count"
---
	--# ----------------------------------------
	--# stg_customers
		--# Data Inspection

				SELECT *
				FROM public.stg_customers;

		--# Row Count Reconciliation

				SELECT
					(SELECT COUNT(*) FROM raw_customers) raw_count,
					(SELECT COUNT(*) FROM stg_customers) stg_count;

				-- Expected: "raw_count = stg_count"

--##################################################################################################
--#  3. SNAPSHOT VALIDATION

	--# ----------------------------------------
	--# customer_snapshot

		SELECT *
		FROM public.customer_snapshot
		ORDER BY customer_id, dbt_valid_from;

	--# ----------------------------------------
	--# One Active Version

		SELECT
			customer_id,
			COUNT(*)
		FROM customer_snapshot
		WHERE dbt_valid_to IS NULL
		GROUP BY customer_id
		HAVING COUNT(*) > 1;

		--Expected: 0 rows
---
--##################################################################################################
--#  4. GOLD LAYER VALIDATION

--# -------------------------------------------------------------------------------------
--# dim_customer ------------------------------------------------------------------------

		--# Full Inspection --------------------------

				SELECT *
				FROM public.dim_customer
				ORDER BY customer_id, valid_from;

		--# Row Count --------------------------

				SELECT COUNT(*) AS total_rows
				FROM public.dim_customer;

		--# Only One Current Record--------------------------

				SELECT
					customer_id,
					COUNT(*)
				FROM dim_customer
				WHERE current_flag = TRUE
				GROUP BY customer_id
				HAVING COUNT(*) > 1;

				-- Expected: 0 rows

		--# Current Records --------------------------

				SELECT *
				FROM dim_customer
				WHERE current_flag = TRUE
				ORDER BY customer_id;

			-- Expected:5 rows

--# -------------------------------------------------------------------------------------
--# dim_date ------------------------------------------------------------------------

		--# Full Inspection

				SELECT *
				FROM public.dim_date
				ORDER BY date_key;

		--# Row Count

				SELECT COUNT(*)
				FROM public.dim_date;

				--Expected:5844


		--# Duplicate Dates


				SELECT
					full_date,
					COUNT(*)
				FROM dim_date
				GROUP BY full_date
				HAVING COUNT(*) > 1;

				-- Expected: 0 rows


--# -------------------------------------------------------------------------------------
--#  fact_sales ------------------------------------------------------------------------

		--# Full Inspection

				SELECT *
				FROM public.fact_sales;

		--# Row Count

				SELECT COUNT(*)
				FROM public.fact_sales;


--##################################################################################################
--# 5. FACT TABLE VALIDATION

	--# Customer Dimension Relationship ------------------------------------------------------------------------

			SELECT *
			FROM fact_sales f
			LEFT JOIN dim_customer c
				   ON f.customer_sk = c.customer_sk
			WHERE c.customer_sk IS NULL;

			-- Expected: 0 rows


	--# Date Dimension Relationship ------------------------------------------------------------------------

			SELECT *
			FROM fact_sales f
			LEFT JOIN dim_date d
				   ON f.date_key = d.date_key
			WHERE d.date_key IS NULL;

			-- Expected: 0 rows


	--# Measure Validation ------------------------------------------------------------------------

		--# Revenue

				SELECT
					SUM(total_amount) AS total_revenue
				FROM fact_sales;

		--# Sales Quantity

				SELECT
					COUNT(*) AS total_sales
				FROM fact_sales;

---
--##################################################################################################
--#  6. RECONCILIATION TESTS

	--# Raw Sales vs Fact Sales -------------------------------

			SELECT
				COUNT(*) raw_sales
			FROM raw_sales;

			SELECT
				SUM(total_sales)
			FROM fact_sales;

			--Expected: Same business volume


	--# Snapshot vs Dimension -------------------------------

			SELECT
				(SELECT COUNT(*) FROM customer_snapshot) snapshot_rows,
				(SELECT COUNT(*) FROM dim_customer) dimension_rows;


			-- Expected: Same SCD2 history

---
--##################################################################################################
--#  7. DATA QUALITY TESTS

	--# Null Business Keys ------------------------------------------------

			SELECT *
			FROM fact_sales
			WHERE customer_sk IS NULL
			   OR date_key IS NULL;

			-- Expected: 0 rows

	--# Negative Amounts ------------------------------------------------

			SELECT *
			FROM fact_sales
			WHERE total_amount < 0;

			-- Expected: 0 rows

	--# Duplicate Facts ------------------------------------------------

			SELECT
				customer_sk,
				date_key,
				COUNT(*)
			FROM fact_sales
			GROUP BY customer_sk, date_key
			HAVING COUNT(*) > 1;

			-- Expected: 0 rows


--##################################################################################################
--# 8. BUSINESS VALIDATION

	--# Revenue by Day ------------------------------------------------

			SELECT
				d.full_date,
				SUM(f.total_amount) revenue
			FROM fact_sales f
			JOIN dim_date d
			  ON f.date_key = d.date_key
			GROUP BY d.full_date
			ORDER BY d.full_date;


	--# Top Customers ------------------------------------------------

			SELECT
				c.customer_name,
				SUM(f.total_amount) total_revenue
			FROM fact_sales f
			JOIN dim_customer c
			  ON f.customer_sk = c.customer_sk
			WHERE c.current_flag = TRUE
			GROUP BY c.customer_name
			ORDER BY total_revenue DESC;

---

--##################################################################################################
--#  VALIDATION STATUS

PASS Criteria:

	✓ No duplicate current customers
	✓ No orphan facts
	✓ No NULL business keys
	✓ No duplicate dates
	✓ SCD2 working correctly
	✓ Raw → Staging reconciliation
	✓ Snapshot → Dimension reconciliation
	✓ Fact → Dimension referential integrity
	✓ Revenue totals consistent




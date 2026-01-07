.PHONY: deploy-warehouse check-env

check-env:
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "❌ DATABASE_URL is not set"; \
		exit 1; \
	fi

deploy-warehouse: check-env
	@echo "🚀 Deploying warehouse schema..."
	psql "$$DATABASE_URL" -f warehouse/db/deploy.sql
	@echo "✅ Warehouse schema deployed"

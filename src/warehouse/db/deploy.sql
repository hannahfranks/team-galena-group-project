\echo 'Creating schemas...'
\i warehouse/db/schemas.sql

\echo 'Creating dimension tables...'
\i warehouse/db/dim_tables.sql

\echo 'Creating fact tables...'
\i warehouse/db/fact_tables.sql

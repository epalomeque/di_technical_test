# Create dayli charges view
DROP_DAYLI_CHARGES_VIEW = """DROP VIEW IF EXISTS DAYLI_CHARGES;"""

SQL_DAYLI_CHARGES_VIEW = """
CREATE VIEW DAYLI_CHARGES AS 
SELECT data_charges.id, data_companies.company_name, data_charges.amount, data_charges.status, data_charges.created_at, data_charges.updated_at
FROM data_charges
INNER JOIN data_companies ON data_companies.id=data_charges.company_id
WHERE status in ('charged_back');
"""
# Data Engineering Project - Team Galena

In this group project, we created a data platform to **Extract** data from an operational database into a data lake, **Transform** the data into a star schema, and **Load** the remodelled it into a data warehouse hosted in AWS, allowing highly efficient **OLAP**. 

## Pipeline Overview 
🌊 **Ingestion - Data Lake** 
- AWS Ingestion Lambda 
- Triggered every 15 minutes using CloudWatch logs and EventBridge schedule
- Retrieves db credentials from AWS Secrets Manager using boto3
- Creates connection with PostgreSQL db using pg8000
- Extracts tables and writes to S3 ingestion bucket with timestamped file names

🪄 **Transformation** 
- AWS Transformation Lambda invoked by each ingestion 
- Loads most recently ingested tables using timestamps lookup file 
- Wrangles and cleans data, then transforms into star schema
- Writes transformed tables to S3 transformation bucket with timestamped file names

⭐️ **Data Warehouse - Star Schema**
- AWS Warehouse Lambda triggered with each transformation
- Loads most recently transformed dimension and fact tables
- Writes new data to RDS PostgreSQL Data Warehouse

📊 **Data Analysis** 
- Visualisations in BI Tableau
- Summary statistics and trends in the data

## Dataset 
🔸 **DB name:** totesys<br>
🔸 **Description:** PostgreSQL db hosted in RDS, updated several times a day 

## Project Structure
```bash
team-galena-group-project/
│
├── .github/			        # CI/CD GitHub Actions
└── └── ci.yml
│
├── infrastructure/			    # IaC using Terraform
│   ├── build/
│   ├── config.tf
│   ├── eventbridge.tf
│   ├── iam.tf
│   ├── lambda.tf
│   └── s3.tf
│  
├── src/			            # data processing pipeline
│   └── ingestion/
│      └── ingest.py            # ingestion script holding lambda handler
│   └── transformation/
│       ├── utils/              # table parser and save parquet to s3 utils
│       ├── dim_counterparty.py
│       ├── dim_currency.py
│       ├── dim_date.py
│       ├── dim_design.py
│       ├── dim_location.py
│       └── dim_staff.py
│       ├── lambda_handler.py  # transformation lambda handler
│       └── transformer.py     # transformer script to create dimensions and facts
│   └── warehouse/
│
├── tests/			            # unit tests following TDD
│   └── unit/
│
├── venv/	
├── .gitignore
├── README.md
└── requirements.txt   
```

## How to Run the Project

**1. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # on Linux/macOS
venv\Scripts\activate      # on Windows

export PYTHONPATH=$(pwd)   # Set project root
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```
**3. Create an AWS IAM user and configure credentials in terminal**

- Store Access Key ID and Secret Access Key in .aws/credentials:
```bash
[default]
aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key = <your secret access key>
```

**4. Create Secret for db credentials in AWS Secrets Manager**
- Secret name: totesys/rds/credentials

**5. Create necessary S3 buckets in AWS Console**
- galena-remote-state-backend
- galena-s3-ingestion-lambda-bucket
- galena-s3-transformation-lambda-bucket
- s3-ingestion-bucket-team-galena
- s3-transformation-bucket-team-galena

**6. Initialise, plan, and apply Terraform**
```bash
terraform init
terraform plan
terraform apply
```

## Contributors
💻 @hannahfranks<br>
💻 @J4M1N<br>
💻 @shohag1610<br>
💻 @leonie-vs<br>




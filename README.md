# 🧹 aws-finops-automator

An automated cloud cost optimization pipeline that combines **Infrastructure as Code (Terraform)** and **Python automation scripting (Boto3)** to detect, audit, and remediate resource sprawl and financial leakage in an AWS environment.

This project simulates real-world production environments locally via **LocalStack** to replicate automated lifecycle management without incurring live infrastructure charges.

---

## 🏗️ System Architecture

The infrastructure footprint deployed by this workflow consists of the following modular components:

* **Custom VPC Network:** Abstracted networking topology scaling a private `10.20.0.0/16` CIDR boundary.
* **High Availability Subnets:** Public subnets distributed dynamically across multiple mock Availability Zones (`us-east-1a` and `us-east-1b`) to ensure fault tolerance.
* **Compute Tier:** Dual `t3.micro` EC2 instances provisioned uniformly across the public subnets to act as the web application host layer.
* **Storage Vault:** Object-oriented AWS S3 bucket configured with active file versioning and a 30-day automated non-current lifecycle expiration rule for log retention.
* **Target Telemetry Asset:** An unattached 10 GB `gp3` EBS Block Storage Volume intentionally left orphaned to test the FinOps detection engine.

---

## 🛠️ Design Decisions & Architectural Pushbacks

### 1. Structural Modularity (Terraform Modules)
To prevent a "flat-file anti-pattern," all core network resources (VPC, Subnets, and Gateways) were decoupled into a reusable child module (`./modules/network`). This enforces an enterprise-grade directory structure, isolating critical networking baselines from individual application tiers.

### 2. Architectural Security Pushback (The Port 22 Trap)
The project baseline requirement called for exposing Port 22 (SSH) globally to `0.0.0.0/0`.
* **Deviation & Risk Mitigation:** While a default variable parameter was exposed to allow compliant automation runs, this configuration has been heavily flagged in the codebase metadata as a high-severity risk. In a live enterprise production configuration, this entry would be locked down to explicit corporate proxy gateways or a client VPN CIDR block.

---

## 🚀 Local Execution Guide

### Prerequisites
* Docker / Docker Desktop installed and running
* Python 3.12+
* Terraform binary installed on the system path

### 1. Initialize the Mock Cloud Environment
1. Ensure your terminal is at the project root folder and activate the Python virtual environment:
```bash
source .venv/bin/activate
```
### 2. Launch LocalStack (Free Tier v4.4.0)
Run the clean, open-source version of LocalStack inside Docker in the foreground. Wait until the terminal logs explicitly display Ready.:
```Bash
sudo docker run --rm -p 4566:4566 --name localstack localstack/localstack:4.4.0
```
### 3. Deploy the Mock Infrastructure
Open a second terminal window (ensure .venv is activated), navigate to the terraform/ directory, and apply the infrastructure code:
```Bash
cd terraform
tflocal apply -auto-approve
```
### 4. Run the Cost Janitor Automation Script
Navigate back to the project root directory and execute the automation script to discover orphans and generate report.json:
```Bash
cd ..
python janitor/janitor.py
```

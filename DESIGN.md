
## 1. Multi-Cloud Expansion Strategy (AWS to GCP/Azure)

To scale the Cost Janitor tool seamlessly to GCP and Azure without breaking or rewriting core orchestration logic, the tool's architecture must be refactored into a **Decoupled Factory Pattern** using abstract base classes.


       [ Core Orchestration Engine ]
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
   [AWS Adapter] [GCP Adapter] [Azure Adapter]
         │          │          │
    (Boto3 API) (GCP Cloud) (Azure Resource)

---

## 2. IAM Permissions & Minimal Policy
The script follows the rule of least privilege[cite: 107]:
* **`--dry-run` Mode:** Needs Read-Only access to scan and view resource metadata.
* **`--delete` Mode:** Needs active Delete/Mutation permissions to remove orphaned resources.

### Minimal Read-Only IAM Policy (JSON) 

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "JanitorReadOnly",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes",
        "ec2:DescribeInstances",
        "ec2:DescribeAddresses",
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    }
  ]
}

## 3. Safety Guardrails (Outage Prevention)
To prevent the script from accidentally crashing NimbusKart's production system, we add two strict safety nets:

* **Time Buffer for Race Conditions:** A newly unattached EBS volume might just be restarting or scaling down. The script will only flag/delete a volume if it has been in the `available` state for more than **24 hours**.
* **Blast Radius Circuit Breaker:** If a CI/CD error accidentally removes tags from all servers, a naive script would delete everything. Our script will automatically shut down and alert a human if it detects that it is about to delete more than **15% of total company resources** at once.

---

## 4. Observability & Alerting for FinOps
We publish these core metrics to our monitoring dashboard so the team knows the Janitor is working properly:

* **Metric 1: `JanitorExecutionSuccess`** * *Source:* Script Execution Logs 
  * *Alert Threshold:* `< 1` (Fires a critical alert if the daily script crashes or fails to run).
* **Metric 2: `BlastRadiusBreached`** * *Source:* Script Exceptions 
  * *Alert Threshold:* `> 0` (Alerts instantly if the 15% safety breaker is tripped).
* **Metric 3: `MonthlyWastePurgedUSD`** * *Source:* `report.json` 
  * *Alert Threshold:* No Alert (Purely for tracking total money saved on the dashboard).

---

## 5. What We Did Not Build 
We consciously excluded the following features to keep the initial local version simple and stable:

* **Live AWS Pricing API Integration:** We used fixed static pricing constants inside `constants.py` to ensure the script works offline on LocalStack without needing real AWS credentials.

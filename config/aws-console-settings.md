# AWS console settings used (no Terraform, everything was set up in the console)

Region: eu-north-1 (Stockholm)

| Resource | Settings |
|---|---|
| Launch template `ecobuy-template` | Amazon Linux 2023 (x86), t3.micro, no key pair, user data = `app/user-data.sh`, tag `Project = EcoBuy` on instances |
| Security group `ecobuy-web-sg` | Inbound: HTTP port 80 from anywhere. No SSH |
| Target group `ecobuy-tg` | Instances, HTTP port 80, health check path `/health` |
| Load balancer `ecobuy-alb` | Application, internet-facing, default VPC, two availability zones (eu-north-1a and 1b), listener HTTP 80 forwarding to `ecobuy-tg` |
| Auto Scaling Group `ecobuy-asg` | Launch template `ecobuy-template`, both zones, attached to `ecobuy-tg`, ELB health checks on, desired 2, minimum 2, maximum 5, group metrics collection on |
| Scaling policy `ecobuy-cpu-70` | Target tracking, average CPU utilization, target 70, 300 second warm-up, scale-in enabled |

CloudWatch created two alarms for the policy: `AlarmHigh` (CPU above 70 for 3 readings) and `AlarmLow` (CPU below 49 for 15 readings).

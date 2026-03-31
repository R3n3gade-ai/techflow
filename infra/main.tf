# achelion_arms/infra/main.tf
# Achelion ARMS: "The Fortress" Infrastructure Configuration
# Using Terraform for Infrastructure as Code (IaC)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- 1. Networking (VPC) ---
# A secure, private VPC with public and private subnets.
# Zero direct internet access to the Master Engine.
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr             = "10.0.0.0/16"
  public_subnets       = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets      = ["10.0.10.0/24", "10.0.11.0/24"]
  enable_nat_gateway   = true
}

# --- 2. State Management (RDS PostgreSQL) ---
# Holds the immutable audit_log, portfolio_snapshots, and mc_pmi_history.
module "rds" {
  source = "./modules/rds"
  
  vpc_id              = module.vpc.vpc_id
  private_subnets     = module.vpc.private_subnets
  instance_class      = "db.t4g.small"
  allocated_storage   = 20
  db_name             = "arms_fortress"
}

# --- 3. High-Speed Cache (ElastiCache Redis) ---
# Crucial for SYS-1 (Circuit Breakers) and SYS-5 (Correlation Monitor).
module "redis" {
  source = "./modules/redis"
  
  vpc_id              = module.vpc.vpc_id
  private_subnets     = module.vpc.private_subnets
  node_type           = "cache.t4g.micro"
  num_cache_nodes     = 1
}

# --- 4. Container Orchestration (ECS Fargate) ---
# The Master Engine (L4-L6) runs as a containerized service.
module "ecs" {
  source = "./modules/ecs"
  
  vpc_id              = module.vpc.vpc_id
  private_subnets     = module.vpc.private_subnets
  cluster_name        = "arms-cluster"
  container_image     = "achelion/arms-master:latest"
  cpu                 = 512
  memory              = 1024
}

# --- 5. Security & Secrets ---
# AWS Secrets Manager for API keys and database credentials.
resource "aws_secretsmanager_secret" "arms_secrets" {
  name = "arms-prod-secrets"
}

# achelion_arms/infra/variables.tf

variable "aws_region" {
  description = "The AWS region to deploy the infrastructure to."
  default     = "us-east-1"
}

variable "environment" {
  description = "The name of the environment (e.g., prod, dev)."
  default     = "prod"
}

variable "project_name" {
  description = "The name of the project."
  default     = "arms"
}

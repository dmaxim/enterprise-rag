variable "namespace" {
  type        = string
  description = "Namespace for resource names"
  default     = "mxinfo-ent-rag"
}

variable "environment" {
  type        = string
  description = "Environment used in resource names"
  default     = "poc"
}

variable "location" {
  type        = string
  description = "Azure Region for resources"
  default     = "eastus"
}

variable "location_abbreviation" {
  type        = string
  description = "Azure Region abbreviation used in resource names"
  default     = "eus"
}

variable "subscription_id" {
  type        = string
  description = "Azure Subscription ID"

}

variable "tenant_id" {
  type        = string
  description = "Azure Tenant ID"

}

variable "key_vault_name" {
  type        = string
  description = "Key Vault name"
  default     = "kv-mxinfo-ent-rag-poc"
}


variable "user_principal_name" {
  type        = string
  description = "User Principal Name for KeyVault Access"

}
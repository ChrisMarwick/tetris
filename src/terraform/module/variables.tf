variable "environment" {
  type = string
  default = "staging"
}

variable "provision_ecr" {
  type = bool
  default = false
}
variable "environment" {
  type = string
  default = "staging"
}

variable "should_deploy_instance" {
  type = bool
  default = false
}
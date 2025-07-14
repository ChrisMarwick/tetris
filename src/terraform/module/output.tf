output "ecr_url" {
  value = data.aws_ecr_repository.ecr_datasource.repository_url
}
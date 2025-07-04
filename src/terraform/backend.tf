resource "aws_ecr_repository" "container_registry" {
    name = "tetris_container_registry_${var.environment}"
    force_delete = true

    image_scanning_configuration {
        scan_on_push = false
    }
}

# resource "aws_ecs_task_definition" "ecs_task_definition" {
#     family = "tetris_task_definition"
#
# }

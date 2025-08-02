resource "aws_ecr_repository" "container_registry" {
    name = "tetris_container_registry_${var.environment}"
    force_delete = true

    image_scanning_configuration {
        scan_on_push = false
    }
}

resource "aws_ecs_cluster" "ecs_cluster" {
    name = "tetris-backend-cluster-${var.environment}"
}

resource "aws_iam_role" "iam_role" {
    name = "ECSEC2Role-${var.environment}"

    assume_role_policy = jsonencode({
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment" {
    role = aws_iam_role.iam_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "iam_instance_profile" {
    name = "tetris-ec2-instance-profile-${var.environment}"
    role = aws_iam_role.iam_role.name
}

resource "aws_security_group" "tetris_sg" {
    name = "tetris-sg-${var.environment}"
    vpc_id = data.aws_vpc.vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "tetris_sg_rule" {
    security_group_id = aws_security_group.tetris_sg.id

    cidr_ipv4 = "0.0.0.0/0"
    ip_protocol = "-1"
}

resource "aws_vpc_security_group_egress_rule" "tetris_sg_rule" {
    security_group_id = aws_security_group.tetris_sg.id

    cidr_ipv4 = "0.0.0.0/0"
    ip_protocol = "-1"
}

resource "aws_launch_template" "launch_template" {
    name = "tetris-backend-launch-template-${var.environment}"
    image_id = "ami-01267069d3f827ef9"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.tetris_sg.id]
    key_name = "tetris-key-pair-${var.environment}"

    iam_instance_profile {
        name = "tetris-ec2-instance-profile-${var.environment}"
    }
}

resource "aws_autoscaling_group" "autoscaling_group" {
    name = "tetris-backend-autoscaling-group-${var.environment}"
    max_size = 1
    min_size = 1
    vpc_zone_identifier = data.aws_subnets.subnets.ids
    force_delete = true

    launch_template {
        id = aws_launch_template.launch_template.id
        version = "$Latest"
    }
}

resource "aws_ecs_capacity_provider" "capacity_provider" {
    name = "tetris-capacity-provider3-${var.environment}"
    auto_scaling_group_provider {
        auto_scaling_group_arn = aws_autoscaling_group.autoscaling_group.arn
        managed_termination_protection = "DISABLED"

        managed_scaling {
            maximum_scaling_step_size = 1
            minimum_scaling_step_size = 1
            status = "ENABLED"
        }
    }
}

resource "aws_ecs_cluster_capacity_providers" "ecs_capacity_providers" {
    cluster_name = aws_ecs_cluster.ecs_cluster.name
    capacity_providers = [aws_ecs_capacity_provider.capacity_provider.name]
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
    count = var.should_deploy_instance ? 1 : 0

    family = "tetris-backend-${var.environment}"
    container_definitions = jsonencode([
        {
            "name": "tetris-backend",
            "image": "${aws_ecr_repository.container_registry.repository_url}:${var.environment}",
            "cpu": 0,
            "portMappings": [
                {
                    "name": "tetris-backend-http",
                    "containerPort": 8000,
                    "hostPort": 80,
                    "protocol": "tcp",
                    "appProtocol": "http"
                }
            ],
            "essential": true,
            "environment": [],
            "environmentFiles": [],
            "mountPoints": [],
            "volumesFrom": [],
            "ulimits": [],
            "systemControls": []
        }
    ])
    memory = 900
    requires_compatibilities = ["EC2"]
}

resource "aws_ecs_service" "ecs_service" {
    count = var.should_deploy_instance ? 1 : 0

    name = "tetris-backend"
    cluster = aws_ecs_cluster.ecs_cluster.id
    task_definition = aws_ecs_task_definition.ecs_task_definition[0].id
    desired_count = 1
}
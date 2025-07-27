module "tetris" {
    source = "../../module"

    environment = "staging"
    should_deploy_instance = var.should_deploy_instance
}
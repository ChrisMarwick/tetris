module "tetris" {
    source = "../../module"

    environment = "live"
    should_deploy_instance = var.should_deploy_instance
}
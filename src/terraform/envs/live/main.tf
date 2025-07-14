module "tetris" {
    source = "../../module"

    environment = "live"
    provision_ecr = true
}
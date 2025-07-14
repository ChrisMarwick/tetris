module "tetris" {
    source = "../../module"

    environment = "staging"
    provision_ecr = false
}
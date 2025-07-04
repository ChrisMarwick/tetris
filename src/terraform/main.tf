resource "aws_resourcegroups_group" "resource_group" {
    name = "rg_tetris_${var.environment}"

    resource_query {
        query = <<JSON
{
    "ResourceTypeFilters": [
        "AWS::AllSupported"
    ],
    "TagFilters": [
        {
            "Key": "app",
            "Values": ["tetris"]
        }
    ]
}
JSON
    }
}

resource "aws_s3_bucket" "storage_bucket" {
    bucket = "unclechris-tetris-bucket-${var.environment}"
}
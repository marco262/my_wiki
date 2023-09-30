resource "google_storage_bucket" "my_wiki" {
  name     = "${local.project_id}-my-wiki"
  location = local.region
}
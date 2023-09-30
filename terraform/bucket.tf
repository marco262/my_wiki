resource "google_storage_bucket" "my_wiki" {
  name     = "${local.project_id}-my-wiki"
  location = local.region
  uniform_bucket_level_access = true
}

# Makes the bucket publicly accessible
resource "google_storage_bucket_iam_member" "all_users" {
  bucket = google_storage_bucket.my_wiki.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}
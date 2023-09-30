terraform {
  backend "gcs" {
    bucket = "upheld-setting-362218-terraform"
    prefix = "my-wiki"
    impersonate_service_account = "terraform-my-wiki@upheld-setting-362218.iam.gserviceaccount.com"
  }
}

provider "google" {
  project = local.project_id
  region = local.region
  impersonate_service_account = "terraform-my-wiki@upheld-setting-362218.iam.gserviceaccount.com"
}
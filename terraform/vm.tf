resource "google_compute_address" "my_wiki" {
  name         = "my-wiki"
  address_type = "EXTERNAL"
  network_tier = "STANDARD"
}

resource "google_compute_instance" "my_wiki" {
  name         = "my-wiki"
  zone         = local.zone
  machine_type = "e2-micro"
  boot_disk {
    device_name = "my-wiki"
    initialize_params {
      image = "debian-cloud/debian-11"
      type  = "pd-standard"
    }
  }
  network_interface {
    network = "default"
    access_config {
      nat_ip       = google_compute_address.my_wiki.address
      network_tier = "STANDARD"
    }
  }
  tags = [
    "https-server",
  ]
  scheduling {
    automatic_restart           = false
    instance_termination_action = "STOP"
    preemptible                 = true
    provisioning_model          = "SPOT"
  }
  service_account {
    email  = "8096397005-compute@developer.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }
}
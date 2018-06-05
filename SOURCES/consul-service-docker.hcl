service {
  name = "docker"
  tags = [ "docker" ]
  checks {
    name = "docker-script-check"
    args = [
      "/var/lib/consul/checks/check_docker",
      "-minimal",
      "-base-url=http://localhost:4243",
      "-warn-data-space=80",
      "-crit-data-space=90",
      "-warn-meta-space=80",
      "-crit-meta-space=90"
    ]
    interval = "10s"
  }
}

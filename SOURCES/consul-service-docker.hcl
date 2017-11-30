service {
  name = "docker"
  tags = [ "docker" ]
  checks {
    name = "Docker health check"
    script = "/var/lib/consul/checks/check_docker -base-url=http://localhost:4243"
    interval = "10s"
  }
}

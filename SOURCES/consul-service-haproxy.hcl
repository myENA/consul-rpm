service {
  name = "haproxy"
  port = 80
  tags = [ "haproxy", "lb" ]
  checks {
    name = "HAProxy stats check"
    http = "http://admin:admin@localhost/haproxy?stats;csv"
    interval = "10s"
  }
  checks {
    name = "HAProxy default backend check"
    http = "http://localhost.ena.com/check.json"
    interval = "10s"
  }
}

client_addr = "127.0.0.1 {{ GetPrivateInterfaces | exclude \"type\" \"IPv6\" | sort \"default\" | join \"address\" \" \" }}"
data_dir = "/var/lib/consul/data"
enable_script_checks = true
performance {
  raft_multiplier = 1
}

# Wireguard mesh network configuration generator

Used to generate config files to be used with `wg-quick` for a set of hosts (all of them behind [at worst] CGNAT) connected to a central machine that has a public IP and routes the traffic between the other hosts.
In the example config file provided the generated config files will allow the below flow of traffic:

> Bob -> Alice -> Charlie
> Charlie -> Alice -> Bob


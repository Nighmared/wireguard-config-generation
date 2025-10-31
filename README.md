# Wireguard mesh network configuration generator

Used to generate config files to be used with `wg-quick` for a set of hosts (all of them behind [at worst] CGNAT) connected to a central machine that has a public IP and routes the traffic between the other hosts.
In the example config file provided the generated config files will allow the below flow of traffic:

> Bob -> Alice -> Charlie
> Charlie -> Alice -> Bob

In the example config file all of Bobs traffic can be routed through Alice (also to the internet), so it can be used as a generic VPN too :)

## Usage

`python main.py`
It reads in the configuration from a file `base.json`


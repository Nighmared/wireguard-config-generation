from dataclasses import dataclass
import json
from typing import Optional
import os


@dataclass
class Peer:
    name: str
    allowed_ips: list[str]
    persistent_keepalive: int


@dataclass
class Host:
    name: str
    ip_addr: str
    privkey: str
    pubkey: str
    peers: list[Peer]
    is_proxy: bool
    endpoint: Optional[str] = None


@dataclass
class Base:
    hosts: list[Host]


def gen_config_file(h: Host, hosts: dict[str, Host]):
    fname = f"configs/{h.name}/wg0.conf"
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(
        fname,
        "w",
        encoding="utf-8",
    ) as outfile:
        outfile.write("[Interface]\n")
        outfile.write(f"Address = {h.ip_addr}\n")
        outfile.write("ListenPort = 51820\n")
        outfile.write(f"PrivateKey = {h.privkey}\n\n")
        if h.is_proxy:
            outfile.write(
                "PostUp = iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -o eth0 -j MASQUERADE\n"
            )
            outfile.write(
                "PostUp = iptables -I INPUT -p udp -m udp --dport 51820 -j ACCEPT\n"
            )
            outfile.write("PostUp = iptables -A FORWARD -i %i -j ACCEPT\n")
            outfile.write("PostUp = iptables -A FORWARD -o %i -j ACCEPT\n")
            outfile.write(
                "PostDown = iptables -t nat -D POSTROUTING -s 172.16.0.0/24 -o eth0 -j MASQUERADE\n"
            )
            outfile.write(
                "PostDown = iptables -D INPUT -p udp -m udp --dport 51820 -j ACCEPT\n"
            )
            outfile.write("PostDown = iptables -D FORWARD -i %i -j ACCEPT\n")
            outfile.write("PostDown = iptables -D FORWARD -o %i -j ACCEPT\n\n")

        for peer in h.peers:
            ph = hosts[peer.name]
            outfile.write(f"[Peer]  #{ph.name}\n")
            outfile.write(f"PublicKey = {ph.pubkey}\n")
            outfile.write(f"AllowedIPs = {','.join(peer.allowed_ips)}\n")
            if ph.endpoint is not None:
                outfile.write(f"Endpoint = {ph.endpoint}\n")
            outfile.write(f"PersistentKeepalive = {peer.persistent_keepalive}\n")

            outfile.write("\n")


def main():
    with open("base.json", "r", encoding="utf-8") as f:
        info = json.loads(f.read())
        data = Base(
            hosts=[
                Host(
                    endpoint=i["endpoint"] if "endpoint" in i else None,
                    ip_addr=i["ip_addr"],
                    name=i["name"],
                    peers=[Peer(**p) for p in i["peers"]],
                    privkey=i["privkey"],
                    pubkey=i["pubkey"],
                    is_proxy=i["is_proxy"],
                )
                for i in info["hosts"]
            ]
        )

        hosts: dict[str, Host] = dict((h.name, h) for h in data.hosts)
        for h in data.hosts:
            gen_config_file(h, hosts)


if __name__ == "__main__":
    main()

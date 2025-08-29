import shutil
import os
from pathlib import Path

for i in range(180):
    sat_dir = Path(f"conf/Sat{i}/frr_conf")
        
    try:
        if sat_dir.exists():
            # 删除整个 frr_conf 文件夹及其内容
            shutil.rmtree(sat_dir)
        else:
            print(f"不存在: {sat_dir} - 跳过")
    except Exception as e:
        print(f"删除 {sat_dir} 时出错: {str(e)}")


# OSPFv6配置
for i in range(180):
    area =i // 30  # 区域编号 (0-5)
    orbit = i // 10  # 轨道编号 (0-17)
    number = i % 10  # 轨道内编号 (0-9)
    location = orbit % 3  # 域内位置 (0-2)
    if location == 0:
        ospf6_conf = f"""!
frr version 8.4-my-manual-build
frr defaults traditional
hostname Sat{i}
!
interface eth0
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth1
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth3
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
router ospf6
  ospf6 router-id 10.{area}.{orbit}.{number}
  redistribute connected
  redistribute bgp
!
"""
    elif location == 1:
        ospf6_conf = f"""!
frr version 8.4-my-manual-build
frr defaults traditional
hostname Sat{i}
!
interface eth0
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth1
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth2
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth3
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
router ospf6
  ospf6 router-id 10.{area}.{orbit}.{number}
  redistribute connected
  redistribute bgp
!
"""
    elif location == 2:
        ospf6_conf = f"""!
frr version 8.4-my-manual-build
frr defaults traditional
hostname Sat{i}
!
interface eth0
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth1
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
interface eth2
  ipv6 ospf6 area 0.0.0.0
  ipv6 ospf6 hello-interval 60
  ipv6 ospf6 dead-interval 180
!
router ospf6
  ospf6 router-id 10.{area}.{orbit}.{number}
  redistribute connected
  redistribute bgp
!
"""

    # 确保目录存在
    os.makedirs(f"conf/Sat{i}/frr_conf", exist_ok=True)
    os.makedirs(f"conf/Sat{i}/frr_log", exist_ok=True)
    
    with open(f"conf/Sat{i}/frr_conf/ospf6d.conf", "w") as f:
        f.write(ospf6_conf)


# Zebra配置
for i in range(180):
    area =i // 30
    orbit = i // 10
    number = i % 10
    
    zebra_conf = f"""!
hostname Sat{i}
!
interface lo
  ipv6 address fd00::{area}:{orbit}:{number}/128
  ip forwarding
  ipv6 forwarding
!
log timestamp precision 6
log file /var/log/frr/zebra.log
!
"""

    os.makedirs(f"conf/Sat{i}/frr_conf", exist_ok=True)
    with open(f"conf/Sat{i}/frr_conf/zebra.conf", "w") as f:
        f.write(zebra_conf)


#BGP配置
for i in range(m*n):
    area =i // 30  # 区域编号 (0-5)
    orbit = i // 10  # 轨道编号 (0-17)
    number = i % 10  # 轨道内编号 (0-9)
    location = orbit % 3  # 域内位置 (0-2)
    as_number = area + 1;   #AS编号

    if location==0 and number==5:
        bgp_conf = f"""!
hostname Sat{i}
!
router bgp {as_number}
  bgp router-id 192.{area}.{orbit}.{number}
  timers bgp 60 180
  no bgp ebgp-requires-policy
  no bgp network import-check
  neighbor eth2 interface remote-as external
  neighbor eth2 timers connect 5
  neighbor fd00::{area}:{orbit+2}:{number} remote-as {as_number}
  neighbor fd00::{area}:{orbit+2}:{number} update-source lo
  !
  address-family ipv6 unicast
    neighbor eth2 activate
    neighbor fd00::{area}:{orbit+2}:{number} activate
    network fd00::{area}:0:0/96
  exit-address-family
!
"""
        os.makedirs(f"conf/Sat{i}/frr_conf", exist_ok=True)
        with open(f"conf/Sat{i}/frr_conf/bgpd.conf", "w") as f:
            f.write(bgp_conf)

    elif location==2 and number==5:
        bgp_conf = f"""!
hostname Sat{i}
!
router bgp {as_number}
  bgp router-id 192.{area}.{orbit}.{number}
  timers bgp 60 180
  no bgp ebgp-requires-policy
  no bgp network import-check
  neighbor eth3 interface remote-as external
  neighbor eth3 timers connect 5
  neighbor fd00::{area}:{orbit-2}:{number} remote-as {as_number}
  neighbor fd00::{area}:{orbit-2}:{number} update-source lo
  !
  address-family ipv6 unicast
    neighbor eth3 activate
    neighbor fd00::{area}:{orbit-2}:{number} activate
    network fd00::{area}:0:0/96
  exit-address-family
!
"""
        os.makedirs(f"conf/Sat{i}/frr_conf", exist_ok=True)
        with open(f"conf/Sat{i}/frr_conf/bgpd.conf", "w") as f:
            f.write(bgp_conf)


#daemons
for i in range(180):
    area =i // 30  # 区域编号 (0-5)
    orbit = i // 10  # 轨道编号 (0-17)
    number = i % 10  # 轨道内编号 (0-9)
    location = orbit % 3  # 域内位置 (0-2)

    if (location==0 or location==2) and number==5:
        src = "daemons_bgp_ospf6"
    else: 
        src = "daemons_ospf6"
    dst = f"conf/Sat{i}/frr_conf/daemons"
    # 确保目标目录存在
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    # 复制文件
    shutil.copy(src, dst)
# RBL Keeper
Raspberry Pi zero上で走り、rbl_callcenterと連携して然るべきタイミングに回転灯を回す

# 導入
/home/rblkeeper/ 直下にgit clone

## rpi起動時に自動的に実行されるようにする
1. rbl.serviceを以下のディレクトリに配置
/lib/systemd/system/

2. 以下を実行し、再起動
systemctl start test.service

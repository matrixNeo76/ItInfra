# RouterOS Configuration Script - Progetto: severino-srl
# Generato automaticamente da ItInfra Automation Suite
# Data generazione: 2026-09-16 09:55:39

################################################################
# Estratto da: 04-MOP.md
################################################################
# Script Configurazione Iniziale MikroTik CRS326-24G-2S+RM
/system identity set name="sw-core-01"

# Creazione bridge LAN locale
/interface bridge add name=bridge-local protocol-mode=rstp

# Aggiunta porte ether2-ether24 al bridge locale (ether1 rimane ESCLUSA per WAN)
/interface bridge port
add bridge=bridge-local interface=ether2
add bridge=bridge-local interface=ether3
add bridge=bridge-local interface=ether4
add bridge=bridge-local interface=ether5
add bridge=bridge-local interface=ether6
add bridge=bridge-local interface=ether7
add bridge=bridge-local interface=ether8
add bridge=bridge-local interface=ether9
add bridge=bridge-local interface=ether10
add bridge=bridge-local interface=ether11
add bridge=bridge-local interface=ether12
add bridge=bridge-local interface=ether13
add bridge=bridge-local interface=ether14
add bridge=bridge-local interface=ether15
add bridge=bridge-local interface=ether16
add bridge=bridge-local interface=ether17
add bridge=bridge-local interface=ether18
add bridge=bridge-local interface=ether19
add bridge=bridge-local interface=ether20
add bridge=bridge-local interface=ether21
add bridge=bridge-local interface=ether22
add bridge=bridge-local interface=ether23
add bridge=bridge-local interface=ether24

# Assegnazione IP di Management e Gateway LAN al bridge
/ip address add address=192.168.120.1/24 interface=bridge-local comment="Default Gateway LAN Severino"

# Configurazione interfaccia WAN ether1
/interface list add name=WAN
/interface list add name=LAN
/interface list member add interface=ether1 list=WAN
/interface list member add interface=bridge-local list=LAN

/ip dhcp-client add interface=ether1 disabled=no comment="WAN Uplink da Vodafone Station"

# Regole Firewall e NAT Masquerade
/ip firewall nat add chain=srcnat out-interface-list=WAN action=masquerade comment="NAT Masquerade verso Internet"

/ip firewall filter
add chain=input action=accept connection-state=established,related comment="Accetta connessioni stabilite"
add chain=input action=drop connection-state=invalid comment="Drop pacchetti invalidi"
add chain=input action=accept in-interface-list=LAN comment="Accesso management consentito da LAN"
add chain=input action=drop in-interface-list=WAN comment="Blocca accessi diretti da WAN"
add chain=forward action=accept connection-state=established,related
add chain=forward action=drop connection-state=invalid
add chain=forward action=accept in-interface-list=LAN out-interface-list=WAN comment="Traffico outbound LAN verso WAN"
add chain=forward action=drop in-interface-list=WAN connection-nat-state=!dstnat comment="Blocca traffico non sollecitato da WAN"

# Configurazione DNS Forwarding con fallback
/ip dns set allow-remote-requests=yes servers=192.168.120.239,1.1.1.1,8.8.8.8

# Backup configurazione
/system backup save name="mop-baseline-sw-core-01"

################################################################
# Estratto da: 05-Rollback.md
################################################################
# Script Fallback Emergenza MikroTik Switch Semplificato
/system identity set name="sw-fallback-01"
/interface bridge add name=bridge-all
/interface bridge port add bridge=bridge-all interface=all
/ip address add address=192.168.1.254/24 interface=bridge-all comment="Accesso diretto su range Vodafone Station"

################################################################
# Estratto da: 08-SOP-Runbook.md
################################################################
# Connettersi via SSH o Terminale WinBox a sw-core-01 (192.168.120.1)
/system identity print
# 1. Generazione backup binario (password prelevata da vault://it/projects/severino-srl/mikrotik/backup-key)
/system backup save name="asbuilt-backup-sw-core-01"

# 2. Generazione export configurazione in chiaro per audit
/export file="asbuilt-export-sw-core-01.rsc"

################################################################
# Estratto da: 08-SOP-Runbook.md
################################################################
/system package update check-for-updates
   ```
2. Se approvato da Marco Severino, procedere con il download e l'installazione fuori orario lavorativo:
   ```routeros
   /system package update download
   /system reboot
   ```
3. Dopo il riavvio, aggiornare il BIOS del bootloader hardware (RouterBOOT):
   ```routeros
   /system routerboard upgrade
   /system reboot
   ```
4. Al riavvio finale, verificare lo stato del bridge e della WAN:
   ```routeros
   /interface bridge print
   /ip route print
   /ping 8.8.8.8 count=4
   ```

---

## 6. Procedura RB-05: Manutenzione Host HP Z4 e Macchine Virtuali

**ID Runbook:** RB-05  
**Livello Rischio:** L2/L3  
**Frequenza:** Mensile (Patch Day Microsoft)  
**Autorità:** Francesco Iavarone / Marco Severino  

### 6.1 Sequenza di Riavvio Ordinato delle Macchine Virtuali
Qualora sia necessario riavviare l'host fisico HP Z4 per aggiornamenti di sistema:


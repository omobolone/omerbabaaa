# Mastürbasyon Bırakma Robotu (Gün Gün Sayaç)

Bu proje, terminalden çalışan basit bir **gün sayacı robotudur**.
Amaç: alışkanlığı bırakma sürecinde kaçıncı günde olduğunu takip etmek.

## Kurulum

Python 3.10+ yeterli.

## Kullanım

```bash
python3 nofap_robot.py baslat
python3 nofap_robot.py durum
python3 nofap_robot.py bozdum
python3 nofap_robot.py gecmis
```

### Özel tarih ile işlem

```bash
python3 nofap_robot.py baslat --tarih 2026-02-01
python3 nofap_robot.py bozdum --tarih 2026-02-20
```

## Veri dosyası

Uygulama çalışma dizininde `nofap_data.json` dosyası oluşturur.

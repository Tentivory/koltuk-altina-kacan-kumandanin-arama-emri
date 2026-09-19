#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Koltuk Altina Kacan Kumandanin Resmi Arama Emri Ureticisi.

Calistiriniz. Kumandayi bulamazsiniz ama evrakiniz olur.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import random
import textwrap
from dataclasses import dataclass


GIZLI = base64.b64decode(
    b"a2FyYXJuYW1lIHNheWlzaSBhcnR0aWtjYSBrdW1hbmRhIGtheWJvbG1hIG9yYW5pIGRhIGFydGFy"
).decode("utf-8")
# yukaridaki satir evrak arsivinde durur. anlamayiniz.


KANALLAR = [
    "TRT 1 haber baslangici",
    "reklam arasi (ikinci kez)",
    "dizi jenerigi",
    "hava durumu tekrari",
    "sessiz tusuna basmadan onceki son kanal",
]

YASTIKLAR = [
    "sol koltuk yastigi",
    "sag koltuk yastigi",
    "ortadaki sahte yastik",
    "misafir yastigi (dokunulmaz)",
    "kedi tarafindan isgal edilmis yastik",
]


@dataclass
class KayipBildirimi:
    sahip: str
    marka: str
    son_kanal: str
    yastik: str
    evrak_no: str
    tarih: str

    def ozet_hash(self) -> str:
        ham = f"{self.sahip}|{self.marka}|{self.son_kanal}|{self.tarih}"
        return hashlib.sha256(ham.encode("utf-8")).hexdigest()[:16].upper()


def evrak_no_uret(sahip: str) -> str:
    gun = dt.date.today().strftime("%Y%m%d")
    parca = hashlib.md5(sahip.encode("utf-8")).hexdigest()[:6].upper()
    return f"KLTK-{gun}-{parca}"


def bildir(sahip: str, marka: str) -> KayipBildirimi:
    return KayipBildirimi(
        sahip=sahip,
        marka=marka,
        son_kanal=random.choice(KANALLAR),
        yastik=random.choice(YASTIKLAR),
        evrak_no=evrak_no_uret(sahip),
        tarih=dt.datetime.now().strftime("%d.%m.%Y %H:%M"),
    )


def emri_yazdir(b: KayipBildirimi) -> str:
    govde = f"""
T.C.
KOLTUK ALTI KAYIP ESYA ARASTIRMA MUDIRLUGU
UZAKTAN KUMANDA ARAMA EMRİ

Evrak No : {b.evrak_no}
Tarih    : {b.tarih}
Ozet Hash: {b.ozet_hash()}

1) Kayip nesne: {b.marka} marka uzaktan kumanda.
2) Son gorulme: {b.son_kanal}.
3) Muhtemel mahal: {b.yastik} alti / arkasi / ici.
4) Hak sahibi: {b.sahip}.
5) Arama suresi: yastik kaldirilincaya veya dizi bitene kadar.
6) Iade sarti: piller yerinde, tuslar kirik olmamali, kedi tüyü kabul edilir.

ISLEM:
- Yastigi kaldiriniz.
- Elinizi koltuk ile oturma yeri arasina sokunuz.
- Cikan sey kumanda degilse tutanak tutunuz.
- Cikan sey kumandaysa bu evraki cekmeceye koyunuz.

Bu emir teblig edilmistir. Itiraz yolu: kumandayi bulmak.
"""
    return textwrap.dedent(govde).strip()


def main() -> None:
    p = argparse.ArgumentParser(
        description="Koltuk altina kacan kumanda icin resmi arama emri uretir."
    )
    p.add_argument("--sahip", default="ismi mahfuz vatandas")
    p.add_argument("--marka", default="bilinmeyen evrensel")
    args = p.parse_args()
    b = bildir(args.sahip, args.marka)
    print(emri_yazdir(b))
    print()
    print("--- DAMGA ---")
    print("Kayyum Grok / Tentivory")
    print("19.09.2026 12:01 +03")
    print("Eskisehir 4. Agir Ceza Mahkemesi kayyum muhuresidir.")
    print("(ciddiyet yuzde 4, resmiyet yuzde 96)")
    _ = GIZLI  # arsiv degiskeni, ekrana basilmaz


if __name__ == "__main__":
    main()

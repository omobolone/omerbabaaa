#!/usr/bin/env python3
"""Mastürbasyon bırakma gün sayacı (CLI robot)."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

DATA_PATH = Path("nofap_data.json")


@dataclass
class TrackerState:
    start_date: date
    relapses: list[date]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TrackerState":
        return cls(
            start_date=_parse_date(raw["start_date"]),
            relapses=[_parse_date(item) for item in raw.get("relapses", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "start_date": self.start_date.isoformat(),
            "relapses": [d.isoformat() for d in self.relapses],
        }

    def streak_days(self, today: date | None = None) -> int:
        now = today or date.today()
        return (now - self.start_date).days + 1


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_state(path: Path = DATA_PATH) -> TrackerState | None:
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return TrackerState.from_dict(raw)


def save_state(state: TrackerState, path: Path = DATA_PATH) -> None:
    path.write_text(
        json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def robot_message_for_streak(days: int) -> str:
    if days < 7:
        return "Başlangıç çok önemli. Her gün kazanım!"
    if days < 30:
        return "Harika gidiyorsun. İstikrar oturuyor."
    if days < 90:
        return "Süper seri! Disiplinin güçleniyor."
    return "Efsane seviye! Yeni yaşam düzenin kalıcı hale geliyor."


def cmd_baslat(args: argparse.Namespace) -> None:
    start = _parse_date(args.tarih) if args.tarih else date.today()
    state = TrackerState(start_date=start, relapses=[])
    save_state(state)
    print(f"🤖 Sayaç başlatıldı: {start.isoformat()} (1. gün)")


def cmd_durum(_: argparse.Namespace) -> None:
    state = load_state()
    if not state:
        print("🤖 Kayıt bulunamadı. Önce 'baslat' komutunu kullan.")
        return

    days = state.streak_days()
    print(f"🤖 Bugün {days}. gündesin.")
    print(f"   Başlangıç tarihi: {state.start_date.isoformat()}")
    print(f"   Toplam reset sayısı: {len(state.relapses)}")
    print(f"   Motivasyon: {robot_message_for_streak(days)}")


def cmd_bozdum(args: argparse.Namespace) -> None:
    state = load_state()
    if not state:
        print("🤖 Önce 'baslat' ile sayaç oluşturman gerekiyor.")
        return

    relapse_date = _parse_date(args.tarih) if args.tarih else date.today()
    state.relapses.append(relapse_date)
    state.start_date = relapse_date
    save_state(state)
    print(f"🤖 Reset kaydedildi: {relapse_date.isoformat()}. Yeni seri başladı (1. gün).")


def cmd_gecmis(_: argparse.Namespace) -> None:
    state = load_state()
    if not state:
        print("🤖 Geçmiş bulunamadı.")
        return

    if not state.relapses:
        print("🤖 Henüz reset yok. Temiz seri devam ediyor.")
        return

    print("🤖 Reset geçmişi:")
    for i, relapse in enumerate(state.relapses, start=1):
        print(f"  {i}. {relapse.isoformat()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mastürbasyon bırakma gün sayacı robotu")
    sub = parser.add_subparsers(dest="komut", required=True)

    p_baslat = sub.add_parser("baslat", help="Sayacı başlat")
    p_baslat.add_argument("--tarih", help="YYYY-MM-DD")
    p_baslat.set_defaults(func=cmd_baslat)

    p_durum = sub.add_parser("durum", help="Güncel durumu göster")
    p_durum.set_defaults(func=cmd_durum)

    p_bozdum = sub.add_parser("bozdum", help="Reset kaydı gir")
    p_bozdum.add_argument("--tarih", help="YYYY-MM-DD")
    p_bozdum.set_defaults(func=cmd_bozdum)

    p_gecmis = sub.add_parser("gecmis", help="Reset geçmişini göster")
    p_gecmis.set_defaults(func=cmd_gecmis)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

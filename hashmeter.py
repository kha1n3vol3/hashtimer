#!/usr/bin/env python3

import asyncio
import sys
import uvloop
import hashlib
import time
import signal
from datetime import datetime
from pathlib import Path
from tdigest import TDigest
import json
from typing import Optional, Tuple, Dict, Any
import argparse

def load_banner() -> str:
    try:
        with open('banner.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "HashTimer"

class HashMeter:
    def __init__(self, args: argparse.Namespace):
        self.config = self._init_config(args)
        self.data_dir = Path(self.config['data_dir'])
        self.data_dir.mkdir(exist_ok=True)
        
        self.tdigest_file = self.data_dir / 'hashmeter.json'
        self.log_file = self.data_dir / f'timing_values_{datetime.now():%Y%m%d_%H%M%S}.log'
        self.running = True
        self.td = self._load_tdigest()
        
        self._setup_signal_handlers()

    def _init_config(self, args: argparse.Namespace) -> Dict[str, Any]:
        return {
            'password': args.password.encode(),
            'salt': args.salt.encode(),
            'iterations': args.iterations,
            'key_size': args.key_size,
            'interval': args.interval,
            'data_dir': args.data_dir
        }

    def _setup_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._handle_signal)

    def _handle_signal(self, signum: int, frame: Any) -> None:
        print("\nShutting down gracefully...")
        self.running = False

    def _load_tdigest(self) -> TDigest:
        try:
            if self.tdigest_file.exists():
                with open(self.tdigest_file) as f:
                    data = json.load(f)
                    td = TDigest()
                    td.update_centroids_from_list(data['centroids'])
                    return td
        except Exception as e:
            print(f"Error loading TDigest: {e}")
        return TDigest()

    async def measure(self) -> Tuple[bytes, float]:
        start = time.monotonic()
        hashed = hashlib.pbkdf2_hmac('sha256', 
                                    self.config['password'],
                                    self.config['salt'],
                                    self.config['iterations'],
                                    self.config['key_size'])
        return hashed, (time.monotonic() - start) * 1e6

    async def run(self):
        print(load_banner())
        
        header = "{:<12} {:<8} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
            "Current", "Count", "Min", "25th", "50th", "75th", "95th", "99th", "Max"
        )
        print("\n" + "="*108)
        print(header)
        print("="*108)

        while self.running:
            try:
                _, timing = await self.measure()
                self.td.update(timing)

                percentiles = [self.td.percentile(p) for p in [25, 50, 75, 95, 99]]
                
                stats = "{:<12} {:<8} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(
                    f"{timing:.2f} μs",
                    int(self.td.n),
                    f"{self.td.percentile(0):.2f} μs",
                    *[f"{p:.2f} μs" for p in percentiles],
                    f"{self.td.percentile(100):.2f} μs"
                )
                print(stats, flush=True)

                with open(self.log_file, 'a') as f:
                    f.write(f"{datetime.now().isoformat()},{timing:.2f}\n")
                
                if self.td.n % 1000 == 0:
                    self.td.compress()
                    print("[*] Compressed TDigest data")
                    self.td.compress()
                    with open(self.tdigest_file, 'w') as f:
                        json.dump({'centroids': self.td.centroids_to_list()}, f)

                await asyncio.sleep(self.config['interval'])
                
            except Exception as e:
                print(f"Error: {e}")
                self.running = False

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Monitor PBKDF2 hash timing distributions')
    parser.add_argument('--password', default='mysecretpassword', help='Password to hash')
    parser.add_argument('--salt', default='somesalt', help='Salt for hashing')
    parser.add_argument('--iterations', type=int, default=1000, help='Hash iterations')
    parser.add_argument('--key-size', type=int, default=32, help='Key size in bytes')
    parser.add_argument('--interval', type=int, default=15, help='Measurement interval in seconds')
    parser.add_argument('--data-dir', default='data', help='Directory for data files')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    meter = HashMeter(args)
    
    try:
        if sys.version_info >= (3, 11):
            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(meter.run())
        else:
            uvloop.install()
            asyncio.run(meter.run())
    except Exception as e:
        print(f"Fatal error: {e}")

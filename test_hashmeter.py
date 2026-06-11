import argparse
import asyncio
import json
import tempfile
import unittest

from hashmeter import HashMeter


class HashMeterPersistenceTest(unittest.TestCase):
    def test_short_run_persists_tdigest_on_exit(self):
        with tempfile.TemporaryDirectory() as data_dir:
            args = argparse.Namespace(
                password="password",
                salt="salt",
                iterations=1,
                key_size=32,
                interval=0,
                data_dir=data_dir,
            )
            meter = HashMeter(args)

            async def measure_once():
                meter.running = False
                return b"hash", 123.45

            meter.measure = measure_once

            asyncio.run(meter.run())

            timing_logs = list(meter.data_dir.glob("timing_values_*.log"))
            self.assertEqual(1, len(timing_logs))
            self.assertTrue(meter.tdigest_file.exists())

            with open(meter.tdigest_file) as f:
                data = json.load(f)

            self.assertTrue(data["centroids"])


if __name__ == "__main__":
    unittest.main()

import contextlib
import io
import json
import tempfile
import unittest

from tdigest import TDigest

from analyze_hashmeter import analyze_hashmeter_data


class AnalyzeHashmeterTest(unittest.TestCase):
    def test_identical_timings_report_unavailable_ratios(self):
        td = TDigest()
        for _ in range(3):
            td.update(0.0)

        with tempfile.NamedTemporaryFile("w", suffix=".json") as fixture:
            json.dump({"centroids": td.centroids_to_list()}, fixture)
            fixture.flush()

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = analyze_hashmeter_data(fixture.name)

        self.assertIsNone(result["stability_ratio"])
        self.assertIsNone(result["outlier_ratio"])
        self.assertIn("Stability Ratio (IQR/Median): N/A", output.getvalue())
        self.assertIn("Outlier Impact Ratio: N/A", output.getvalue())


if __name__ == "__main__":
    unittest.main()

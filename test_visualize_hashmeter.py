import unittest
from unittest import mock

import visualize_hashmeter


class VisualizeHashmeterCliTest(unittest.TestCase):
    def test_parse_args_defaults_to_hashmeter_json(self):
        args = visualize_hashmeter.parse_args([])

        self.assertEqual("data/hashmeter.json", args.file)

    def test_parse_args_accepts_custom_file(self):
        args = visualize_hashmeter.parse_args(["--file", "/tmp/run/hashmeter.json"])

        self.assertEqual("/tmp/run/hashmeter.json", args.file)

    def test_main_visualizes_selected_file_with_log_scale(self):
        tdigest = object()

        with mock.patch.object(visualize_hashmeter, "import_tdigest", return_value=tdigest) as import_tdigest:
            with mock.patch.object(visualize_hashmeter, "visualize_tdigest") as visualize_tdigest:
                visualize_hashmeter.main(["-f", "/tmp/run/hashmeter.json"])

        import_tdigest.assert_called_once_with("/tmp/run/hashmeter.json")
        visualize_tdigest.assert_called_once_with(tdigest, log_scale=True)


if __name__ == "__main__":
    unittest.main()

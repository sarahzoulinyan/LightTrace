import tempfile
import unittest
from pathlib import Path

from coordinate_io import load_coordinates, parse_coordinate_lines


class ParseCoordinateLinesTests(unittest.TestCase):
    def test_parses_parenthesized_and_plain_records(self):
        lines = ["(29.6516, -82.3248),\n", "28.5383, -81.3792\n"]

        self.assertEqual(
            parse_coordinate_lines(lines),
            [(29.6516, -82.3248), (28.5383, -81.3792)],
        )

    def test_ignores_blank_lines_and_comments(self):
        lines = ["\n", "# Florida boundary\n", " (30.3322, -81.6557) \n"]

        self.assertEqual(parse_coordinate_lines(lines), [(30.3322, -81.6557)])

    def test_reports_line_number_for_non_numeric_value(self):
        with self.assertRaisesRegex(ValueError, "line 2.*numeric"):
            parse_coordinate_lines(["(29.0, -82.0)\n", "(north, -81.0)\n"])

    def test_rejects_out_of_range_coordinates(self):
        with self.assertRaisesRegex(ValueError, "latitude out of range"):
            parse_coordinate_lines(["(91, 0)\n"])

        with self.assertRaisesRegex(ValueError, "longitude out of range"):
            parse_coordinate_lines(["(0, -181)\n"])

    def test_rejects_empty_input(self):
        with self.assertRaisesRegex(ValueError, "no coordinate records"):
            parse_coordinate_lines(["\n", "# comment\n"])


class LoadCoordinatesTests(unittest.TestCase):
    def test_loads_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "boundary.txt")
            path.write_text("(29.6516, -82.3248)\n", encoding="utf-8")

            self.assertEqual(load_coordinates(path), [(29.6516, -82.3248)])


if __name__ == "__main__":
    unittest.main()

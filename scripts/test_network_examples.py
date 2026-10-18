"""Author regression checks on synthetic inputs, never a student lab."""
import unittest
from network_examples import layers, subnet


class ExamplesTests(unittest.TestCase):
    def test_encapsulation_and_independent_calls(self):
        self.assertEqual(layers()["Ethernet"]["IPv4"]["TCP"]["data"], "example")
        changed = layers()
        changed.clear()
        self.assertIn("Ethernet", layers())

    def test_prefix_crosses_octet(self):
        result = subnet("192.0.2.139/26")
        self.assertEqual(result["network"], "192.0.2.128/26")
        self.assertEqual(result["netmask"], "255.255.255.192")
        self.assertEqual(result["first_host"], "192.0.2.129")
        self.assertEqual(result["last_host"], "192.0.2.190")
        self.assertEqual(result["host_count"], 62)

    def test_large_network_is_constant_space(self):
        self.assertEqual(subnet("192.0.2.1/0")["host_count"], 4294967294)

    def test_point_to_point_and_host_route(self):
        self.assertEqual(subnet("192.0.2.10/31")["host_count"], 2)
        self.assertEqual(subnet("192.0.2.10/32")["first_host"], "192.0.2.10")

    def test_invalid_input(self):
        for value in ("192.0.2.999/24", "192.0.2.1/33", "::1/128"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                subnet(value)


if __name__ == "__main__":
    unittest.main()

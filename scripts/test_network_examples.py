"""Author regression checks on synthetic inputs, never a student lab."""
import unittest
from network_examples import choose_route, layers, route_example, subnet


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

    def test_longest_prefix_independent_of_order(self):
        routes = [("0.0.0.0/0", "192.0.2.1", "e0"),
                  ("198.51.100.0/25", "192.0.2.2", "e0")]
        expected = "192.0.2.2"
        self.assertEqual(choose_route("198.51.100.13", routes)["next_hop"], expected)
        self.assertEqual(choose_route("198.51.100.13", list(reversed(routes)))["next_hop"], expected)
        self.assertEqual(route_example()["prefix"], "198.51.100.0/25")

    def test_direct_route_uses_destination(self):
        result = choose_route("192.0.2.11", [("192.0.2.0/24", None, "e0")])
        self.assertTrue(result["direct"])
        self.assertEqual(result["next_hop"], "192.0.2.11")

    def test_default_and_missing_route(self):
        self.assertIsNone(choose_route("203.0.113.5", []))
        result = choose_route("203.0.113.5", [("0.0.0.0/0", "192.0.2.1", "e0")])
        self.assertEqual(result["prefix"], "0.0.0.0/0")

    def test_equal_prefix_is_explicitly_unsupported(self):
        with self.assertRaisesRegex(ValueError, "equal prefixes"):
            choose_route("192.0.2.11", [("192.0.2.0/24", None, "e0"),
                                        ("192.0.2.0/24", None, "e1")])

    def test_invalid_route_configuration(self):
        for route in [("192.0.2.1/24", None, "e0"),
                      ("0.0.0.0/0", "bad", "e0"),
                      ("0.0.0.0/0", None, "")]:
            with self.subTest(route=route), self.assertRaises(ValueError):
                choose_route("192.0.2.11", [route])


if __name__ == "__main__":
    unittest.main()

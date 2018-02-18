import unittest
import time
from nrf24l01 import NRF24L01

class TestDeviceCreation(unittest.TestCase):
    pipes = [[0xe7, 0xd3, 0xf0, 0x35, 0x77],
             [0xc2, 0xc2, 0xc2, 0xc2, 0xc2],
             [0xc3],
             [0xc4],
             [0xc5],
             [0xc6]]

    def setUp(self):
        super().setUp()
        self.radio = NRF24L01(0, 0, 22, 18)
        self.radio.address_width = 5
        self.radio.crc = NRF24L01.CRC_ENABLED
        self.radio.crc_length = NRF24L01.CRC_8
        self.radio.pa_level = NRF24L01.PA_HIGH
        self.radio.data_rate = NRF24L01.BR_2MBPS
        self.radio.channel = 76
        self.radio.retries = 5
        self.radio.delay = 1000
        self.radio.enable_interrupt(NRF24L01.RX_DR | NRF24L01.TX_DS | NRF24L01.MAX_RT)

    def test_valid(self):
        self.assertIsNotNone(self.radio, 'Initialization of radio failed')

    def test_read_mode(self):
        for k, v in enumerate(self.pipes):
            self.radio.open_rx_pipe(k, v, 32)
        self.radio.start_listening()
        time.sleep(1)
        self.assertEqual(self.radio.state, 'rx_mode', 'State was not RX_MODE')

    def test_transmit_mode(self):
        self.radio.enable_dynamic_payload(0)
        self.radio.open_tx_pipe(self.pipes[0], 32)
        self.radio.stop_listening()
        self.assertEqual(self.radio.state, 'standby_i', 'State was not STANDBY_I')

    def test_dynammic_rx_payload(self):
        for k, v in enumerate(self.pipes):
            self.radio.open_rx_pipe(k, v, 32)
            self.radio.enable_dynamic_payload(k)

        self.assertTrue(self.radio.is_dynamic_payload(0), 'Dynamic payload not enabled')
        self.assertTrue(self.radio.is_dynamic_payload(1), 'Dynamic payload not enabled')
        self.assertTrue(self.radio.is_dynamic_payload(2), 'Dynamic payload not enabled')
        self.assertTrue(self.radio.is_dynamic_payload(3), 'Dynamic payload not enabled')
        self.assertTrue(self.radio.is_dynamic_payload(4), 'Dynamic payload not enabled')
        self.assertTrue(self.radio.is_dynamic_payload(5), 'Dynamic payload not enabled')

    def tearDown(self):
        self.radio.stop()


if __name__ == '__main__':
    unittest.main()



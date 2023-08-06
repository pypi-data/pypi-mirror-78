import unittest
from unittest import mock

from cloudshell.cp.core.reservation_info import ReservationInfo


class TestReservationInfo(unittest.TestCase):
    def setUp(self):
        self.context = mock.MagicMock()

    def test_from_resource_context(self):
        reservation_info = ReservationInfo.from_resource_context(context=self.context)
        self.assertEqual(
            reservation_info.reservation_id, self.context.reservation.reservation_id
        )

    def test_from_remote_resource_context(self):
        reservation_info = ReservationInfo.from_remote_resource_context(
            context=self.context
        )
        self.assertEqual(
            reservation_info.reservation_id,
            self.context.remote_reservation.reservation_id,
        )

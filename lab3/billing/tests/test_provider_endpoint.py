from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from billing.models import Barrel, Invoice, InvoiceLine, Provider

User = get_user_model()


class ProviderEndpointTests(APITestCase):
    def setUp(self):
        self.provider_a = Provider.objects.create(
            name="Acme Oils",
            address="Main St 1",
            tax_id="TAX-12345",
        )

        self.provider_b = Provider.objects.create(
            name="Industrias Don Pepe",
            address="Sesame St 1",
            tax_id="TAX-78787",
        )

        self.invoice_a = Invoice.objects.create(
            provider=self.provider_a, invoice_no="INV-001", issued_on="2024-10-10"
        )

        self.invoice_b = Invoice.objects.create(
            provider=self.provider_b, invoice_no="INV-002", issued_on="2025-5-5"
        )

        self.barrel = Barrel.objects.create(
            provider=self.provider_b,
            number="BAR-001",
            oil_type="Virgin Extra",
            liters=50,
            billed=False,
        )

        self.user_a = User.objects.create_user(
            username="regular_user", password="strongpass123", provider=self.provider_a
        )

        self.provider_list_url = reverse("provider-list")
        self.invoice_list_url = reverse("invoice-list")

    def test_provider_list_returns_name_and_tax_id(self):
        provider = Provider.objects.create(
            name="Acme Oils",
            address="Main St 1",
            tax_id="TAX-12345",
        )
        user = User.objects.create_user(
            username="provider_user",
            password="strongpass123",
            provider=provider,
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("provider-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("name", response.data[0])
        self.assertIn("tax_id", response.data[0])
        self.assertEqual(response.data[0]["name"], provider.name)
        self.assertEqual(response.data[0]["tax_id"], provider.tax_id)

    def test_cross_add_barrel_to_invoice(self):
        user = User.objects.create_user(
            username="testuser",
            password="password",
            provider=self.provider_a,
        )
        self.client.force_authenticate(user=user)

        url = reverse("invoice-add-line", args=[self.invoice_a.pk])
        data = {
            "barrel": self.barrel.id,
            "liters": 50,
            "unit_price": "25.00",
            "description": "I'm an invoice line in an invoice world",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "barrel provider must match invoice provider",
            response.data.get("detail", ""),
        )
        self.assertEqual(InvoiceLine.objects.count(), 0)

        self.barrel.refresh_from_db()
        self.assertFalse(self.barrel.billed)

    def test_list_and_detail_visibility_as_regular_user(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.get(self.invoice_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("invoice_no", response.data[0])
        self.assertEqual(response.data[0]["invoice_no"], self.invoice_a.invoice_no)

        url = reverse("invoice-detail", args=[self.invoice_b.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)
        self.assertNotIn("invoice_no", response.data)
        self.assertIn("detail", response.data)

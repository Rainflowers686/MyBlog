import importlib.util
import os
from pathlib import Path
import runpy
from unittest.mock import Mock, patch

from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase, override_settings

from .views import DemoPasswordResetView


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class SecurityConfigurationTests(SimpleTestCase):
    def load_settings(self, **values):
        with patch.dict(os.environ, values):
            return runpy.run_path(str(PROJECT_ROOT / "myblog/settings.py"))

    def test_missing_secret_prevents_startup(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "DJANGO_SECRET_KEY"):
            self.load_settings(DJANGO_SECRET_KEY="", DB_PASSWORD="synthetic-test-only")

    def test_old_development_key_is_rejected(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "Generate a new"):
            self.load_settings(
                DJANGO_SECRET_KEY="django-insecure-" + "x" * 60,
                DB_PASSWORD="synthetic-test-only",
            )

    def test_missing_database_password_prevents_startup(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "DB_PASSWORD"):
            self.load_settings(DJANGO_SECRET_KEY="test-key-" * 8, DB_PASSWORD="")

    def test_demo_flag_cannot_enable_reset_links_when_debug_is_off(self):
        config = self.load_settings(
            DJANGO_SECRET_KEY="test-key-" * 8,
            DB_PASSWORD="synthetic-test-only",
            DJANGO_DEBUG="0",
            MYBLOG_DEMO_PASSWORD_RESET="1",
        )
        self.assertFalse(config["DEBUG"])
        self.assertFalse(config["MYBLOG_DEMO_PASSWORD_RESET"])


class PasswordResetBoundaryTests(SimpleTestCase):
    def assert_normal_mail_flow(self):
        request = RequestFactory().post(
            "/accounts/password/reset/",
            {"email": "person@example.invalid"},
            HTTP_HOST="localhost",
        )
        view = DemoPasswordResetView()
        view.setup(request)
        form = Mock()
        form.cleaned_data = {"email": "person@example.invalid"}
        with patch("core.views.get_user_model") as lookup, patch("core.views.render") as render:
            response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/password/reset/done/")
        form.save.assert_called_once()
        lookup.assert_not_called()
        render.assert_not_called()

    @override_settings(DEBUG=False, MYBLOG_DEMO_PASSWORD_RESET=True)
    def test_production_does_not_return_a_reset_token(self):
        self.assert_normal_mail_flow()

    @override_settings(DEBUG=True, MYBLOG_DEMO_PASSWORD_RESET=False)
    def test_debug_alone_does_not_return_a_reset_token(self):
        self.assert_normal_mail_flow()


class DatabaseHelperTests(SimpleTestCase):
    def load_helper(self):
        spec = importlib.util.spec_from_file_location(
            "myblog_setup_db_check", PROJECT_ROOT / "myblog/setup_db.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_import_has_no_database_side_effect(self):
        with patch("pymysql.connect") as connect:
            self.load_helper()
        connect.assert_not_called()

    def test_missing_password_does_not_connect(self):
        helper = self.load_helper()
        with patch.dict(os.environ, {"DB_PASSWORD": ""}), patch("pymysql.connect") as connect:
            result = helper.main()
        self.assertEqual(result, 1)
        connect.assert_not_called()

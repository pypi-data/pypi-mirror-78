# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

import pytest

from arkindex_worker.worker import ElementsWorker


@pytest.fixture(autouse=True)
def setup_api(responses, monkeypatch):

    # Always use the environment variable first
    schema_url = os.environ.get("ARKINDEX_API_SCHEMA_URL")
    if schema_url is None:
        # Try to load a local schema as the current developer of base-worker
        # may also work on the backend nearby
        paths = [
            "~/dev/ark/backend/schema.yml",
            "~/dev/ark/backend/output/schema.yml",
        ]
        for path in paths:
            path = Path(path).expanduser().absolute()
            print(path)
            if path.exists():
                monkeypatch.setenv("ARKINDEX_API_SCHEMA_URL", str(path))
                schema_url = str(path)
                break

    # Fallback to prod environment
    if schema_url is None:
        schema_url = "https://arkindex.teklia.com/api/v1/openapi/?format=openapi-json"

    # Allow accessing remote API schemas
    responses.add_passthru(schema_url)

    # Force api requests on a dummy server with dummy credentials
    monkeypatch.setenv("ARKINDEX_API_URL", "http://testserver/api/v1")
    monkeypatch.setenv("ARKINDEX_API_TOKEN", "unittest1234")


@pytest.fixture(autouse=True)
def give_worker_version_id_env_variable(monkeypatch):
    monkeypatch.setenv("WORKER_VERSION_ID", "12341234-1234-1234-1234-123412341234")


@pytest.fixture
def mock_worker_version_api(responses):
    """Provide a mock API response to get worker configuration"""
    payload = {
        "id": "12341234-1234-1234-1234-123412341234",
        "configuration": {
            "docker": {"image": "python:3"},
            "configuration": {"someKey": "someValue"},
        },
        "revision": {
            "hash": "deadbeef1234",
            "name": "some git revision",
        },
        "docker_image": "python:3",
        "docker_image_name": "python:3",
        "state": "created",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )


@pytest.fixture
def mock_elements_worker(monkeypatch, mock_worker_version_api):
    """Build and configure an ElementsWorker with fixed CLI parameters to avoid issues with pytest"""
    monkeypatch.setattr(sys, "argv", ["worker"])

    worker = ElementsWorker()
    worker.configure()
    return worker

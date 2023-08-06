# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import sys
import uuid
from enum import Enum

import yaml
from apistar.exceptions import ErrorResponse

from arkindex import ArkindexClient, options_from_env
from arkindex_worker import logger
from arkindex_worker.models import Element
from arkindex_worker.reporting import Reporter


class BaseWorker(object):
    def __init__(self, description="Arkindex Base Worker"):
        self.parser = argparse.ArgumentParser(description=description)

        # Setup workdir either in Ponos environment or on host's home
        if os.environ.get("PONOS_DATA"):
            self.work_dir = os.path.join(os.environ["PONOS_DATA"], "current")
        else:
            # We use the official XDG convention to store file for developers
            # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
            xdg_data_home = os.environ.get(
                "XDG_DATA_HOME", os.path.expanduser("~/.local/share")
            )
            self.work_dir = os.path.join(xdg_data_home, "arkindex")
            os.makedirs(self.work_dir, exist_ok=True)

        self.worker_version_id = os.environ.get("WORKER_VERSION_ID")
        if not self.worker_version_id:
            logger.warning(
                "Missing WORKER_VERSION_ID environment variable, worker is in read-only mode"
            )

        logger.info(f"Worker will use {self.work_dir} as working directory")

    @property
    def is_read_only(self):
        """Worker cannot publish anything without a worker version ID"""
        return self.worker_version_id is None

    def configure(self):
        """
        Configure worker using cli args and environment variables
        """
        self.parser.add_argument(
            "-c",
            "--config",
            help="Alternative configuration file when running without a Worker Version ID",
            type=open,
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            help="Display more information on events and errors",
            action="store_true",
            default=False,
        )

        # Call potential extra arguments
        self.add_arguments()

        # CLI args are stored on the instance so that implementations can access them
        self.args = self.parser.parse_args()

        # Setup logging level
        if self.args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

        # Build Arkindex API client from environment variables
        self.api_client = ArkindexClient(**options_from_env())
        logger.debug(f"Setup Arkindex API client on {self.api_client.document.url}")

        if self.worker_version_id:
            # Retrieve initial configuration from API
            worker_version = self.api_client.request(
                "RetrieveWorkerVersion", id=self.worker_version_id
            )
            logger.info(
                f"Loaded worker {worker_version['worker']['name']} revision {worker_version['revision']['hash'][0:7]} from API"
            )
            self.config = worker_version["configuration"]["configuration"]
        elif self.args.config:
            # Load config from YAML file
            self.config = yaml.safe_load(self.args.config)
            logger.info(
                f"Running with local configuration from {self.args.config.name}"
            )
        else:
            self.config = {}
            logger.warning("Running without any extra configuration")

    def add_arguments(self):
        """Override this method to add argparse argument to this worker"""

    def run(self):
        """Override this method to implement your own process"""


class TranscriptionType(Enum):
    Page = "page"
    Paragraph = "paragraph"
    Line = "line"
    Word = "word"
    Character = "character"


class EntityType(Enum):
    Person = "person"
    Location = "location"
    Subject = "subject"
    Organization = "organization"
    Misc = "misc"
    Number = "number"
    Date = "date"


class ElementsWorker(BaseWorker):
    def __init__(self, description="Arkindex Elements Worker"):
        super().__init__(description)

        # Add report concerning elements
        self.report = Reporter("unknown worker")

        # Add mandatory argument to process elements
        self.parser.add_argument(
            "--elements-list",
            help="JSON elements list to use",
            type=open,
            default=os.environ.get("TASK_ELEMENTS"),
        )
        self.parser.add_argument(
            "--element",
            type=uuid.UUID,
            nargs="+",
            help="One or more Arkindex element ID",
        )
        self.classes = {}

    def list_elements(self):
        assert not (
            self.args.elements_list and self.args.element
        ), "elements-list and element CLI args shouldn't be both set"
        out = []

        # Process elements from JSON file
        if self.args.elements_list:
            data = json.load(self.args.elements_list)
            assert isinstance(data, list), "Elements list must be a list"
            assert len(data), "No elements in elements list"
            out += list(filter(None, [element.get("id") for element in data]))
        # Add any extra element from CLI
        elif self.args.element:
            out += self.args.element

        return out

    def run(self):
        """
        Process every elements from the provided list
        """
        self.configure()

        # List all elements either from JSON file
        # or direct list of elements on CLI
        elements = self.list_elements()
        if not elements:
            logger.warning("No elements to process, stopping.")
            sys.exit(1)

        # Process every element
        count = len(elements)
        failed = 0
        for i, element_id in enumerate(elements, start=1):
            try:
                # Load element using Arkindex API
                element = Element(
                    **self.api_client.request("RetrieveElement", id=element_id)
                )
                logger.info(f"Processing {element} ({i}/{count})")
                self.process_element(element)
            except ErrorResponse as e:
                failed += 1
                logger.warning(
                    f"An API error occurred while processing element {element_id}: {e.title} - {e.content}",
                    exc_info=e if self.args.verbose else None,
                )
                self.report.error(element_id, e)
            except Exception as e:
                failed += 1
                logger.warning(
                    f"Failed running worker on element {element_id}: {e}",
                    exc_info=e if self.args.verbose else None,
                )
                self.report.error(element_id, e)

        # Save report as local artifact
        self.report.save(os.path.join(self.work_dir, "ml_report.json"))

        if failed:
            logger.error(
                "Ran on {} elements: {} completed, {} failed".format(
                    count, count - failed, failed
                )
            )
            if failed >= count:  # Everything failed!
                sys.exit(1)

    def process_element(self, element):
        """Override this method to analyze an Arkindex element from the provided list"""

    def load_corpus_classes(self, corpus_id):
        """
        Load ML classes for the given corpus ID
        """
        corpus_classes = self.api_client.request(
            "ListCorpusMLClasses",
            id=corpus_id,
        )
        self.classes[corpus_id] = {
            ml_class["name"]: ml_class["id"] for ml_class in corpus_classes["results"]
        }
        logger.info(f"Loaded {len(self.classes[corpus_id])} ML classes")

    def get_ml_class_id(self, corpus_id, ml_class):
        """
        Return the ID corresponding to the given class name on a specific corpus
        """
        if not self.classes.get(corpus_id):
            self.load_corpus_classes(corpus_id)

        ml_class_id = self.classes[corpus_id].get(ml_class)
        assert ml_class_id, f"ml_class '{ml_class}' doesn't exist on corpus {corpus_id}"

        return ml_class_id

    def create_sub_element(self, element, type, name, polygon):
        """
        Create a child element on the given element through API
        Return the ID of the created sub element
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert type and isinstance(
            type, str
        ), "type shouldn't be null and should be of type str"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert polygon and isinstance(
            polygon, list
        ), "polygon shouldn't be null and should be of type list"
        assert len(polygon) >= 3, "polygon should have at least three points"
        assert all(
            isinstance(point, list) and len(point) == 2 for point in polygon
        ), "polygon points should be lists of two items"
        assert all(
            isinstance(coord, (int, float)) for point in polygon for coord in point
        ), "polygon points should be lists of two numbers"
        if self.is_read_only:
            logger.warning("Cannot create element as this worker is in read-only mode")
            return

        sub_element = self.api_client.request(
            "CreateElement",
            body={
                "type": type,
                "name": name,
                "image": element.zone.image.id,
                "corpus": element.corpus.id,
                "polygon": polygon,
                "parent": element.id,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_element(element.id, type)

        return sub_element["id"]

    def create_transcription(self, element, text, type, score):
        """
        Create a transcription on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert type and isinstance(
            type, TranscriptionType
        ), "type shouldn't be null and should be of type TranscriptionType"
        assert text and isinstance(
            text, str
        ), "text shouldn't be null and should be of type str"
        assert (
            score and isinstance(score, float) and 0 <= score <= 1
        ), "score shouldn't be null and should be a float in [0..1] range"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcription as this worker is in read-only mode"
            )
            return

        self.api_client.request(
            "CreateTranscription",
            id=element.id,
            body={
                "text": text,
                "type": type.value,
                "worker_version": self.worker_version_id,
                "score": score,
            },
        )
        self.report.add_transcription(element.id, type.value)

    def create_classification(
        self, element, ml_class, confidence, high_confidence=False
    ):
        """
        Create a classification on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert ml_class and isinstance(
            ml_class, str
        ), "ml_class shouldn't be null and should be of type str"
        assert (
            confidence and isinstance(confidence, float) and 0 <= confidence <= 1
        ), "confidence shouldn't be null and should be a float in [0..1] range"
        assert isinstance(
            high_confidence, bool
        ), "high_confidence shouldn't be null and should be of type bool"
        if self.is_read_only:
            logger.warning(
                "Cannot create classification as this worker is in read-only mode"
            )
            return

        self.api_client.request(
            "CreateClassification",
            body={
                "element": element.id,
                "ml_class": self.get_ml_class_id(element.corpus.id, ml_class),
                "worker_version": self.worker_version_id,
                "confidence": confidence,
                "high_confidence": high_confidence,
            },
        )
        self.report.add_classification(element.id, ml_class)

    def create_entity(self, element, name, type, corpus, metas=None, validated=None):
        """
        Create an entity on the given corpus through API
        Return the ID of the created entity
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert type and isinstance(
            type, EntityType
        ), "type shouldn't be null and should be of type EntityType"
        assert corpus and isinstance(
            corpus, str
        ), "corpus shouldn't be null and should be of type str"
        if metas:
            assert isinstance(metas, dict), "metas should be of type dict"
        if validated:
            assert isinstance(validated, bool), "validated should be of type bool"
        if self.is_read_only:
            logger.warning("Cannot create entity as this worker is in read-only mode")
            return

        entity = self.api_client.request(
            "CreateEntity",
            body={
                "name": name,
                "type": type.value,
                "metas": metas,
                "validated": validated,
                "corpus": corpus,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_entity(element.id, entity["id"], type.value, name)

        return entity["id"]

    def create_element_transcriptions(
        self, element, sub_element_type, transcription_type, transcriptions
    ):
        """
        Create multiple sub elements with their transcriptions on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert sub_element_type and isinstance(
            sub_element_type, str
        ), "sub_element_type shouldn't be null and should be of type str"
        assert transcription_type and isinstance(
            transcription_type, TranscriptionType
        ), "transcription_type shouldn't be null and should be of type TranscriptionType"
        assert transcriptions and isinstance(
            transcriptions, list
        ), "transcriptions shouldn't be null and should be of type list"

        for index, transcription in enumerate(transcriptions):
            text = transcription.get("text")
            assert text and isinstance(
                text, str
            ), f"Transcription at index {index} in transcriptions: text shouldn't be null and should be of type str"

            score = transcription.get("score")
            assert (
                score and isinstance(score, float) and 0 <= score <= 1
            ), f"Transcription at index {index} in transcriptions: score shouldn't be null and should be a float in [0..1] range"

            polygon = transcription.get("polygon")
            assert polygon and isinstance(
                polygon, list
            ), f"Transcription at index {index} in transcriptions: polygon shouldn't be null and should be of type list"
            assert (
                len(polygon) >= 3
            ), f"Transcription at index {index} in transcriptions: polygon should have at least three points"
            assert all(
                isinstance(point, list) and len(point) == 2 for point in polygon
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two items"
            assert all(
                isinstance(coord, (int, float)) for point in polygon for coord in point
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two numbers"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcriptions as this worker is in read-only mode"
            )
            return

        annotations = self.api_client.request(
            "CreateElementTranscriptions",
            id=element.id,
            body={
                "element_type": sub_element_type,
                "transcription_type": transcription_type.value,
                "worker_version": self.worker_version_id,
                "transcriptions": transcriptions,
                "return_elements": True,
            },
        )
        for annotation in annotations:
            if annotation["created"]:
                logger.debug(
                    f"A sub_element of {element.id} with type {sub_element_type} was created during transcriptions bulk creation"
                )
                self.report.add_element(element.id, sub_element_type)
            self.report.add_transcription(annotation["id"], transcription_type.value)

        return annotations

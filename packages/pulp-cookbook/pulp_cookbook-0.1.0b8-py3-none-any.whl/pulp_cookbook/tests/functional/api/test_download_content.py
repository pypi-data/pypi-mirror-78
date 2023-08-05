# (C) Copyright 2019 Simon Baatz <gmbnomis@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Tests that verify download of content served by Pulp."""
import unittest
from random import choice
from urllib.parse import urljoin

from pulp_smash import api, config, exceptions
from pulp_smash.pulp3.utils import (
    delete_orphans,
    gen_distribution,
    gen_remote,
    gen_repo,
    modify_repo,
    sync,
)

from pulp_cookbook.tests.functional.api.utils import (
    create_publication,
    get_content_and_unit_paths,
    get_cookbook_content,
    http_get_sha256,
)
from pulp_cookbook.tests.functional.constants import (
    fixture_u1,
    COOKBOOK_DISTRIBUTION_PATH,
    COOKBOOK_REMOTE_PATH,
    COOKBOOK_REPO_PATH,
)


class DownloadContentTestCase(unittest.TestCase):
    """Verify whether content served by pulp can be downloaded."""

    def create_and_sync_repo(self, cfg, client, policy):
        repo = client.post(COOKBOOK_REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo["pulp_href"])

        body = gen_remote(fixture_u1.url, policy=policy)
        remote = client.post(COOKBOOK_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote["pulp_href"])

        sync(cfg, remote, repo, mirror=True)
        return client.get(repo["pulp_href"])

    def create_distribution(self, cfg, client, repo):
        """Create a publication for the latest repo version and a distribution."""
        # Create a publication.
        publication = create_publication(cfg, repo)
        self.addCleanup(client.delete, publication["pulp_href"])

        # Create a distribution.
        body = gen_distribution()
        body["publication"] = publication["pulp_href"]
        response_dict = client.post(COOKBOOK_DISTRIBUTION_PATH, body)
        dist_task = client.get(response_dict["task"])
        distribution_href = dist_task["created_resources"][0]
        distribution = client.get(distribution_href)
        self.addCleanup(client.delete, distribution_href)

        # Assert that the publication contains a reference to the distribution
        publication = client.get(publication["pulp_href"])
        self.assertEqual(publication["distributions"], [distribution_href])

        return distribution

    def download_check(self, cfg, client, repo, distribution, policy):
        """Verify the '/universe' endpoint, download and check a cookbook."""
        # pulp_cookbook universe live endpoint contains
        # all cookbooks
        distribution_base_url = distribution["base_url"] + "/"
        universe_url = distribution_base_url + "universe"

        universe = client.get(universe_url)
        for content, publication_path in get_content_and_unit_paths(repo):
            u_url = universe[content["name"]][content["version"]]["download_url"]
            self.assertEqual(u_url, urljoin(distribution_base_url, publication_path))

        # Pick a cookbook, and download it from Fixtures…
        cu, unit_path = choice(get_content_and_unit_paths(repo))
        fixtures_hash = http_get_sha256(urljoin(fixture_u1.url, unit_path))

        # …and Pulp content
        client.response_handler = api.safe_handler

        unit_url = urljoin(distribution_base_url, unit_path)
        pulp_hash = http_get_sha256(unit_url)

        self.assertEqual(fixtures_hash, pulp_hash)

        # Verify that the content unit contains the right sha256
        cu_updated = client.get(cu["pulp_href"]).json()
        if policy != "streamed":
            self.assertEqual(fixtures_hash, cu_updated["content_id"])
            self.assertIsNotNone(cu_updated["artifact"])
        else:
            self.assertIsNone(cu_updated["artifact"])

    def sync_and_download_check(self, policy):
        """Verify whether content served by pulp can be downloaded.

        The process of publishing content is more involved in Pulp 3 than it
        was under Pulp 2. Given a repository, the process is as follows:

        1. Create a publication from the repository. (The latest repository
           version is selected if no version is specified.) A publication is a
           repository version plus metadata.
        2. Create a distribution from the publication. The distribution defines
           at which URLs a publication is available. For the cookbook plugin
           this is below a live API at ``pulp_cookbook/market/`` e.g.
           ``http://example.com/pulp_cookbook/market/foo/`` and
           ``http://example.com/pulp_cookbook/market/bar/``.

        Do the following:

        1. Create, populate, publish, and distribute a repository.
        2. Select a random content unit in the distribution. Download that
           content unit from Pulp, and verify that the content unit has the
           same checksum when fetched directly from fixtures.

        This test targets the following issues:

        * `Pulp #2895 <https://pulp.plan.io/issues/2895>`_
        * `Pulp Smash #872 <https://github.com/PulpQE/pulp-smash/issues/872>`_
        """
        cfg = config.get_config()
        delete_orphans(cfg)
        client = api.Client(cfg, api.json_handler)
        repo = self.create_and_sync_repo(cfg, client, policy)
        distribution = self.create_distribution(cfg, client, repo)
        self.download_check(cfg, client, repo, distribution, policy)

    def sync_merge_and_download_check(self, policy):
        """
        Merge two repos synced from same source and publish.

        1. sync repo and repo2 from the same source
        2. Add all content units from repo2 to repo
        3. publish and create distribution for repo
        4. Perform download check
        """
        cfg = config.get_config()
        delete_orphans(cfg)
        client = api.Client(cfg, api.json_handler)
        repo = self.create_and_sync_repo(cfg, client, policy)
        repo2 = self.create_and_sync_repo(cfg, client, policy)

        cb_content = get_cookbook_content(repo2)
        modify_repo(cfg, repo, add_units=cb_content)

        repo = client.get(repo["pulp_href"])
        distribution = self.create_distribution(cfg, client, repo)
        self.download_check(cfg, client, repo, distribution, policy)

    def test_download_immediate_policy(self):
        self.sync_and_download_check(policy="immediate")

    def test_download_on_demand_policy(self):
        self.sync_and_download_check(policy="on_demand")

    def test_download_streamed_policy(self):
        self.sync_and_download_check(policy="streamed")

    def test_download_merged_immediate_policy(self):
        # When using immediate policy, same content units are merged (sha256 is
        # known). Therefore, there are no duplicate content units in the repo.
        self.sync_merge_and_download_check(policy="immediate")

    def test_download_merged_on_demand_policy(self):
        #  When using non-immediate policy, content units can't be merged
        #  (sha256 is unknown). Therefore, creating a repository version must fail.
        with self.assertRaisesRegex(
            exceptions.TaskReportError,
            r"repository version would contain multiple versions of cookbooks:",
        ):
            self.sync_merge_and_download_check(policy="on_demand")

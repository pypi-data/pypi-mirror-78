#  Copyright (c) 2019 Toyota Research Institute.  All rights reserved.

import unittest
import boto3
import os
import pandas as pd

os.environ['CAMD_S3_BUCKET'] = 'camd-test'
from camd.campaigns.structure_discovery import ProtoDFTCampaign
from camd.agent.stability import AgentStabilityML5
from camd.agent.base import RandomAgent
from camd.analysis import StabilityAnalyzer
from camd.experiment.base import ATFSampler
from camd import CAMD_S3_BUCKET, CAMD_TEST_FILES
from camd.utils.data import filter_dataframe_by_composition, load_dataframe
from monty.tempfile import ScratchDir

CAMD_DFT_TESTS = os.environ.get("CAMD_DFT_TESTS", False)
SKIP_MSG = "Long tests disabled, set CAMD_DFT_TESTS to run long tests"


def teardown_s3():
    """Tear down test files in s3"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(CAMD_S3_BUCKET)
    bucket.objects.filter(Prefix="proto-dft-2/runs/Si").delete()
    bucket.objects.filter(Prefix="proto-dft-2/submit/Si").delete()


class ProtoDFTCampaignTest(unittest.TestCase):
    def test_simulated(self):
        exp_dataframe = pd.read_pickle(os.path.join(CAMD_TEST_FILES, "mn-ni-o-sb.pickle"))
        experiment = ATFSampler(exp_dataframe)
        candidate_data = exp_dataframe.iloc[:, :-11]
        agent = RandomAgent(n_query=2)
        analyzer = StabilityAnalyzer(hull_distance=0.2)
        # Reduce seed_data
        seed_data = load_dataframe("oqmd1.2_exp_based_entries_featurized_v2")
        seed_data = filter_dataframe_by_composition(seed_data, "MnNiOSb")
        with ScratchDir('.'):
            campaign = ProtoDFTCampaign(
                candidate_data=candidate_data, agent=agent, experiment=experiment,
                analyzer=analyzer, seed_data=seed_data,
                heuristic_stopper=5
            )
            campaign.autorun()

    @unittest.skipUnless(CAMD_DFT_TESTS, SKIP_MSG)
    def test_simple_dft(self):
        with ScratchDir('.'):
            campaign = ProtoDFTCampaign.from_chemsys("Si")
            # Nerf agent a bit
            agent = AgentStabilityML5(n_query=2)
            campaign.agent = agent
            campaign.autorun()
            teardown_s3()


if __name__ == '__main__':
    unittest.main()

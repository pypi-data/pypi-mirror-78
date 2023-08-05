import unittest
import tempfile

import ods
from staroid import Staroid
import os, time

def integration_test_ready():
    return "STAROID_ACCESS_TOKEN" in os.environ and "STAROID_ACCOUNT" in os.environ

TEST_REGION="aws us-west2"

class TestSpark(unittest.TestCase):
    def test_install(self):
        ods.init()
        spark = ods.spark("test")

        # install without exception
        spark.install()

        # second install call should finish quickly
        start_time = time.time()
        spark.install()
        elapsed = time.time() - start_time

        self.assertTrue(elapsed < 3)

    @unittest.skipUnless(integration_test_ready(), "Integration test environment is not configured")
    def test_run_spark_job(self):
        # given ske
        ske = "opends spark it-test"
        Staroid().cluster().create(ske, TEST_REGION)

        # init with ske name
        ods.init(ske=ske)

        spark = ods.spark("test").session()
        df = spark.createDataFrame([{"hello": "world"} for x in range(100)])
        self.assertEqual(100, df.count())

        # delete cluster instance
        ods.spark("test").delete()

        # clean up
        Staroid().cluster().delete(ske)


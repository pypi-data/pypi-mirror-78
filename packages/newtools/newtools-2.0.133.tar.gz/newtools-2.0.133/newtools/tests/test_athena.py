import unittest
from os import path

from dativa.tools.aws import S3Client

from newtools import AthenaClient, log_to_stdout

logger = log_to_stdout("newtools")


# noinspection SqlNoDataSourceInspection
class AthenaTest(unittest.TestCase):
    source_file = "s3://deductive-tools-testing/s3_upload_athena/demographic/"
    tablename = "demographic"
    region = "eu-west-1"
    database = "test_database"
    bucket = "deductive-tools-testing"
    output_location = "s3://aws-athena-query-results-933373196108-eu-west-1/"
    invalid_file_location = "/this/location/does/not/exist.csv"
    athena_client = None

    @classmethod
    def setUpClass(cls):
        logger.info("Running setupclass for Athena test")
        cls.base_path = "{0}/test_data/".format(
            path.dirname(path.abspath(__file__)))
        logger.info("Uploading test data to s3")
        cls.s3 = S3Client()
        cls.s3.delete_files(cls.bucket, "s3_upload_athena")

        cls.s3.put_folder(source=path.join(cls.base_path, "s3_upload_athena"),
                          bucket=cls.bucket,
                          destination="s3_upload_athena",
                          file_format="*")

        cls.athena_client = AthenaClient(cls.region, cls.database, max_retries=2)

        logger.info("Creating Table: {}".format(cls.tablename))
        cls.athena_client.add_query(
            f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS {cls.tablename}(
              jurisdiction_name integer,
              count_participants integer,
              count_female integer,
              percent_female float,
              count_male integer,
              percent_male float)
            PARTITIONED BY (`part` string)
            ROW FORMAT SERDE
              'org.apache.hadoop.hive.serde2.OpenCSVSerde'
            STORED AS INPUTFORMAT
              'org.apache.hadoop.mapred.TextInputFormat'
            OUTPUTFORMAT
              'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
              '{cls.source_file}'
            TBLPROPERTIES ('skip.header.line.count'='1')
            ;""", output_location=cls.output_location)

        cls.athena_client.add_query(
            f"""
            ALTER TABLE {cls.tablename} ADD IF NOT EXISTS PARTITION (part="1")
            LOCATION '{cls.source_file}part=1/'
            ;""", output_location=cls.output_location)

        cls.athena_client.add_query(
            f"""
            ALTER TABLE {cls.tablename} ADD IF NOT EXISTS PARTITION (part="2")
            LOCATION '{cls.source_file}part=2/'
            """, output_location=cls.output_location)

        cls.athena_client.wait_for_completion()

    @classmethod
    def tearDownClass(cls):
        cls.athena_client.add_query(f"DROP TABLE {cls.tablename}", output_location=cls.output_location)
        cls.athena_client.wait_for_completion()

    def test_queries(self):
        logger.info("Querying athena")
        self.s3.delete_files(self.bucket, "pq")
        self.athena_client.add_query("select * from {}".format(self.tablename),
                                     "athena_test",
                                     "{0}pq/".format(self.output_location))
        count = self.athena_client.add_query("select count(*) from {}".format(self.tablename),
                                             "athena_test",
                                             self.output_location)
        self.athena_client.wait_for_completion()

        # self.assertEqual(0, self.scp.number_active)
        self.assertEqual(0, self.athena_client.number_active)

        df_count = self.athena_client.get_query_result(count)
        self.assertEqual(df_count.iloc[0, 0], 42)

    def test_stopping_queries(self):
        self.s3.delete_files(self.bucket, "pq")
        ac = AthenaClient(self.region, self.database, max_retries=2, max_queries=1)
        ac.add_query("select * from {}".format(self.tablename),
                     "athena_test",
                     "{0}pq/".format(self.output_location))
        ac.add_query("select count(*) from {}".format(self.tablename),
                     "athena_test",
                     self.output_location)
        self.assertEqual(1, ac.number_active)
        self.assertEqual(1, ac.number_pending)
        ac.stop_and_delete_all_tasks()
        self.assertEqual(0, ac.number_active)

    def test_raise_athena_exception(self):
        logger.info("Checking if AthenaClient throws exception when a request\
                     for results of an incomplete query is made")

        query = self.athena_client.add_query("select * from {}".format(self.tablename),
                                             "athena_test",
                                             self.output_location)
        with self.assertRaises(ValueError):
            self.athena_client.get_query_result(query)

    def test_reset_query(self):
        """Test to check if is_complete  attribute for a failed query is
        set after checking query status"""
        with self.assertRaises(TimeoutError):
            self.athena_client.add_query("select {0} from {1}".format("table_doesnt_exist", self.tablename),
                                         "athena_test",
                                         self.output_location)
            self.athena_client.wait_for_completion()

    def test_maximum_retries_imposed(self):
        """Test to check query doesn't exceed maximum retries"""
        with self.assertRaises(TimeoutError):
            query = self.athena_client.add_query("select {0} from {1}".format("table_doesnt_exist", self.tablename),
                                                 "athena_test",
                                                 self.output_location)
            self.athena_client.wait_for_completion()

        self.athena_client._update_task_status(query)
        self.assertEqual(query.retries, 2)
        self.assertTrue(query.is_complete)
        self.assertEqual(query.error, "SYNTAX_ERROR: line 1:8: Column 'table_doesnt_exist' cannot be resolved")

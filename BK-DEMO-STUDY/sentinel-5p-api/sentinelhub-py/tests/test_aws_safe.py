import unittest
import os

from sentinelhub import AwsTileRequest, AwsProductRequest, read_data, write_data, DataCollection, AwsConstants,\
    TestSentinelHub, TestCaseContainer


class TestSafeFormat(TestSentinelHub):

    class SafeTestCase(TestCaseContainer):
        """
        Container for each test case of .SAFE structure testing
        """

        def get_filename(self):
            return os.path.join(TestSafeFormat.INPUT_FOLDER, '{}.csv'.format(self.name))

        def get_request_data(self):
            return [(req.url, req.filename[:]) for req in self.request.get_download_list()]

        def load_truth(self):
            return [tuple(item) for item in read_data(self.get_filename())]

        def save_truth(self):
            """ Use this method only to create new unittests
            """
            write_data(self.get_filename(), self.get_request_data())

        @staticmethod
        def compare_safe_struct(true_safe, req_safe):
            """ This method compares two lists with safe structure
            """
            true_set = set(true_safe)
            req_set = set(req_safe)
            missing = [item for item in true_set if item not in req_set]
            redundant = [item for item in req_set if item not in true_set]
            if len(missing) + len(redundant) > 0:
                return False, 'Missing files: {}\nRedundant files: {}'.format(missing, redundant)

            for index, (true_item, req_item) in enumerate(zip(true_safe, req_safe)):
                if true_item != req_item:
                    return False, 'Wrong order in line {}, {} expected but {} obtained.' \
                                  '\nEntire struct:\n{}'.format(index, true_item, req_item, req_safe)

            return True, "The SAFE structures match!"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_cases = [
            cls.SafeTestCase('L1C_02.01',
                             AwsProductRequest('S2A_OPER_PRD_MSIL1C_PDMC_20151218T020842_R115_V20151217T224602_'
                                               '20151217T224602', bands=AwsConstants.S2_L1C_BANDS,
                                               metafiles=AwsConstants.S2_L1C_METAFILES,
                                               tile_list=['T59HNA'], safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.01_tile',
                             AwsTileRequest(tile='29KQB', time='2016-04-12', aws_index=None,
                                            data_collection=DataCollection.SENTINEL2_L1C, safe_format=True,
                                            data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.02',
                             AwsProductRequest('S2A_OPER_PRD_MSIL1C_PDMC_20160606T232310_R121_V20160526T0'
                                               '84351_20160526T084351.SAFE', tile_list=['34HCF'],
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.04_old',
                             AwsProductRequest('S2A_OPER_PRD_MSIL1C_PDMC_20160910T174323_R071_V20160701T2'
                                               '04642_20160701T204643', safe_format=True,
                                               data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.04',
                             AwsProductRequest('S2A_MSIL1C_20170413T104021_N0204_R008_T31SCA_20170413T104021',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.05',
                             AwsProductRequest('S2A_MSIL1C_20171012T112111_N0205_R037_T29SQC_20171012T112713',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.06',
                             AwsProductRequest('S2A_MSIL1C_20180331T212521_N0206_R043_T07WFR_20180401T005612',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.06_2',
                             AwsProductRequest('S2A_MSIL1C_20181004T175151_N0206_R141_T18XVM_20190219T160358',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.07',
                             AwsProductRequest('S2A_MSIL1C_20181119T031011_N0207_R075_T50TLK_20181119T061056',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L1C_02.07_2',
                             AwsProductRequest('S2A_MSIL1C_20190129T143751_N0207_R096_T20LLK_20190225T132350',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.01',
                             AwsProductRequest('S2A_USER_PRD_MSIL2A_PDMC_20160310T041843_R138_V20160308T131142_'
                                               '20160308T131142', safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.05',  # L2A_02.04 is the same
                             AwsProductRequest('S2A_MSIL2A_20170827T105651_N0205_R094_T31WFN_20170827T105652',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.06',
                             AwsProductRequest('S2B_MSIL2A_20180216T102059_N0206_R065_T35VLL_20180216T122659',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.07',
                             AwsProductRequest('S2A_MSIL2A_20180402T151801_N0207_R068_T33XWJ_20180402T202222',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.08',
                             AwsProductRequest('S2A_MSIL2A_20181005T104021_N0208_R008_T34WEU_20181007T220806',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.09',
                             AwsProductRequest('S2B_MSIL2A_20181029T093109_N0209_R136_T35UMQ_20181029T122414',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.10',
                             AwsProductRequest('S2B_MSIL2A_20181115T110319_N0210_R094_T32VLJ_20181115T142501',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER)),
            cls.SafeTestCase('L2A_02.11',
                             AwsProductRequest('S2B_MSIL2A_20190310T235739_N0211_R030_T57MVM_20190311T013927',
                                               safe_format=True, data_folder=cls.INPUT_FOLDER))
        ]

        # Uncomment the following only when creating new test cases
        # for test_case in cls.test_cases:
        #     test_case.save_truth()
        #     test_case.request.save_data()

    def test_safe_struct(self):
        for test_case in self.test_cases:
            with self.subTest(msg='Test case {}'.format(test_case.name)):
                true_safe = test_case.load_truth()
                req_safe = test_case.get_request_data()
                is_equal, message = self.SafeTestCase.compare_safe_struct(true_safe, req_safe)
                self.assertTrue(is_equal, message)


if __name__ == '__main__':
    unittest.main()
